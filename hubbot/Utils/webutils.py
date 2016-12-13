from __future__ import unicode_literals
import requests


def paste_ee(key, data, description, expire):
    values = {"key": key,
              "description": description,
              "paste": data,
              "expiration": expire,
              "format": "json"}
    result = requests.post("http://paste.ee/api", data=values, timeout=3, headers={"Connection": "close"})
    if result:
        json_result = result.json()
        if json_result["status"] == "success":
            return json_result["paste"]["link"]
        elif json_result["status"] == "error":
            return "An error occurred while posting to Paste.ee, code: {}, reason: {}".format(json_result["errorcode"],
                                                                                              json_result["error"])
