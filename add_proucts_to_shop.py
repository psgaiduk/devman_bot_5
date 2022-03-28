from moltin import Moltin
from dotenv import load_dotenv
import os
import json


def main():

    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

    if os.path.exists(dotenv_path):

        load_dotenv(dotenv_path)

    moltin_client_id = os.getenv('MOLTIN_CLIENT_ID')

    moltin_client_secret = os.getenv('MOLTIN_CLIENT_SECRET')

    moltin = Moltin(secret_code=moltin_client_secret, client_id=moltin_client_id)

    menu_path = os.path.join(os.path.dirname(__file__), 'pizzeria', 'menu.json')

    with open(menu_path) as file_menu:

        menu = json.load(file_menu)

        for item in menu:

            name = item['name']

            description = f'{item["description"]}\n\n' \
                          f'Жиры: {item["food_value"]["fats"]}\n' \
                          f'Белки: {item["food_value"]["proteins"]}\n' \
                          f'Углеводы: {item["food_value"]["carbohydrates"]}\n' \
                          f'Энергетическая ценность: {item["food_value"]["kiloCalories"]} ККал\n\n' \
                          f'Вес: {item["food_value"]["weight"]} грамм'

            price = item['price']

            image_link = item['product_image']['url']

            moltin.add_product(name=name, description=description, price=price, image=image_link)

    with open(os.path.join(os.path.dirname(__file__), 'pizzeria', 'addresses.json'), encoding='utf-8') as file:

        addresses = json.load(file)

        for address in addresses:
            moltin.create_entry_in_flows('pizzeria', {
                'address': address['address']['full'],
                'alias': address['alias'],
                'Longitude': address['coordinates']['lat'],
                'Latitude': address['coordinates']['lat']})


if __name__ == '__main__':
    main()
