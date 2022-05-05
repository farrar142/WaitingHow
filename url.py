import json,requests

class Urlizer:
    iam = ''
        
    def __init__(self,*args,**kwargs):
        self.iam = self.URL(*args,**kwargs)
        
    def __call__(self,*args,**kwargs):
        return self.iam
    
    class URL:
        __protocol__ = ""
        __url__ = ""
        __uri__ = ""
        params = ""
        data = {}
        header = {}
        
        def __init__(self,*args,**kwargs):
            if not Urlizer.iam:
                if args:
                    try:
                        first = args[0].split("://",1)
                        self.protocol = first[0]
                        try:
                            second = first[1].split('/',1)
                            self.url = second[0]
                            self.uri = second[1]
                        except:
                            self.url = first[1]
                            self.uri = ''
                    except:
                        self.protocol = 'http'
                        try:
                            second = args[0].split('/',1)
                            self.url = second[0]
                            self.uri = second[1]
                        except:
                            self.url = first[1]
                            self.uri = ''
                else:
                    try:
                        self.protocol = kwargs['protocol']
                    except:
                        self.protocol =  'http'
                    try:
                        self.url = kwargs['url']
                    except:
                        self.url =  ''
                    try:
                        self.uri = kwargs['url']
                    except:
                        self.uri =  ''
                print("asdsdasd")
                Urlizer.iam = self
            else:
                raise Exception("nope")
        def __str__(self):
            return f"{self.protocol}://{self.url}/{self.uri}?{self.params} "
        
    
    def setParams(self,*args,**kwargs):
        a=''
        if args:
            for i in args:
                a = [k + '=' + str(v) + '&' for k,v in i.items()]
        if kwargs:
            a = [k + '=' + str(v) + '&' for k,v in kwargs.items()]
            
        self.iam.params += ''.join(a).rstrip('&')
    
    def setData(self,dictionary):
        try:
            type(dictionary)==dict()
        except:
            raise Exception("딕셔너리 형태로 입력해주세요")
        if not self.iam.data:
            self.iam.data = dictionary
        else:
            for k,v in dictionary.items():
                self.iam.data["k"] = v
    
    def setHeader(self,dictionary):
        try:
            type(dictionary)==dict()
        except:
            raise Exception("딕셔너리 형태로 입력해주세요")
        if not self.iam.header:
            self.iam.header = dictionary
        else:
            for k,v in dictionary.items():
                self.iam.header["k"] = v
        
    def get(self):
        url = self.iam 
        print(url)
        print(url.header)
        return requests.get(self(),headers=url.header)
        
# url = Urlizer("http://waitinghow.honeycombpizza.link/shops/test")
# url = Urlizer("https://www.developers.koscom.co.kr/v2/market/multiquote/stocks/005930/lists")
# params = {
#     'shop_name':'italy',
#     'page':'1',
#     'perPage':'5'
#     }
# datas ={
# }
# headers = {
#     'Content-Type':'applications/json; charset=utf-8'
# }
# url.setHeader(headers)
# url.setData(datas)
# # url.setParams(params)
# results = url.get()
# print(results)
headers = {
    "Content-Type":"text/plain; charset=utf-8"
}
result = requests.get("https://svnweb.freebsd.org/csrg/share/dict/words?views=co",headers=headers).content
print(result)

# from bs4 import BeautifulSoup

# url = 'https://waitingtest.honeycombpizza.link/'

# headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get(url,headers=headers)

# soup = BeautifulSoup(data.text, 'html.parser')
# title=soup.select_one('meta[property="og:title"]')
# print(soup,title)
