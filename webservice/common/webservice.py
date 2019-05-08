from suds.client import Client
from common.LogTools import LogTools


class WebService:

    def __init__(self):
        self.log = LogTools(__name__)


    def web_service(self, url, params):
        self.log.mylog.debug("测试地址是{}".format(url))
        self.log.mylog.debug("测试参数是{}".format(params))
        if type(params) is str:
            params = eval(params)
        client = Client(url)
        result = client.service.sendMCode(params)
        self.log.mylog.debug("响应信息是{}".format(result))
        return result


if __name__ == '__main__':
    url = "http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl"
    params = {"client_ip": "192.168.1.13", "tmpl_id": "1", "mobile": "18826587147"}
    res = WebService().web_service(url, params)
    print(res)
