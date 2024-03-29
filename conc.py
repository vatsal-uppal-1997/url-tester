#!/usr/bin/python3
import sys
import requests
import urllib3
import concurrent.futures
from urllib.parse import urlparse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

valid_status_codes = [200,201,202,203,204,205,206,
                      300,301,302,303,304,307,308]
can_open = []
cannot_open = []
followRedirects = False

def open_url(url, scheme="https", calledAgain=False):
    if url == None or url == "":
        return
    url = url.lower()
    parse = urlparse(url, scheme)
    url = parse._replace(scheme=scheme).geturl()
    error = False
    try:
        response = requests.get(url.lower(), headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}, verify=False, allow_redirects=followRedirects, timeout=60)
        if (response.text != None and response.text != "") or response.status_code in valid_status_codes:
            if scheme == "http":
                print(f"{response.url} http version is accessible")
            else:
                print(f"{response.url} is accessible")
            return
        else:
            if scheme == "http":
                print(f"\t{url} is not accessible")
                return
            else:
                print(f"\t{url} is not accessible --- Trying with http again")
            error = True
    except:
        if scheme == "http":
            print(f"\t{url} is not accessible")
            return
        else:
            print(f"\t{url} is not accessible --- Trying with http again")
        error = True
    time.sleep(2)
    if calledAgain:
        cannot_open.append(response.url)
    elif error:
        open_url(url, "http", True)


if __name__ == "__main__":
    args = sys.argv[1:]
    inputFile = args[0]
    canFname = args[1]
    cannotFname = args[2]
    workers = int(args[3])
    if len(args) == 5:
        followRedirects = bool(args[4])
    urls = None
    if inputFile == "stdin":
        fname = sys.stdin
        urls = fname.read().split("\n")
    else:
        with open(inputFile, encoding="utf-8", errors="ignore") as data:
            urls = data.read().split("\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(open_url, urls)

    with open(canFname, 'w') as f:
        for item in can_open:
            f.write(f"{item}\n")
    with open(cannotFname, 'w') as f:
        for item in cannot_open:
            f.write(f"{item}\n")
