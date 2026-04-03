import requests


def get_login():

    url = "https://api.linglong.space/auth"
    data= {
        "password":"wyb19970803*",
        "username":"ut003193"

    }

    result = requests.post(url=url,json=data).json()
    token = result['data']['token']

    return token