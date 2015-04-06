import re

import requests

from scrapers.models.dog import Dog


#Small reverse engineering of the pet finder api
class PetFinderApi():

    def __init__(self, zip_code):
        self.zip_code = zip_code

    @staticmethod
    def _get_api_key():
        response = requests.get('https://www.petfinder.com/wp-content/themes/petfinder2013/js/build/main.min.js')

        regex = r'prototype.API_KEY="([^"]+)"'
        match = re.search(regex, response.text)

        api_key = match.group(1)

        return api_key

    def _get_dog_list(self, api_key):
        url = 'https://www.petfinder.com/v1/pets/search.json'

        payload = {'query': ('{{"age": ["Baby", "Young"],'
                             '"animal": "Dog",'
                             '"gender": ["female"],'
                             '"location": "{}",'
                             '"lat": "37.6698",'
                             '"lon": "-97.2806",'
                             '"page_number": "0",'
                             '"page_size": "35",'
                             '"status": "Adoptable",'
                             '"sort": "geodist() asc, id desc"}}'.format(self.zip_code)),
                   'api_key': api_key}
        response = requests.post(url, data=payload)
        return response.json()

    def find_dog_items(self):
        api_key = PetFinderApi._get_api_key()

        dog_list = self._get_dog_list(api_key)

        dog_items = PetFinderApi._parse_dog_list(dog_list)

        return dog_items

    @staticmethod
    def _parse_dog_list(dog_list):
        dog_items = []
        for dog in dog_list['results']:
            dog_items.append(PetFinderApi._parse_dog(dog))

        return dog_items

    @staticmethod
    def _parse_dog(data):
        item = Dog()

        item['url'] = ["https://www.petfinder.com/petdetail/{}/".format(data['id'])]

        name = data['name']
        item['name'] = name

        breed = data['primary_breed']
        item['breed'] = breed

        age = data['age']
        item['age'] = age

        size = data['size']
        item['size'] = size

        desc = data['description']
        item['desc'] = desc

        img = "https://drpem3xzef3kf.cloudfront.net{}".format(data['pet_photo'][0])
        item['img'] = img

        agency = data['shelter_name']
        item['agency'] = agency

        return item
