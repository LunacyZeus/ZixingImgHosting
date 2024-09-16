PUBLISHER = 'https://publisher-devnet.walrus.space'

EPOCHS = "5"

import requests


def send_file_to_remote_server(pic):
    url = "https://publisher-devnet.walrus.space/v1/store?epochs=5"
    headers = {
        'Content-Type': 'application/octet-stream',  # 设置文件类型
    }

    # 使用流式上传文件
    response = requests.put(url, data=pic.read(), headers=headers)

    # 处理响应结果
    if response.status_code == 200:
        return response.json()  # 或者其他你需要的响应信息
    else:
        return {'error': f"Failed to upload, status code: {response.status_code}"}
