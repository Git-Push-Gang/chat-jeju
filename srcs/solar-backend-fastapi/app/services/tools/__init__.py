# import importlib
# import inspect
# import os
# import sys
#
# # Path to the directory containing the module files
#
# # module_directory = 'functions'
# project_root = os.path.abspath(os.path.dirname(__file__))
# sys.path.append(project_root)
#
#
#
import importlib
import inspect
import os


def initialize_functions(module_names, module_directory):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    module_directory = os.path.join(script_dir, 'functions')

    print(f'functions_path: {module_directory}')
    module_names = [f.replace('.py', '') for f in os.listdir(module_directory) if f.endswith('.py')]

    print(f'functions_module_names: {module_names}')
    functions = {}
    function_descriptions = []

    for name in module_names:
        try:
            # 모듈 경로를 동적으로 생성하여 임포트
            module_path = f"{module_directory}.{name}".replace('/', '.')
            module = importlib.import_module(module_path)

            # 모듈 내의 모든 함수 찾기
            for func_name, func in inspect.getmembers(module, inspect.isfunction):
                functions[func_name] = func

            # 설명이 있는 경우 추가
            if hasattr(module, 'description'):
                function_descriptions.append(module.description)
            else:
                print(f"Module {name} does not have a 'description' attribute")

        except ImportError as e:
            print(f"Failed to import {name}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while importing {name}: {e}")

    return functions, function_descriptions

#
# functions, function_descriptions = initialize_functions()
# print(f'FUNCTIONS: {functions}')
# print(f'FUNCTION_DESCRIPTIONS: {function_descriptions}')
