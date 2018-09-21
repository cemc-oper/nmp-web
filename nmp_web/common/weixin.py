# coding=utf-8
import requests

from nmp_web.common import save_weixin_access_token_to_cache, get_weixin_access_token_from_cache

REQUEST_POST_TIME_OUT = 60


class Auth(object):
    def __init__(self, config: dict):
        """
        :param config:
            {
                "name": "TokenConfig",
                "type": "record",
                "fields": [
                    {"name": "corp_id", type: "string"},
                    {"name": "corp_secret", type: "string"},
                    {"name": "url", type: "string"},
                ]
            }
        :return:
        """

        self.corp_id = config['corp_id']
        self.corp_secret = config['corp_secret']
        self.url = config['url']

    def get_access_token_from_server(self) -> dict:
        headers = {'content-type': 'application/json'}
        url = self.url.format(
            corp_id=self.corp_id, corp_secret=self.corp_secret
        )

        token_response = requests.get(
            url,
            verify=False,
            headers=headers,
            timeout=REQUEST_POST_TIME_OUT
        )

        response_json = token_response.json()
        print(response_json)
        if response_json['errcode'] == 0:
            access_token = response_json['access_token']
            save_weixin_access_token_to_cache(access_token)
            result = {
                'status': 'ok',
                'access_token': access_token
            }
        else:
            result = {
                'status': 'error',
                'errcode': response_json['errcode'],
                'errmsg': response_json['errmsg']
            }

        return result

    def get_access_token_from_cache(self) -> str:
        return get_weixin_access_token_from_cache()

    def save_access_token_to_cache(self, access_token: str) -> None:
        return save_weixin_access_token_to_cache(access_token)

    def get_access_token(self) -> str:
        weixin_access_token = get_weixin_access_token_from_cache()
        if weixin_access_token is None:
            self.get_access_token_from_server()
            weixin_access_token = get_weixin_access_token_from_cache()
        return weixin_access_token


class WeixinApp(object):
    def __init__(self, weixin_config: dict):
        self.weixin_config = weixin_config

        self.auth = Auth(self.weixin_config['token'])

    def get_user_info(self, code: str):
        auth = Auth(self.weixin_config['token'])
        weixin_access_token = auth.get_access_token()
        # weixin_access_token = auth.get_access_token_from_server()

        url = "https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token={access_token}&code={code}".format(
            access_token=weixin_access_token,
            code=code
        )

        result = requests.get(
            url,
            verify=False,
            timeout=REQUEST_POST_TIME_OUT
        ).json()

        if 'errcode' in result:
            error_code = result['errcode']
            if error_code == 40014:
                # need refactoring
                weixin_access_token = auth.get_access_token_from_server()['access_token']
                url = "https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token={access_token}&code={code}".format(
                    access_token=weixin_access_token,
                    code=code
                )
                result = requests.get(
                    url,
                    verify=False,
                    timeout=REQUEST_POST_TIME_OUT
                ).json()

        return result
