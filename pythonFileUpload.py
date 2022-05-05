import io
import os

from google.auth.transport.requests import Request
from google.protobuf import service
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from bs4 import BeautifulSoup




file_id = '1guHKDs7FE9oGoHrOfuNjKIeNRQeO6NWY51h4bS_z9fk'
git_file_location = '/home/pi/personalwebsite/index.html'
PATH_OF_GIT_REPO = r'/home/pi/personalwebsite/.git'
COMMIT_MESSAGE = 'Auto Update'

creds = None
drive_service = build('drive', 'v3', credentials=creds)
request = drive_service.files().export_media(fileId=file_id,
                                             mimeType='text/html')
fh = io.BytesIO()
downloader = MediaIoBaseDownload(fh, request)
done = False

name = drive_service.files().get(fileId=file_id).execute()['name']

while done is False:
    status, done = downloader.next_chunk()
    print("Download %d%%." % int(status.progress() * 100))
file_name = os.path.abspath(git_file_location)
f = open(file_name, 'wb')

f.write(fh.getvalue())

# load the file
with open(git_file_location) as inf:
    txt = inf.read()
    soup = BeautifulSoup(txt, 'html.parser')


def a_href(url, label='', target='_blank', **kwargs):
    soup = BeautifulSoup('', 'html.parser')
    combined_attrs = dict(target=target, href=url, **kwargs)
    tag = soup.new_tag(name='a', attrs=combined_attrs)
    tag.string = label
    return tag  # or tag.prettify() for better formatting

soup.body.append(a_href("https://github.com/djessemoody/personalwebsite/blob/master/pythonFileUpload.py",label="Check out the script that grabs this from google docs and uploads it to moodyiii.com here"))

with open(git_file_location, "w") as outf:
    outf.write(str(soup.prettify()))


from git import Repo



def git_push():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        origin = repo.remote(name='origin')
        origin.pull()
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin.push()
    except BaseException as err:
        print('Some error occured while pushing the code')

git_push()
