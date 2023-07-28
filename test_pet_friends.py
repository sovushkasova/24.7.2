import requests

from api import PetFriends
from settings import valid_email, valid_password
from settings import invalid_email, invalid_password
import os

pf = PetFriends()

def test_get_api_key_for_user(email=valid_email,password=valid_password):
    status, result = pf.get_api_key(email,password)
    assert status == 200
    assert "key" in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data( name='Бо', animal_type='бульдог',
                                      age='4', pet_photo='images/4V0A7872.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Бо", "бульдог", "4", "images/4V0A7872.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Боб', animal_type='французский бульдог', age=5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_add_new_pet_without_photo( name='Рэй', animal_type='чих',
                                      age='4'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_photo_of_pet(pet_photo='images/rom.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if pet_photo is None:
        pf.add_photo_of_pet(auth_key, "Рэй", "чих", "4")
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_photo_of_pet(auth_key,pet_id, pet_photo)
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        assert status == 200


def test_failed_get_api_key_in(email=invalid_email,password=invalid_password):
    status, result = pf.get_api_key_in(email,password)
    assert status != 200
    assert result
    print("\n" "Пользователь не существует")

def test_failed__get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key_in(invalid_email, invalid_password)
    status, result = pf.get_list_of_pets_in(auth_key, filter)



