import re
import requests


def fetchURL(url, params=None, extraHeaders=None):
    headers = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en-us,en;q=0.5"}
    if extraHeaders:
        headers.update(extraHeaders)
    try:
        request = requests.get(url, params=params, headers=headers, timeout=5)
        pageType = request.headers["content-type"]
        if not re.match("^(text/.*|application/((rss|atom|rdf)\+)?xml(;.*)?|application/(.*)json(;.*)?)$", pageType):
            # Make sure we don't download any unwanted things
            return None
        return request
    except:
        return None


def postURL(url, data, extraHeaders=None):
    headers = {"User-Agent": "Mozilla/5.0"}
    if extraHeaders:
        headers.update(extraHeaders)
    try:
        request = requests.post(url, data=data, headers=headers, timeout=5)
        pageType = request.headers["content-type"]
        if not re.match("^(text/.*|application/((rss|atom|rdf)\+)?xml(;.*)?|application/(.*)json(;.*)?)$", pageType):
            # Make sure we don't download any unwanted things
            return None
        return request
    except:
        return None


def pasteEE(key, data, description, expire):
    values = {"key": key,
              "description": description,
              "paste": data,
              "expiration": expire,
              "format": "json"}
    result = postURL("http://paste.ee/api", values)
    if result:
        jsonResult = result.json()
        if jsonResult["status"] == "success":
            return jsonResult["paste"]["link"]
        elif jsonResult["status"] == "error":
            return "An error occurred while posting to Paste.ee, code: {}, reason: {}".format(jsonResult["errorcode"],
                                                                                              jsonResult["error"])
