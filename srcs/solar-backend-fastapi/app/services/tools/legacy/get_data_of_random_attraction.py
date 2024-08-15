import random


def get_data_of_random_attraction(region_name, data, number=3):
    category_name = "attraction"
    filtered_data = data[(data['region_name'] == region_name) & (data['category_name'] == category_name)]

    # 필터링된 데이터가 존재하는지 확인
    if filtered_data.empty:
        return f"No data found for region '{region_name}' and category '{category_name}'"
    # number 값을 filtered_data의 길이로 제한
    number = min(number, len(filtered_data))

    whole_text = ""
    upper_limit = len(filtered_data) - 1
    for i in range(number):
        whole_text += filtered_data.iloc[random.randint(0, upper_limit)]["location_description"]

    return whole_text


description = {
    "type": "function",
    "function": {
        "name": "get_data_of_random_attraction",
        "description": "Use region_name, category_name, and number to retrieve the complete data of 3 random attraction.",
        "parameters": {
            "type": "object",
            "properties": {
                "region_name": {
                    "type": "string",
                    "description": "Region name e.g. al-kareum, west-kareum",
                },
                "number": {
                    "type": "int",
                    "description": "The number of attraction to get information e.g. 2, 3",
                },
            },
            "required": ["region_name", "number"],
        },
    },
}
