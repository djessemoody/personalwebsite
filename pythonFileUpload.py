import io
import os

from google.auth.transport.requests import Request
from google.protobuf import service
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload





file_id = '1guHKDs7FE9oGoHrOfuNjKIeNRQeO6NWY51h4bS_z9fk'
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
file_name = os.path.abspath("/home/pi/personalwebsite/index.html")
f = open(file_name, 'wb')
f.write(fh.getvalue())


from git import Repo

PATH_OF_GIT_REPO = r'/home/pi/personalwebsite/.git'  # make sure .git folder is properly configured
COMMIT_MESSAGE = 'Auto Update'

def git_push():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except BaseException as err:
        print('Some error occured while pushing the code')

git_push()
