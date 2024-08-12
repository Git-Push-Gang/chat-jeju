import importlib
import inspect


def initialize_functions(module_names, module_directory):
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
