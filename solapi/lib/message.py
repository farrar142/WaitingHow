import requests
from . import config
from . import solapi

def sendMany(data):
  return requests.post(config.getUrl('/messages/v4/send-many'), headers=solapi.get_headers(config.apiKey, config.apiSecret), json=data)

def sendOne(data):
  return requests.post(config.getUrl('/messages/v4/send'), headers=solapi.get_headers(config.apiKey, config.apiSecret), json=data)

def post(path, data):
  return requests.post(config.getUrl(path), headers=solapi.get_headers(config.apiKey, config.apiSecret), json=data)

def put(path, data, headers = {}):
  headers.update(solapi.get_headers(config.apiKey, config.apiSecret))
  return requests.put(config.getUrl(path), headers=headers, json=data)

def get(path, headers = {}):
  headers.update(solapi.get_headers(config.apiKey, config.apiSecret))
  return requests.get(config.getUrl(path), headers=headers)

def delete(path):
  return requests.delete(config.getUrl(path), headers=solapi.get_headers(config.apiKey, config.apiSecret))
