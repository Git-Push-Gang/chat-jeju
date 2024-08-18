import os

from google.oauth2 import service_account
from googleapiclient.discovery import build

from app.services.measure_time import measure_time

current_dir = os.path.dirname(os.path.abspath(__file__))
module_dir = os.path.join(current_dir, 'service-account.json')

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = module_dir  # 본인 구글API json path
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

docs_service = build('docs', 'v1', credentials=credentials)


@measure_time
def get_stay_data():
    drive_service = build('drive', 'v3', credentials=credentials)
    folder_ids = ['1xMP5O4aCu9KOfDJMnDcDOnSJ9WVd5iww',
                  '11YaiDuqxDZndnNJueh9-J-NS3oVDGrf-',
                  '1TzU3PJ3FjZZKbOKIsqKqCNfUqxHUwlZz',
                  '1XOyUSXvDqz2wJGW55dLi7HE3ru_oQW9O']

    mapped_dict = {}
    for folder_id in folder_ids:
        query = f"'{folder_id}' in parents and trashed = false"
        results = drive_service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)',
        ).execute()

        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            for item in items:
                mapped_dict[item['name']] = item['id']
    return mapped_dict


STAY_DATA = get_stay_data()
# print(STAY_DATA)
