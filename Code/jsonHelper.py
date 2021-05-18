import json


# convert the bytes to a json object
def byteToJson(byte):

    # remove unwanted chars
    jsonObj = byte.decode('utf8').replace("'", '"')

    # load the json object to a list and dump it as formatted json
    data = json.loads(jsonObj)
    s = json.dumps(data, indent=4, sort_keys=True)

    return s, data


# build the main payload as a json object
def payloadBuilderReboot(hostname, ip, uuid):

    # pack the dynamic values to a variable
    payload = {
        "action": "reboot",
        "deviceType": hostname,
        "devices": [
            {
                "deviceIP": ip,
                "deviceId": uuid
            }
        ]
    }

    # turn the variable to a json object and then return it
    payload = json.dumps(payload)

    return payload
