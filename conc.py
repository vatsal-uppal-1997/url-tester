#!/usr/bin/python3
import sys
import requests
import urllib3
import concurrent.futures
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

valid_status_codes = [200,201,202,203,204,205,206,
                      300,301,302,303,304,307,308]
can_open = []
cannot_open = []

def open_url(url):
    if url == None or url == "":
        return
    try:
        response = requests.head(url.lower(), headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1"}, timeout=60, verify=False, allow_redirects=False)
        if response.status_code in valid_status_codes:
            print(f"{url} is accessible")
            can_open.append(url)
        else:
            print(f"{url} is not accessible")
            cannot_open.append(url)
    except:
        cannot_open.append(url)

if __name__ == "__main__":
    args = sys.argv[1:]
    inputFile = args[0]
    canFname = args[1]
    cannotFname = args[2]
    urls = None
    if inputFile == "stdin":
        fname = sys.stdin
        urls = fname.read().split("\n")
    else:
        with open(inputFile, encoding="utf-8", errors="ignore") as data:
            urls = data.read().split("\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(open_url, urls)

    with open(canFname, 'w') as f:
        for item in can_open:
            f.write(f"{item}\n")
    with open(cannotFname, 'w') as f:
        for item in cannot_open:
            f.write(f"{item}\n")
