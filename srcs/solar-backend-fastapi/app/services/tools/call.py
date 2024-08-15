# import importlib
# import os
#
# # Path to the directory containing the module files
# module_directory = 'functions'
#
# # List all Python files in the directory and remove the '.py' extension for import
# module_names = [f.replace('.py', '') for f in os.listdir(module_directory) if f.endswith('.py')]
#
# functions = {}
# functions_description = []
#
# for name in module_names:
#     try:
#         # Construct the module import path
#         module_path = f"{module_directory}.{name}"
#
#         # Dynamically import each module
#         module = importlib.import_module(module_path)
#
#         # Map the module's function to its name in the dictionary
#         functions[name] = module.function
#
#         # Add the module's description to functions_description list
#         functions_description.append(module.description)
#
#     except ImportError:
#         print(f"Failed to import {name}")
#     except AttributeError:
#         print(f"Module {name} does not have the required attributes")
#     except Exception as e:
#         print(f"An unexpected error occurred while importing {name}: {e}")
#
# # Output the loaded functions and their descriptions
# print("Loaded Functions:")
# for func in functions:
#     print(f"{func} - {functions[func]}")
#
# print("\nDescriptions:")
# for desc in functions_description:
#     print(desc)