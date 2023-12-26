import os


from addict import Addict
from urllib.parse import urlparse, ParseResult
from configparser import ConfigParser
from typing import Tuple, Optional, Dict
from requests.auth import HTTPBasicAuth
from requests import Response, get as req_get
import json

# error is config scheme not support
ErrConfigSchemeNotSupport = Exception("Config scheme not support")


def get_config(
    uri_of_file: str,
    basic_auth: Optional[Tuple[str, str]] = None,
    headers: Optional[Dict[str, str]] = None,
) -> Addict:
    """
    Retrieves the configuration from a specified file or URL.

    Parameters:
        uri_of_file (str): The URI of the file or URL from which to retrieve the configuration.
        basic_auth (Optional[Tuple[str, str]]): Optional basic authentication credentials as a tuple of username and password.
        headers (Optional[Dict[str, str]]): Optional headers to include in the request.

    Returns:
        Addict: The retrieved configuration as an `Addict` object.

    Raises:
        ErrConfigSchemeNotSupport: If the URI scheme is not supported.

    """
    conf = Addict()
    uri: str = uri_of_file

    if "://" not in uri:
        uri = "file://" + os.path.realpath(uri)

    u: ParseResult = urlparse(uri)
    if u.scheme in ["http", "https"]:
        conf: Addict = get_config_url(uri, basic_auth, headers)
    elif u.scheme == "file":
        conf = get_config_file(uri.replace("file://", ""))
    else:
        raise ErrConfigSchemeNotSupport

    return conf


def get_config_file(filepath: str) -> Addict:
    confparse = ConfigParser()
    conf = Addict()
    if os.path.exists(filepath):
        if filepath.endswith(".ini"):
            confparse.read(filepath)
            conf = Addict(dict(confparse._sections))  # type: ignore
        elif filepath.endswith(".json"):
            with open(file=filepath, mode="r", encoding="utf-8") as f:
                conf = Addict(json.loads(f.read()))
    return conf


def get_config_url(
    url: str,
    basic_auth: Optional[Tuple[str, str]] = None,
    headers: Optional[Dict[str, str]] = None,
) -> Addict:
    conf = Addict()
    bAuth: HTTPBasicAuth | None = HTTPBasicAuth(*basic_auth) if basic_auth else None
    r: Response = req_get(url, timeout=30, auth=bAuth, headers=headers)

    if r.status_code >= 200 and r.status_code < 300:
        if url.endswith(".ini"):
            c = ConfigParser()
            c.read_string(r.text)
            conf = Addict(dict(c._sections))  # type: ignore
        elif url.endswith(".json"):
            conf = Addict(r.json())
        else:
            raise ErrConfigSchemeNotSupport
    return conf


if __name__ == "__main__":
    get_config("file://../test/config.ini")
