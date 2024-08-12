import json
import os
import sys

import dotenv
import pandas as pd
from openai import OpenAI

from app.services.tools.init_fuctions import initialize_functions

dotenv.load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"), base_url="https://api.upstage.ai/v1/solar")

project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_root)

init_data = pd.read_csv("../data/locations.csv")

functions_module_dir = 'tools/functions'
functions_module_names = [f.replace('.py', '') for f in os.listdir(functions_module_dir) if f.endswith('.py')]
print(f'module_names: {functions_module_names}')

FUNCTIONS, FUNCTION_DESCRIPTIONS = initialize_functions(functions_module_names, functions_module_dir)
print(f'FUNCTIONS: {FUNCTIONS}')


def run_conversation(message):
    messages = [
        {
            "role": "user",
            "content": message,
        }
    ]
    tools = FUNCTION_DESCRIPTIONS
    response = client.chat.completions.create(
        model="solar-1-mini-chat",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    print(f'tool_calls: {tool_calls}')

    if tool_calls:
        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = FUNCTIONS[function_name]
            function_args = json.loads(tool_call.function.arguments)
            print(f"function_args: {function_args}")
            function_response = function_to_call(
                region_name=function_args.get("region_name"),
                data=init_data
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
        print(f'messages: {messages}')
        return client.chat.completions.create(
            model="solar-1-mini-chat",
            messages=messages,
        )


print(run_conversation("Hi, Please recommend a place to drink near east-kareum"))
