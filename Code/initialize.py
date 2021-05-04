import json
import requests
import sys
import sensitiveData as sd

session = {}
sdWanUrl = sd.vmanage_ip
username = sd.username
password = sd.password


# TODO: Token auth not working


def login():
    base_url_str = "https://" + sdWanUrl

    login_action = "/j_security_check"

    # Format data for loginForm
    login_data = {"j_username": username, "j_password": password}

    # Url for posting login data
    login_url = base_url_str + login_action
    url = base_url_str + login_url

    sess = requests.session()

    login_response = sess.post(url=login_url, data=login_data, verify=True)

    if b'<html>' in login_response.content:
        print("Login Failed")
        sys.exit(0)

    print(login_response)

    session[sdWanUrl] = sess
    return sess


def get_request(request):
    # login for auth
    sess = login()

    url = "https://" + sdWanUrl + "/dataservice/" + request
    # print url
    response = sess.get(url, verify=False)
    data = response.content
    return data


def post_request(request, payload, headers={'Content-Type': 'application/json'}):
    # login for auth
    login()

    url = "https://" + sdWanUrl + "/dataservice/" + request
    payload = json.dumps(payload)
    print(payload)

    response = session[sdWanUrl].post(url=url, data=payload, headers=headers, verify=False)
    data = response.json()
    return data
