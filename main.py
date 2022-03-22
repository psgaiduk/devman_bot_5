import json
import os

addresses_path = os.path.join(os.path.dirname(__file__), 'pizzeria', 'addresses.json')
menu_path = os.path.join(os.path.dirname(__file__), 'pizzeria', 'menu.json')

with open(addresses_path) as file_addresses:
    addresses = json.load(file_addresses)
    print(addresses)


with open(menu_path) as file_menu:
    menu = json.load(file_menu)
    print(menu)