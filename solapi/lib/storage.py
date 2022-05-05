import requests
import base64
import config
import solapi

def uploadImage(path):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    data = {
        'file': str(encoded_string)[2:-1],
        'type': 'MMS'
    }
    headers = solapi.get_headers(config.apiKey, config.apiSecret)
    return requests.post(config.getUrl('/storage/v1/files'), headers=headers, json=data)

def uploadRCSImage(path):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    data = {
        'file': str(encoded_string)[2:-1],
        'type': 'RCS'
    }
    headers = solapi.get_headers(config.apiKey, config.apiSecret)
    return requests.post(config.getUrl('/storage/v1/files'), headers=headers, json=data)

def uploadKakaoImage(path):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    data = {
        'file': str(encoded_string)[2:-1],
        'type': 'KAKAO'
    }
    headers = solapi.get_headers(config.apiKey, config.apiSecret)
    return requests.post(config.getUrl('/storage/v1/files'), headers=headers, json=data)
