import requests
import json
from django.conf import settings


class VideoAdsFactory(object):
    @classmethod
    def create(cls, service_name, token):
        if service_name == 'tapsell':
            return TapSell(token)

        if service_name == 'tapligh':
            return Tapligh(token)


class TapSell:
    def __init__(self, suggestion_id):
        self.suggestion_id = suggestion_id
        self.url = settings.TAP_SELL_URL

    def run(self):
        payload = "{\n\t\"suggestionId\": \"%s\"\n}" % self.suggestion_id
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", self.url, data=payload, headers=headers)

        result = json.loads(response.text)
        return result['valid']


class Tapligh:
    def __init__(self, token):
        self.token = token
        self.url = settings.TAPLIGH_URL

    def run(self):
        payload = "{\n\t\"token\":\"%s\", \n\t\"packageName\":\"%s\", \n\t\"sdkVersion\":\"%s\", " \
                  "\n\t\"verifyToken\":\"%s\"\n}" % (
                      settings.TAPLIGH_VERIFY_TOKEN,
                      settings.TAPLIGH_SDK_VERSION,
                      settings.TAPLIGH_SDK_VERSION,
                      self.token
                  )
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
        }

        response = requests.request("POST", self.url, data=payload, headers=headers)

        result = json.loads(response.text)

        if result['responseCode'] == 200:
            return True

        else:
            return False
