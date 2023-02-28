from api import PetFriends
from settings import my_email, my_password, ne_my_email, ne_my_password
import os

pf = PetFriends()


def test_get_api_key_for_my_user(email=my_email, password=my_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_list_of_pets_with_key(filter=''):
    _, auth_key = pf.get_api_key(my_email, my_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet(name="Кошкан", animal_type="Cat", age='2', pet_photo="images/cat1.jpg"):
    # проверяем что можно добавить питомца с корректными данными
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    _, auth_key = pf.get_api_key(my_email, my_password)
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Добавляем питомца
    assert status == 200
    assert result['name'] == name
    # Сверяем полученный ответ с ожидаемым результатом


def test_deletle_self_pet():
    # Проверка возможности удаления питомца
    # Получаем ключ и список всех своих питомцев
    _, auth_key = pf.get_api_key(my_email, my_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список своих питомцев пустой, то добовляем ногового и опять запращиваем список
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "КИТ", "Cat", "2", 'images/cat2.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Берем id первого питомца и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.deletle_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_info_about_pet(name="Кошкан", animal_type="Cat", age='2'):
    # Проверяем возможность обвновления информации о питомце
    # Получаем ключ и список всех своих питомцев
    _, auth_key = pf.get_api_key(my_email, my_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список ну пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_info_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('There is not my pets')


def test_add_new_pet_without_photo(name="Кошкан", animal_type="Cat", age='5'):
    # Проверяем что можно добавить питомца с корректными данными
    _, auth_key = pf.get_api_key(my_email, my_password)
    # Запрашиваем ключ  и сохраняем в переменую auth_key
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    # Добавляем питомца
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_more_four_words_in_breed(name="KOSHKAN", age="3", pet_photo="images/cat1.jpg"):
    # Проверка с негативным сценарием
    # Проверяем что добовление питомца с породой более чем из четырёх слов не будет пройдена
    animal_type = "кот кот кот кот кот"
    _, api_key = pf.get_api_key(my_email, my_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    list_animal_type = result['animal_type'].split()
    word_count = len(list_animal_type)
    assert status == 200
    assert word_count < 4, 'Питомец добавлен с названием породы более чем из 4 слов'


def test_get_key_with_wrong_pass(email=my_email, password=ne_my_password):
    # Проверка запроса с неправильным паролем
    status, result = pf.get_api_key(email, password)
    assert status == 403
    # Проверяем нет ои ключа в ответе
    assert "key" not in result


def test_get_key_with_wrong_email(email=ne_my_email, password=my_password):
    # Проверка запроса с неправильной почтой
    status, result = pf.get_api_key(email, password)
    assert status == 403
    # Проверяем нет ли ключа в ответе
    assert "key" not in result


def test_get_key_with_wrong_email_and_password(email= ne_my_email, password = ne_my_password):
    #Проверка запроса с непроавильной почтой и паролем
    status, result = pf.get_api_key(email, password)
    assert  status == 403
    #Проверяем нет ли ключа в ответе
    assert "key" not in result


def test_add_pet_with_negative_age(name="Kowka", animal_type="cat", age="-5", pet_photo="images/cat2.jpg"):
    # Проверка с негативным сценарием
    # Тест не будет пройден с отрицательным возрастом
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, api_key = pf.get_api_key(my_email, my_password)
    _, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    assert age not in result['age']


def test_add_pet_empty_name (name = "", animal_type = "cat", age = "5", pet_photo = "images/cat1.jpg"):
    #Проверка с негативным сценарием
    #Проверка добовления питомца с пустым значением в переменной name
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, api_key = pf.get_api_key(my_email, my_password)
    _, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] != '', "Питомец добавлен с пустым значением в переменной name"


def test_add_pet_with_three_digit_age_number(name='KOWKA', animal_type='cat', age='100', pet_photo='images/Cat1.jpg'):
    #Проверка с негативным сценарием
    #Добавление питомца с числом более трех знаков в переменной age
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, api_key = pf.get_api_key(my_email, my_password)
    _, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    number = result['age']
    assert len(number) < 3, 'Питомец добавлен на сайт с числом привышающим 2 знака в поле возраст'


def test_add_pet_with_a_lot_of_words_in_name(animal_type='cat', age='2', pet_photo='images/Cat1.jpg'):
    #Проверка с негативным сценарием
    #Добавления питомца имя которого превышает 10 слов
    name = 'Кот Кот Кошка Кошка Кот'
    _, api_key = pf.get_api_key(my_email, my_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    list_name = result['name'].split()
    word_count = len(list_name)
    assert status == 200
    assert word_count < 4, 'Питомец добавлен с именем больше 4 слов'


def test_add_pet_in_name_digit(name = "123123123", animal_type = "cat", age = "1", pet_photo = "images/cat2.jpg"):
    #Проверка с негативным сценарием
    #Добовления питомца с именем из цифр
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, api_key = pf.get_api_key(my_email, my_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert name not in result['name'], 'Питомец добавлен с цифрами вместо букв в поле name'


def test_add_pet_in_animal_type_digit(name="Kowka", animal_type = "123123123", age = "1", pet_photo = "images/cat1.jpg"):
    #Проверка с негативным сценарием
    #Добовления питомца с породой из цифр
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, api_key = pf.get_api_key(my_email, my_password)
    satatus, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert animal_type not in result['animal_type'], 'Питомец добавлен с цифрами в поле animal_type'