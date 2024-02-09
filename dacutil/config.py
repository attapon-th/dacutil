import os
from tokenize import String


from .addict import Addict
from urllib.parse import urlparse, ParseResult
from typing import Tuple, Optional, Dict, Literal
from configobj import ConfigObj
from requests.auth import HTTPBasicAuth
from requests import Response, get as req_get
import json
from io import StringIO
import yaml

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

# error is config scheme not support
ErrConfigSchemeNotSupport = Exception("Config scheme not support")

ConfigTypeSupport = ["ini", "json", "yaml", "toml"]


def get_config(
    uri_of_file: str,
    file_type: Literal["infer", "ini", "json", "yaml", "toml"] = "infer",
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

    ftype: Literal["ini", "json", "yaml", "toml"] = "ini"
    if file_type == "infer":
        if u.path.lower().endswith(".json"):
            ftype = "json"
        elif u.path.lower().endswith(".ini"):
            ftype = "ini"
        elif u.path.lower().endswith(".yaml") or u.path.lower().endswith(".yml"):
            ftype = "yaml"
        elif u.path.lower().endswith(".toml"):
            ftype = "toml"
    else:
        ftype = file_type

    if u.scheme in ["http", "https"]:
        conf: Addict = get_config_url(uri, ftype, basic_auth, headers)
    elif u.scheme == "file":
        conf = get_config_file(uri.replace("file://", ""), ftype)
    else:
        raise ErrConfigSchemeNotSupport

    return conf


def get_config_file(filepath: str, file_type: Literal["ini", "json", "yaml", "toml"]) -> Addict:
    conf = Addict()

    if os.path.exists(filepath):
        with open(file=filepath, mode="r", encoding="utf-8") as f:
            conf = Addict(read_config(f.read(), file_type))
    return conf


def get_config_url(
    url: str,
    file_type: Literal["ini", "json", "yaml", "toml"],
    basic_auth: Optional[Tuple[str, str]] = None,
    headers: Optional[Dict[str, str]] = None,
) -> Addict:
    conf = Addict()
    bAuth: HTTPBasicAuth | None = HTTPBasicAuth(*basic_auth) if basic_auth else None
    r: Response = req_get(url, timeout=30, auth=bAuth, headers=headers)

    if r.status_code >= 200 and r.status_code < 300:
        c = read_config(r.text, file_type)
        conf = Addict(c)

    return conf


def read_config(data: str | bytes, file_type: Literal["ini", "json", "yaml", "toml"]) -> dict:
    c = {}
    if len(data) > 0:
        if file_type == "ini":
            cfg = ConfigObj(StringIO(str(data)))
            c = cfg.dict()
        elif file_type == "json":
            cfg = json.loads(data)
            c = dict(cfg)
        elif file_type == "yaml":
            c = yaml.load(StringIO(str(data)), Loader=Loader)
        elif file_type == "toml":
            c = tomllib.loads(str(data))
    return c
