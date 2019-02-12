#!/usr/bin/python3
import argparse
import os
import urllib
import requests
from concurrent.futures import ThreadPoolExecutor

# Disable warnings SSL warnings; ideal for sites with bad SSL setup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def checkSchema(target, schema="https"):
    """
    Attempts to check if the schema of a given URL is valid,
    prepends given schema if not; default HTTPS
    """
    parsed = urllib.parse.urlparse(target)
    return "{schema}://{target}".format(target=target, schema=schema) \
        if not bool(parsed.scheme) else target


def parseTargets(targets: str) -> set:
    """
    Parses a given target(s) - if a file is provided,
    attempts to parse assuming it's newline separated
    Also accepts a single target
    Returns results as a set
    """
    results = []
    if os.path.isfile(targets):
        with open(targets) as f:
            for line in f:
                results.append(checkSchema(line.strip()))
    else:
        results.append(checkSchema(targets))
    return set(results)


def getCookies(url: str) -> list:
    """
    Gets cookies for a given URL and returns them in a 4 part tuple in the form
    (URL, cookie name, bool(HTTPOnly), bool(secure))
    """
    try:
        result = requests.get(url, verify=False, timeout=3)
    except Exception as e:
        print(e)
        return []
    cookies = []
    for cookie in result.cookies:
        httpOnly = False
        for rest in cookie._rest:
            httpOnly = True if rest == "Httponly" else False
        cookies.append((url,
                        cookie.name,
                        httpOnly,
                        True if cookie.secure else False
                        ))
    return cookies


def main(targets, outfile):
    """
    Main function, takes a target name/file and parses them,
    passes to thread pool and ultimately writes to the outfile in CSV format
    """
    targets = parseTargets(targets)

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(getCookies, targets, timeout=10)

    with open(outfile, 'w+') as f:
        f.write("URL,Cookie Name,HTTPOnly?,Secure?\n")
        for result in results:
            url = ""
            for cookie in result:
                url = cookie[0] if url is "" else ".."
                f.write("{url},{name},{httponly},{secure}\n".format(
                    url=url, name=cookie[1],
                    httponly="Yes" if cookie[2] else "No",
                    secure="Yes" if cookie[3] else "No"
                ))

    print("[+] Results written to {}".format(args.outfile))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Parse cookies from given URL(s)")
    parser.add_argument(
        "-t", "--target",
        help="Single target or file of newline seperated targets",
        required=True
    )
    parser.add_argument(
        "-o", "--outfile", default="crumbled.csv",
        help="File to write 'result info' to;\
        CSV format; defaults to shredder.csv"
    )
    args = parser.parse_args()

    main(args.target, args.outfile)
