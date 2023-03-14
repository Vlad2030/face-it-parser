import requests


def friendRequest(
    token: str, facitIdSending: str, facitIdReceiving: str, proxy: None
) -> None:
    if proxy:
        proxies_url = {"https": proxy}
        return requests.post(
            url=f"https://api.faceit.com/friend-requests/v1/"
            f"users/{facitIdSending}/requests",
            proxies=proxies_url,
            headers={"authorization": token},
            json={
                "users": [str(facitIdReceiving)],
                "conversionPoint": "profile",
            },
        )
    else:
        return requests.post(
            url=f"https://api.faceit.com/friend-requests/v1/"
            f"users/{facitIdSending}/requests",
            headers={"authorization": token},
            json={
                "users": [str(facitIdReceiving)],
                "conversionPoint": "profile",
            },
        )
