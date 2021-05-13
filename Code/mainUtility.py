import initialize
import jsonHelper


def jsonGet(url):
    data = initialize.get_request(url)
    obj = jsonHelper.byteToJson(data)

    return obj