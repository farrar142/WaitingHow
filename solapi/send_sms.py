import json
import sys
sys.path.append('lib')
from .lib import message

def send_message(to,context):
  data = {
    u'messages': [
      {
        u'to': to,
        u'from': '01024321690',
        u'text': context
      }
    ]
  }
  res = message.sendMany(data)
  json.dumps(res.json(), indent=2, ensure_ascii=False)
  
if __name__ =="__main__":
  send_message("01024321690","test")