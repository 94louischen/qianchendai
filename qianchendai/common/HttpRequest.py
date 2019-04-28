import requests


class Request:

    def __init__(self):
        self.session = requests.sessions.session()

    def http_request(self, method, url, params, json=None, headers=None, cookies=None):
        if type(params) is str:
            params = eval(params)
        headers = eval(headers)
        method = method.upper()
        if method == "GET":
            resp = self.session.request(method, url, params, json=json, headers=headers, cookies=cookies)
        elif method == "POST":
            if json:
                resp = self.session.request(method, url, json=json, headers=headers, cookies=cookies)
            else:
                resp = self.session.request(method, url, data=params, headers=headers, cookies=cookies)
        else:
            print("暂时不支持的格式")
        return resp

    def close(self):
        self.session.close()


if __name__ == '__main__':
    res = Request()
    method1 = 'get'
    url1 = 'http://test.lemonban.com/futureloan/mvc/api/member/login'
    data = "{'mobilephone':'18826587147','pwd':123456}"
    header = {'content-type': 'application/x-www-form-urlencoded'}
    respon = res.http_request(method1, url1, data, headers=header)
    print(respon.request.headers)
    print(respon.text)
