import requests
import json
from shopping.models import Store


class FactoryStore(object):
    @classmethod
    def create(cls, shop, purchase_token, product_id, package_name):
        if shop.store.valid_name == 'cafe_bazar':
            return CafeBazar(purchase_token, product_id, package_name)

        if shop.store.valid_name == 'myket':
            return Myket(purchase_token, product_id, package_name)


class CafeBazar(object):
    def __init__(self, purchase_token, product_id, package_name, store=None):
        self.purchase_token = purchase_token
        self.product_id = product_id
        self.package_name = package_name
        self.store = Store.objects.get(valid_name='cafe_bazar')
        self.url = "https://pardakht.cafebazaar.ir/devapi/v2/api/validate/{}/inapp/{}/purchases/{}"\
            .format(self.package_name, self.product_id, self.purchase_token)

    def is_verified(self):

        headers = {
            'content-type': "text;charset=utf-8",
            'authorization': self.store.access_token,
            'cache-control': "no-cache"
        }
        response = requests.request("POST", self.url, headers=headers)

        result = json.loads(response.text)

        if 'consumptionState' in result.keys() and 'purchaseState' in result.keys():

            if result['consumptionState'] == 1 and result['purchaseState'] == 0:
                return True, result

        return False, result


class Myket(object):
    def __init__(self, purchase_token, product_id, package_name):
        self.purchase_token = purchase_token
        self.product_id = product_id
        self.package_name = package_name
        self.store = Store.objects.get(valid_name='myket')
        self.url = "https://developer.myket.ir/api/applications/{}/purchases/products/{}/tokens/{}"\
            .format(self.package_name, self.product_id, self.purchase_token)

    def is_verified(self):

        headers = {
            'x-access-token': self.store.access_token,
            'cache-control': "no-cache"
        }

        response = requests.request("GET", self.url, headers=headers)

        result = json.loads(response.text)

        if 'consumptionState' in result.keys() and 'purchaseState' in result.keys():

            if result['consumptionState'] == 1 and result['purchaseState'] == 0:
                return True, result

        return False, result