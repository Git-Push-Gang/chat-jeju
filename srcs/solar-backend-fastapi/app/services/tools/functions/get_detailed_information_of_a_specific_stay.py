from google.oauth2 import service_account
from googleapiclient.discovery import build
from app.services.measure_time import measure_time


@measure_time
def get_detailed_information_of_a_specific_stay(stay_name: str):
    # 숙소 이름을 인자로 받아서 그걸 기준으로 파일 id 찾고(dict) id 기준으로 파일 내용 가져와서
    # 내용 기반 응답 생성
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    SERVICE_ACCOUNT_FILE = "C:\\Upstage\\data\\service-account-file.json"  #본인 구글API json path
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=credentials)

    docs_service = build('docs', 'v1', credentials=credentials)
    drive_service = build('drive', 'v3', credentials=credentials)
    folder_ids = ['1xtTWE3sDM5zbpeNxsS6TU8Xo7qfnF5xE',
                  '1IF_V8Q5zlfHeeVaZrwlG-8I46Lok6PiD',
                  '1VjSwUsnGlxUdCVuS6L4AW8017s_CRdcX',
                  '1A2F8Oq_E74joOh58Nb7O4LBmXlJrcWBF']

    def list_files_in_folder(folder_ids, drive_service=drive_service):
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
                return []
            else:
                for item in items:
                    mapped_dict[item['name']] = item['id']
                return mapped_dict

    stay_id = list_files_in_folder(folder_ids)[stay_name + ' ']

    # In production, this could be your backend API or an external API
    def get_document_content(file_id=stay_id, docs_service=docs_service):

        document = docs_service.documents().get(documentId=file_id).execute()

        doc_content = document.get('body').get('content')

        def read_paragraph_elements(element):
            text_run = element.get('textRun')
            if not text_run:
                return ''
            return text_run.get('content')

        def read_structural_elements(elements):
            text = ''
            for value in elements:
                if 'paragraph' in value:
                    doc_content = value.get('paragraph').get('elements')
                    for elem in doc_content:
                        text += read_paragraph_elements(elem)
                elif 'table' in value:
                    table = value.get('table')
                    for row in table.get('tableRows'):
                        cells = row.get('tableCells')
                        for cell in cells:
                            text += read_structural_elements(cell.get('content'))
                elif 'tableOfContents' in value:
                    toc = value.get('tableOfContents')
                    text += read_structural_elements(toc.get('content'))
            return text

        return read_structural_elements(doc_content)

    return get_document_content(stay_id)


description = {
    "type": "function",
    "function": {
        "name": "get_detailed_information_of_a_specific_stay",
        "description": "Provide detailed information about a specific stay requested by a user, including peripheral details such as whether breakfast is offered",
        "parameters": {
            "type": "object",
            "properties": {
                "stay_name": {
                    "type": "string",
                    "description": "The name of stay user want to know about stay's information not recommendation information, e.g. 트립스테이, oh세화",
                },
            },
            "required": ["stay_name"],
        },
    },
}

# text=get_information_of_specific_stay(stay_name="트립레시피")
# print(text)
