import yaml
import regex as re


def read_yaml(file_path: str, mode: str = 'r'):
    with open(file_path, mode) as file:
        prompts = yaml.safe_load(file)
    return prompts


def get_prommpts():
    file_path = "src/vidsynthai/configs/prompts.yaml"
    prompts = read_yaml(file_path, 'r')
    return prompts


def get_model_config():
    file_path = "src/vidsynthai/configs/model.yaml"
    model_config = read_yaml(file_path, 'r')
    return model_config


def get_user_chat_format(user_message: str):
    return {'role': 'user', 'content': user_message}


def get_python_code(response_str: str):
    pattern = r'```(.*?)```'
    matches = re.findall(pattern, response_str, re.DOTALL)
    if matches:
        return matches[0].replace("python", "").strip()
    return None


def write_code_to_file(file_path: str, code: str):
    with open(file_path, 'w') as file:
        file.write(code)
    return "Successfully done!"


def extract_transcript(text: str):
    pattern = r"<TRANSCRIPT>(.*?)</TRANSCRIPT>"

    match = re.findall(pattern, text, re.DOTALL)
    if match:
        # print(match.group(1))  # Extracted content
        return ''.join(match)