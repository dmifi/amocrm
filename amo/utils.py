import requests

from django.conf import settings

from local_settings import *


def refresh_access_token(request):
    """Обновляем access_token по истечении срока действия"""
    post_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post(URL, data=post_data)
    content = response.text
    with open(settings.BASE_DIR / 'answer.json', 'w') as f:
        f.write(content)


def update_email(request, user_id, name, first_name, last_name, email):
    """ Обновляем поле 'Email' контакта"""
    url = f'https://{SUBDOMAIN}.amocrm.ru/api/v4/contacts/{user_id}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    params = {
        'name': name,
        'first_name': first_name,
        'last_name': last_name,
        'custom_fields_values': [
            {
                "field_id": 687345,
                "field_name": "Email",
                "values": [
                    {
                        "value": email,
                    }
                ]
            }
        ]
    }
    response = requests.patch(url, headers=headers, json=params)
    return response


def update_phone(request, user_id, name, first_name, last_name, phone):
    """ Обновляем поле 'Телефон' контакта"""
    url = f'https://{SUBDOMAIN}.amocrm.ru/api/v4/contacts/{user_id}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    params = {
        'name': name,
        'first_name': first_name,
        'last_name': last_name,
        'custom_fields_values': [
            {
                "field_id": 687293,
                "field_name": "Телефон",
                "values": [
                    {
                        "value": phone,
                    }
                ]
            }
        ]
    }
    response = requests.patch(url, headers=headers, json=params)
    return response


def create_user(request, name, first_name, last_name, email, phone):
    """ Создаем контакт """
    url = f'https://{SUBDOMAIN}.amocrm.ru/api/v4/contacts'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    params = [{
        'name': name,
        'first_name': first_name,
        'last_name': last_name,
        'custom_fields_values': [
            {
                "field_id": 687293,
                "field_name": "Телефон",
                "values": [
                    {
                        "value": phone,
                    }
                ]
            },
            {
                "field_id": 687345,
                "field_name": "Email",
                "values": [
                    {
                        "value": email,
                    }
                ]
            },
        ]
    }]
    response = requests.post(url, headers=headers, json=params)
    return response


def create_lead(request, user_id):
    """ Создаем сделку прикрепив к ней контакт user_id"""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    data = [
        {
            "created_by": 0,
            "_embedded": {
                "contacts": [
                    {
                        "id": user_id
                    }
                ]
            }
        }
    ]
    url = f'https://{SUBDOMAIN}.amocrm.ru/api/v4/leads'
    response = requests.post(url, headers=headers, json=data)
    return response
