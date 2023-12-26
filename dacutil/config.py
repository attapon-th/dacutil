import os


from addict import Dict as adDict
from urllib.parse import urlparse, ParseResult
from configparser import ConfigParser
from typing import Tuple, Optional, Dict
from requests.auth import HTTPBasicAuth
from requests import Response, get as req_get


# Type alias for AdDict
AdDict = adDict

# error is config scheme not support
ErrConfigSchemeNotSupport = Exception("Config scheme not support")


def get_config(
    uri_of_file: str,
    basic_auth: Optional[Tuple[str, str]] = None,
    headers: Optional[Dict[str, str]] = None,
) -> AdDict:
    """
    Retrieves the configuration based on the provided URI of the file.

    Args:
        uri_of_file (str): The URI of the file containing the configuration.
        basic_auth (Tuple[str, str] | None, optional): The basic authentication credentials. Defaults to None.
        headers (dict[str, str] | None, optional): The headers. Defaults to None.

    Returns:
        AdDict: An `AdDict` object representing the retrieved configuration.
    """
    conf = AdDict()
    uri: str = uri_of_file

    # Check if the URI is a local file
    if "://" not in uri:
        # set the scheme to file
        uri = "file://" + os.path.realpath(uri)

    # <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
    u: ParseResult = urlparse(uri_of_file)
    if u.scheme == "http" or u.scheme == "https":
        conf: AdDict = get_config_url(uri, basic_auth, headers)
    elif u.scheme == "file":
        conf = get_config_file(uri.replace("file://", ""))
    else:
        raise ErrConfigSchemeNotSupport

    return conf


def get_config_file(filepath: str) -> AdDict:
    confparse = ConfigParser()
    if os.path.exists(filepath):
        confparse.read(filepath)
        conf = AdDict(dict(confparse._sections))  # type: ignore
        return conf
    return AdDict()


def get_config_url(
    url: str,
    basic_auth: Optional[Tuple[str, str]] = None,
    headers: Optional[Dict[str, str]] = None,
) -> AdDict:
    conf = AdDict()
    bAuth: HTTPBasicAuth | None = HTTPBasicAuth(*basic_auth) if basic_auth else None
    r: Response = req_get(url, timeout=30, auth=bAuth, headers=headers)

    if r.status_code >= 200 and r.status_code < 300:
        if url.endswith(".ini"):
            c = ConfigParser()
            c.read_string(r.text)
            conf = AdDict(dict(c._sections))  # type: ignore
        elif url.endswith(".json"):
            conf = AdDict(r.json())
        else:
            raise ErrConfigSchemeNotSupport
    return conf
