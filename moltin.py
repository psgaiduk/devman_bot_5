import time
from requests import Session
import logging
from utils import transliterate_text
from typing import Dict
from dotenv import load_dotenv
import os
import json

logger = logging.getLogger('app_logger')
logging.basicConfig(level=logging.DEBUG)


class Moltin:

    def __init__(self, client_id, secret_code):
        self.client_id = client_id
        self.secret_code = secret_code
        self.url = 'https://api.moltin.com/v2/'
        self.time_get_header = None
        self.time_token_expires = None
        self._session = Session()
        self.timeout = 5
        self.header = self.get_header()

    def get_header(self) -> Dict[str, str]:
        """
        Function for get header. If time token not expires, then return current header, else get new token, update
        header and return it.
        :return: header
        """

        if self.time_get_header:

            time_passed_since_get_token = time.time() - self.time_get_header

            if time_passed_since_get_token < self.time_token_expires:
                return self.header

        logger.debug('start get header')

        url = 'https://api.moltin.com/oauth/access_token'

        data = {'client_id': self.client_id, 'client_secret': self.secret_code, 'grant_type': 'client_credentials'}

        logger.debug(f'data for get token\nurl = {url}\ndata = {data}')

        response = self._session.post(url=url, data=data, timeout=self.timeout)

        logger.debug(f'get data token\n{response}')

        response.raise_for_status()

        moltin_token = response.json()

        logger.debug(f'dict with token\n{response}')

        access_token = moltin_token['access_token']

        header = {'authorization': f'Bearer {access_token}'}

        logger.debug(f'return header = {header}')

        self.time_token_expires = moltin_token['expires_in']

        self.time_get_header = time.time()

        self.header = header

        return header

    def add_product(self, name: str, description: str, price: int, image: str) -> None:

        """
        Function for add new product in moltin.
        :param name: name of pizza
        :param description: description of pizza
        :param price: price
        :param image: link to image with pizza
        :return:
        """

        logger.info(f'Start work add products\n'
                    f'name = {name}\n'
                    f'description = {description}\n'
                    f'price = {price}\n'
                    f'image = {image}')

        url = f'{self.url}products'

        logger.debug(f'create url = {url}')

        data = {
            "data": {
                "type": "product",
                "name": name,
                "slug": transliterate_text(name),
                "sku": transliterate_text(name),
                "description": description,
                "manage_stock": False,
                "price": [
                    {
                        "amount": price,
                        "currency": "RUB",
                        "includes_tax": True
                    }
                ],
                "status": "live",
                "commodity_type": "physical"
            }
        }

        response = self._session.post(url, headers=self.get_header(), json=data)

        response.raise_for_status()

        new_product = response.json()

        product_id = new_product['data']['id']

        image_id = self.add_image_in_shop(link=image)

        self.add_image_for_product(product_id=product_id, image_id=image_id)

        logger.debug(f'Create a new product\n{new_product}\n{product_id}\n{image_id}')

    def add_image_in_shop(self, link: str) -> str:

        """
        Function add new image in the shop and return image id.
        :param link: link to image
        :return: image id
        """

        logger.info(f'Start work add file in shop\n'
                    f'link = {link}\n')

        response = self._session.post(
            self.url + 'files',
            headers=self.get_header(),
            files={'file_location': (None, link)})

        response.raise_for_status()

        new_image = response.json()

        logger.debug(f'create new file\n new_image = {new_image}')

        return new_image['data']['id']

    def add_image_for_product(self, product_id: str, image_id: str) -> None:

        """
        Function for add image for product
        :param product_id:
        :param image_id:
        :return:
        """

        logger.info(f'Start work add image for product\n'
                    f'product_id = {product_id}\n'
                    f'image_id = {image_id}\n')

        json_data = {
            'data': {
                'type': 'main_image',
                'id': image_id,
            },
        }

        response = self._session.post(
            self.url + f'/products/{product_id}/relationships/main-image',
            headers=self.get_header(),
            json=json_data)

        response.raise_for_status()

    def get_flow_slug(self, name: str) -> str:
        """
        Method return id flow by name flow
        :param name:
        :return:
        """

        logger.info(f'Start work add image for product\nname = {name}\n')

        response = self._session.get(self.url + '/flows/', headers=self.get_header())

        logger.debug(f'get all flows\n'
                     f'response = {response.json()}\n')

        for flow in response.json()['data']:

            if flow['name'] == name:

                logger.debug(f'Get need flow\n'
                             f'flow = {flow}\n')

                return flow['slug']

    def create_flow(self, name: str, description: str) -> None:
        """
        Method create flow in shop
        :param name:
        :param description:
        :return:
        """

        logger.info(f'Start work create flow\nname = {name}\ndescription = {description}')

        json_data = {
            'data': {
                'type': 'flow',
                'name': name,
                'slug': transliterate_text(name),
                'description': description,
                'enabled': True,
            },
        }

        response = self._session.post(self.url + '/flows/', headers=self.get_header(), json=json_data)

        logger.debug(f'Create flow\nresponse = {response.json()}\n')

    def create_entry_in_flows(self, slug: str, values: dict):

        logger.info(f'Start work create flow\nslug = {slug}\nvalues = {values}')

        json_data = {
            'data': {
                'type': 'entry',
            },
        }

        for key, value in values.items():
            json_data['data'][key] = value

        response = self._session.post(self.url + f'/flows/{slug}/entries', headers=self.get_header(), json=json_data)

        logger.debug(f'Create flow\nresponse = {response.json()}\n')