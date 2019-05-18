import warnings
from suds.client import Client
from suds import WebFault
from common.LogTools import LogTools
from common.ConfTools import DoConf
from common import constant


class WebService:
    log = LogTools(__name__)
    cf = DoConf(constant.globe_conf_dir)

    def web_services(self, url, params, method):
        url = "http://" + self.cf.get_value("dev_info", "domain_name") + ":" + self.cf.get_value("dev_info",
                                                                                                 "port") + url
        self.log.mylog.debug("测试地址是{}".format(url))
        self.log.mylog.debug("测试参数是{}".format(params))
        if type(params) is str:
            params = eval(params)
        client = Client(url)
        try:
            result = eval("client.service.{0}({1})".format(method, params))
            self.log.mylog.debug("响应信息是{}".format(result))
            msg = result.retInfo
        except WebFault as e:
            msg = e.fault.faultstring
            warnings.simplefilter('ignore', ResourceWarning)
            self.log.mylog.debug("响应信息是{}".format(e))
        return msg


if __name__ == '__main__':
    url = "/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl"
    params = {'verify_code': '414637', 'user_id': None, 'channel_id': '1', 'pwd': '123456', 'mobile': '18826587147',
              'ip': '192.168.1.13'}
    res = WebService().web_services(url, params, "userRegister")
