import os
import time

import requests
import json

API_KEY = "BdCyZnSwEOGy5UtOvZGLkg22"
SECRET_KEY = "zVU0b2Vp10jXB4aMGKh55PKM899BKTdl"


def get_dependency_info(content):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "temperature": 0.95,
        "top_p": 0.8,
        "penalty_score": 1,
        "enable_system_memory": False,
        "disable_search": False,
        "enable_citation": False
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)["result"]


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


def calc_instruction_length(content):
    dockerfile_content = []
    for line in content.split('\n')[1:-1]:
        if line.strip():
            dockerfile_content.append(line)

    content_len = len(dockerfile_content)
    return content_len

def calc_file_char_num(content):
    dockerfile_content = []
    for line in content.split('\n')[1:-1]:
        if line.strip():
            dockerfile_content.append(line)

    char_num = len("\n".join(dockerfile_content))
    return char_num


if __name__ == '__main__':
    for file_name in os.listdir("../提问模板"):
        if (os.path.exists("../ENRIE-4-8k_result/" + file_name) and
                os.path.exists("../ENRIE-4-8k_result/" + file_name + "-cost_time")):
            continue
        with open("../提问模板/" + file_name, "r", encoding="utf-8") as file:
            content = file.read().replace("\n\n", "\n")
            content_len = calc_instruction_length(content)
            start = time.time()
            result = get_dependency_info(content)
            end = time.time()
            cost_time = end - start

        with open("../ENRIE-4-8k_result/" + file_name, "w", encoding="utf-8") as file:
            file.write(result)

        with open("../ENRIE-4-8k_result/" + file_name + "-cost_time", "w", encoding="utf-8") as file:
            file.write(str(content_len) + "\n")
            file.write(str(cost_time))
