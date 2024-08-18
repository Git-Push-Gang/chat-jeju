import importlib
import inspect
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
module_dir = os.path.join(current_dir, 'functions')

if module_dir not in sys.path:
    sys.path.append(module_dir)

module_names = [f.replace('.py', '') for f in os.listdir(module_dir) if f.endswith('.py')]

functions = {}
function_descriptions = []

for name in module_names:
    try:
        module = importlib.import_module(name)

        for func_name, func in inspect.getmembers(module, inspect.isfunction):
            if func_name != 'Depends':
                functions[func_name] = func

        if hasattr(module, 'description'):
            function_descriptions.append(module.description)

    except ImportError as e:
        print(f"Failed to import {module}: {e}")
