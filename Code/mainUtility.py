import initialize
import jsonHelper
from logger import logger


def jsonGet(url):
    # perform get request
    data = initialize.get_request(url)
    # transform bytes to json object
    obj, data = jsonHelper.byteToJson(data)

    # logging the action for later problem solving (if br0k3n)
    logger("resp-API request: /dataservice/" + url)

    # return both objects
    return obj, data
