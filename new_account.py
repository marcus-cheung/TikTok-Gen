import random
from string import ascii_uppercase, ascii_lowercase, digits

AUTHORIZE_URL = "https://www.tiktok.com/v2/auth/authorize/"
CLIENT_KEY = "awy0h1wmzdpncvdi"
SERVER_ENDPOINT_REDIRECT = "https://marcus-cheung.github.io/monty-mole/auth/callback/"


def login():
    csrf_state = "".join(
        random.choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(16)
    )
    url = AUTHORIZE_URL
    url += f"?client_key={CLIENT_KEY}"
    url += "&scope=user.info.basic"
    url += "&response_type=code"
    url += f"&redirect_uri={SERVER_ENDPOINT_REDIRECT}"
    url += "&state=" + csrf_state

    print(url)

    username = input("Username?")
    callback_url = input("Callback:")


login()
