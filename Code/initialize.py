import json
import requests
import sensitiveData as sd

session = {}
sdWanUrl = sd.vmanage_ip
username = sd.username
password = sd.password


# Credits: https://github.com/CiscoDevNet/Getting-started-with-Cisco-SD-WAN-REST-APIs/
class Authentication:

    @staticmethod
    def get_jsessionid(sdWanUrl, username, password):
        api = "/j_security_check"
        base_url = "https://%s" % (sdWanUrl)
        url = base_url + api
        payload = {'j_username': username, 'j_password': password}

        response = requests.post(url=url, data=payload, verify=True)
        try:
            cookies = response.headers["Set-Cookie"]
            jsessionid = cookies.split(";")
            return (jsessionid[0])
        except:
            print("No valid JSESSION ID returned\n")
            exit()

    @staticmethod
    def get_token(sdWanUrl, jsessionid):
        headers = {'Cookie': jsessionid}
        base_url = "https://%s" % (sdWanUrl)
        api = "/dataservice/client/token"
        url = base_url + api
        response = requests.get(url=url, headers=headers, verify=True)
        if response.status_code == 200:
            return (response.text)
        else:
            return None


Auth = Authentication()
jsessionid = Auth.get_jsessionid(sdWanUrl, username, password)
token = Auth.get_token(sdWanUrl, jsessionid)

if token is not None:
    header = {'Content-Type': "application/json", 'Cookie': jsessionid, 'X-XSRF-TOKEN': token}
else:
    header = {'Content-Type': "application/json", 'Cookie': jsessionid}

base_url = "https://%s/dataservice/" % (sdWanUrl)


def get_request(request):

    print(header)
    url = base_url + request
    response = requests.get(url, headers=header, verify=True)
    #data = response.content

    if response.status_code == 200:
        data = response.json()['data']
    else:
        data = "get failed"

    return data


def post_request(request, payload):

    url = base_url + request
    payload = json.dumps(payload)
    print(payload)

    response = requests.post(url=url, data=payload, headers=header, verify=True)

    if response.status_code == 200:
        response = "post worked"
    else:
        response = "post failed"

    return response