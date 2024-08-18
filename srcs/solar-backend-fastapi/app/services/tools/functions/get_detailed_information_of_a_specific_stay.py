from app.data.init_stay_data import STAY_DATA, docs_service
from app.services.measure_time import measure_time


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


@measure_time
def get_document_content(file_id, docs_service=docs_service):
    document = docs_service.documents().get(documentId=file_id).execute()
    doc_content = document.get('body').get('content')
    return read_structural_elements(doc_content)


@measure_time
def get_detailed_information_of_a_specific_stay(stay_name: str):
    # 숙소 이름을 인자로 받아서 그걸 기준으로 파일 id 찾고(dict) id 기준으로 파일 내용 가져와서
    # 내용 기반 응답 생성
    try:
        stay_id = STAY_DATA[stay_name + ' ']
    except KeyError as e:
        stay_id = STAY_DATA[stay_name]
    # print(stay_id)

    return get_document_content(stay_id)


description = {
    "type": "function",
    "function": {
        "name": "get_detailed_information_of_a_specific_stay",
        "description": "Provide detailed information about a specific stay requested by a user, including peripheral "
                       "details such as whether breakfast is offered",
        "parameters": {
            "type": "object",
            "properties": {
                "stay_name": {
                    "type": "string",
                    "description": "The name of stay user want to know about stay's information not recommendation "
                                   "information, e.g. 트립스테이, oh세화",
                },
            },
            "required": ["stay_name"],
        },
    },
}

# text = get_detailed_information_of_a_specific_stay(stay_name="바띠에")
# print(text)
