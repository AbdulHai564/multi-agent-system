from e2b_code_interpreter import Sandbox
from config import E2B_API_KEY


def parse_output(execution):
    output=""
    if execution.logs.stdout:
        output+="".join(execution.logs.stdout)
    if execution.logs.stderr:
        output+="\nErrors:\n"+"".join(execution.logs.stderr)
    return output or "code ran but no ouput was produced "

def execute_code(code: str):
    sandbox = Sandbox.create(api_key=E2B_API_KEY, timeout=120)
    result = sandbox.run_code(code)
    sandbox.kill()
    return parse_output(result)


def execute_with_packages(code: str, packages: list):
    sandbox = Sandbox.create(api_key=E2B_API_KEY, timeout=120)
    for package in packages:
        sandbox.run_code(f"!pip install {package}")
    result = sandbox.run_code(code)
    sandbox.kill()
    return parse_output(result)






                        