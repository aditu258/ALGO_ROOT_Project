from functions import FUNCTION_REGISTRY

class CodeGenerator:
    @staticmethod
    def generate_execution_code(function_name, *args):
        """
        Creates clean, ready-to-run Python code for any registered function
        Includes error handling and proper formatting
        """
        if function_name not in FUNCTION_REGISTRY:
            raise ValueError(f"Unknown function: {function_name}")
        
        function_info = FUNCTION_REGISTRY[function_name]
        
        # Build the Python script with:
        # 1. Required imports
        # 2. Main execution function
        # 3. Error handling
        # 4. Standard Python script structure
        code_template = f"""\
{function_info["imports"]}

def main():
    try:
        result = {function_name}({', '.join(map(repr, args))})
        print(f"Success! Result: {{result}}")
        return result
    except Exception as e:
        print(f"Error: {{e}}")
        return None

if __name__ == "__main__":
    main()
"""
        return code_template