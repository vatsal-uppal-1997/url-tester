#!/usr/bin/python3
import grequests
import requests
import urllib3
import sys
from rx import Observable, Observer
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


'''


CONSTANTS


-----------------------------------------------------------------
'''

valid_status_codes = [200,201,202,203,204,205,206,
                      300,301,302,303,304,307,308]

class UrlObserver(Observer):
    def __init__(self, canFname="canOpen", cannotFname="cannotOpen"):
        self.canOpen = []
        self.cannotOpen = []
        self.canFname = canFname
        self.cannotFname = cannotFname = cannotFname

    def on_next(self, value):
        if value["url"] == "None" or value["url"] == "":
            return
        if value["canOpen"]:
            self.canOpen.append(value["url"])
        else:
            self.cannotOpen.append({"url": value["url"], "err": value["err"]})

    def on_completed(self):
        with open(self.canFname, 'w') as f:
            for item in self.canOpen:
                f.write("%s\n" % item)
        with open(self.cannotFname, 'w') as f:
            for item in self.cannotOpen:
                print(item["url"])
                f.write(f"{item['url']}\t{item['err']}\n")

    def on_error(self, error):
        print("Error Occurred: {0}".format(error))

urlObserver = UrlObserver()
'''


LOGIC


-----------------------------------------------------------------
'''

def handle_err(req, exception):
    out = {"url": req.url, "canOpen": False, "err": exception}
    urlObserver.on_next(out)

def file_observable(fname):
    url_list = None
    if fname == "stdin":
        fname = sys.stdin
        url_list = fname.read().split("\n")
    else:
        with open(fname, encoding="utf8", errors='ignore') as data:
            url_list = data.read().split("\n")
    with requests.Session() as s:
        reqs = (grequests.get(url.lower(), stream=False, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1"}, timeout=60, verify=False, allow_redirects=True, session=s) for url in url_list)
        responses = grequests.map(reqs, size=50, exception_handler=handle_err)
    return responses

def open_urls(response): 
    if response == None:
        return {"url": "None", "canOpen": False}
    try:
        if response.status_code in valid_status_codes:
            out = {"url": response.url, "canOpen": True}
        else:
            out = {"url": response.url, "canOpen": False, "err": response.status_code}
        response.close()
        return out
    except Exception as e:
        out = {"url": response.url, "canOpen": False, "err": e}
        response.close()
        return out

def main():
    args = sys.argv[1:]
    inputFile = args[0]
    urlObserver.canFname = args[1]
    urlObserver.cannotFname = args[2]
    source = (Observable.from_(file_observable(inputFile))
            .map(open_urls))
    source.subscribe(urlObserver)

if __name__ == '__main__':
    main()
