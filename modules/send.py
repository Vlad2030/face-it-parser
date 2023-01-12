import requests
import json

def friendRequest(token, facitIdSending, facitIdReceiving, proxy=None):
    if proxy == None:
        r = requests.post(
            f"https://api.faceit.com/friend-requests/v1/" \
                f"users/{facitIdSending}/requests",
            headers={
                "authorization": token
            },
            json={
                "users": [str(facitIdReceiving)],
                "conversionPoint": "profile"
            },
        )
    else:
        proxies = {"https": proxy}
        r = requests.post(
            f"https://api.faceit.com/friend-requests/v1/" \
            f"users/{facitIdSending}/requests",
            proxies=proxies,
            headers={
                "authorization": token
            },
            json={
                "users": [str(facitIdReceiving)],
                "conversionPoint": "profile"
            },
        )