def get_data_of_stay(region_name, data, location_id):
    """Get stay data"""
    # 조건에 맞는 데이터 필터링
    category_name = "stay"
    filtered_data = data[(data['region_name'] == region_name) & (data['category_name'] == category_name) & (
            data['location_id'] == location_id)]
    # 필터링된 데이터가 존재하는지 확인
    if filtered_data.empty:
        return f"No data found for region '{region_name}' and category '{category_name}'"
    return filtered_data["location_description"]


description = {
    "type": "function",
    "function": {
        "name": "get_data_of_stay",
        "description": "Use region_name, category_name, and stay_id to retrieve the complete data of stay.",
        "parameters": {
            "type": "object",
            "properties": {
                "region_name": {
                    "type": "string",
                    "description": "Region name e.g. east-kareum, al-kareum",
                },
                "location_id": {
                    "type": "int",
                    "description": "Id of stay e.g. 0, 1, 2",
                },
            },
            "required": ["region_name", "location_id"],
        },
    },
}

# data['region_id']['category_id']['location_id']
# data['est_karuem']['attraction']['녹산로']

# # 서비스 계정 키 파일 경로
# SERVICE_ACCOUNT_FILE = 'C:\\Upstage\\data\\service-account-file.json'

# # 필요한 범위 설정 (Google Drive API 사용)
# SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# # 서비스 계정 자격 증명 설정
# credentials = service_account.Credentials.from_service_account_file(
#         SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# # Google Docs API 클라이언트 생성
# docs_service = build('docs', 'v1', credentials=credentials)

# # In production, this could be your backend API or an external API
# def function(file_id, docs_service=docs_service):
#     """Get real time hotel data"""
#     # 문서 내용 가져오기
#     document = docs_service.documents().get(documentId=DOCUMENT_ID).execute()

#     # 문서 본문 가져오기
#     doc_content = document.get('body').get('content')

#     # 문서 내용 파싱
#     def read_paragraph_element(element):
#         text_run = element.get('textRun')
#         if not text_run:
#             return ''
#         return text_run.get('content')

#     text = ''
#     for value in doc_content:
#         if 'paragraph' in value:
#             doc_content = value.get('paragraph').get('elements')
#             for elem in doc_content:
#                 text += read_paragraph_element(elem)
#         elif 'table' in value:
#             table = value.get('table')
#             for row in table.get('tableRows'):
#                 cells = row.get('tableCells')
#                 for cell in cells:
#                     text += read_structural_elements(cell.get('content'))
#         elif 'tableOfContents' in value:
#             toc = value.get('tableOfContents')
#             text += read_structural_elements(toc.get('content'))
#     return text

# description = {
#         "type": "function",
#         "function": {
#             "name": "get_current_weather",
#             "description": "Get the current weather in a given location",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "location": {
#                         "type": "string",
#                         "description": "The city and state, e.g. San Francisco, CA",
#                     },
#                     "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
#                 },
#                 "required": ["location"],
#             },
#         },
#     }
