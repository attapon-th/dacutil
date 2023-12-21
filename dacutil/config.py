from addict import Dict as AdDict
from urllib.parse import urlparse
import os
from configparser import ConfigParser
import requests


def get_config(uri_of_file: str):
    conf = AdDict()
    uri = uri_of_file

    if "://" not in uri:
        conf = get_config_file(uri)
    # <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
    u = urlparse(uri_of_file)
    if u.scheme == "http" or u.scheme == "https":
        conf = get_config_url(uri)
    if u.scheme == "file":
        conf = get_config_file(uri.replace("file://", ""))
    return conf


def get_config_file(filepath: str) -> AdDict:
    confparse = ConfigParser()
    if os.path.exists(filepath):
        confparse.read(filepath)
        conf = AdDict(dict(confparse._sections))  # type: ignore
        return conf
    return AdDict()


def get_config_url(url: str) -> AdDict:
    conf = AdDict()
    r = requests.get(url)
    if r.status_code >= 200 and r.status_code < 300:
        c = ConfigParser()
        c.read_string(r.text)
        conf = AdDict(dict(c._sections))  # type: ignore
    return conf
