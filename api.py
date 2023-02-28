import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru"

    def get_api_key(self, email: str, password: str = "") -> json:
        headers = {'email': email,
                   'password': password
        }
        res = requests.get(self.base_url+"/api/key", headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+"/api/pets", headers=headers, params = filter)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        #Метод отправляет на сервер данные о добовляемом питомце и возрвращает статус запроса и результат в формате JSON с данными питомца
        data = MultipartEncoder(
            fields = {
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo,"rb"),"image/jpg")
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + '/api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        print(result)
        return status, result

    def add_photo_of_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        #Метод отправляет на сервер фото питомца и возрвращает статус запроса и результат в формате JSON с данными питомца
        data = MultipartEncoder(
            fields={'pet_photo':(pet_photo, open(pet_photo, 'rb'), "images/jpg")
            })
        headers = {'auth_key': auth_key["key"], 'Content-Type': data.content_type}
        res = requests.post(self.base_url+'/apo/pets/set_photo/'+pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        print(result)
        return status,result

    def deletle_pet(self, auth_key: json, pet_id: str) -> json:
        #Метод отправляет на сервер запрос на удаление питомца по указанному ID и возрвращает статус запроса и результат в формате JSON с данными питомца
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url+'/api/pets/'+pet_id, headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def update_info_about_pet(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: int) -> json:
        #Метод отправляет на сервер запрос об обновлении данных питомца по указанному ID
        #и возвращает статус запроса и результат в формате JSON с обновленными данными питомца
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        res = requests.put(self.base_url +"/api/pets/"+pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def create_pet_simple(self, auth_key: json, name: str, animal_type: str, age: int) -> json:
        #Метод отправляет (постит) на сервер о добавлении данных о новом питомце без фото и возвращает
        # статус запроса на сервер и результат в формате JSON с данными добавленного питомца без фото
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }
        res = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result