import requests


def pasteEE(key, data, description, expire):
    values = {"key": key,
              "description": description,
              "paste": data,
              "expiration": expire,
              "format": "json"}
    result = requests.post(url="http://paste.ee/api", data=values, timeout=5)
    if result:
        jsonResult = result.json()
        if jsonResult["status"] == "success":
            return jsonResult["paste"]["link"]
        elif jsonResult["status"] == "error":
            return "An error occurred while posting to Paste.ee, code: {}, reason: {}".format(jsonResult["errorcode"],
                                                                                              jsonResult["error"])
