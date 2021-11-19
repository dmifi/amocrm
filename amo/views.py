import requests

from django.http import HttpResponse

from .utils import refresh_access_token, update_phone, create_user, \
    create_lead, update_email
from local_settings import *


def find_or_create_contact(request):
    """
    Принимает GET запрос с обязательными параметрами: name, email, phone.
    Используя эти данные, ищем контакт в AmoCRM с данной почтой и(или) телефоном.
    Если такого нет, создаем новый, заполнив имя, телефон и почту.
    Если найден, обновляем его входящими данными.
    После этого, создем сделку по данному контакту в первом статусе воронки.
    """
    name = request.GET.get("name", "")
    first_name = ' '.join(name.split()[1:])
    last_name = name.split()[0]
    email = request.GET.get("email", "")
    phone = request.GET.get("phone", "")
    url = f'https://{SUBDOMAIN}.amocrm.ru/api/v3/contacts'
    headers = {
        "Authorization": f'Bearer {ACCESS_TOKEN}'
    }

    params = {'filter[687345]': email}  # "field_id": Email - 687345
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 401:
        refresh_access_token(request)
        response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        # Контакт найден - обновляем поле phone через id
        user_id = response.json()['_embedded']['contacts'][0]['id']
        response = update_phone(request, user_id, name, first_name, last_name,
                                phone)
        response = create_lead(request, user_id)

    elif response.status_code == 204:
        params = {'filter[687293]': phone}  # "field_id": Телефон - 687293
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            user_id = response.json()['_embedded']['contacts'][0]['id']
            # Контакт найден - обновляем поле email через id
            response = update_email(request, user_id, name, first_name,
                                    last_name, email)
            response = create_lead(request, user_id)

        elif response.status_code == 204:
            # Контакт не найден - добавляем новый контакт
            response = create_user(request, name, first_name, last_name, email,
                                   phone)
            user_id = response.json()['_embedded']['contacts'][0]['id']
            response = create_lead(request, user_id)

    return HttpResponse(status=200)


def get_access_and_refresh_tokens(request):
    """
    Обмен authorization_code на access_token и refresh_token.
    Используется при первом запуске. Только при DEBUG=True.
    """
    post_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": CODE,
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post(URL, data=post_data)
    print(response)
    content = response.text
    with open(settings.BASE_DIR / 'answer.json', 'w') as f:
        f.write(content)
    return HttpResponse(status=200, data='OK')
