import os


from .addict import Addict
from dacutil import crypt
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
ErrConfigNotFound = Exception("Config not found")

ConfigTypeSupport = ["ini", "json", "yaml", "toml"]


def get_config(
    uri_of_file: str,
    file_type: Literal["infer", "ini", "json", "yaml", "toml", "raw"] = "infer",
    basic_auth: Optional[Tuple[str, str]] = None,
    headers: Optional[Dict[str, str]] = None,
    age_key: Optional[str] = None,
    passphrase: Optional[str] = None,
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
    uri: str = uri_of_file

    if "://" not in uri:
        uri = "file://" + os.path.realpath(uri)

    u: ParseResult = urlparse(uri)

    ftype: Literal["ini", "json", "yaml", "toml", "raw"] = "ini"
    if file_type == "infer":
        filepath = u.path
        if filepath.lower().endswith(".age"):
            filepath = filepath.replace(".age", "")
        if filepath.lower().endswith(".json"):
            ftype = "json"
        elif filepath.lower().endswith(".ini"):
            ftype = "ini"
        elif filepath.lower().endswith(".yaml") or filepath.lower().endswith(".yml"):
            ftype = "yaml"
        elif filepath.lower().endswith(".toml"):
            ftype = "toml"
    else:
        ftype = file_type

    data: Optional[str | bytes] = None
    if u.scheme in ["http", "https"]:
        data = get_config_url(uri, basic_auth, headers)
    elif u.scheme == "file":
        data = get_config_file(uri.replace("file://", ""))
    else:
        raise ErrConfigSchemeNotSupport
    if data is None:
        raise ErrConfigNotFound
    if age_key is not None:
        data = crypt.age_decrypt(data, age_key)
    if passphrase is not None:
        data = crypt.decrypt_b64(data, passphrase)

    if isinstance(data, bytes):
        data = data.decode("utf-8")

    return Addict(read_config(data, file_type=ftype))


def get_config_file(filepath: str) -> Optional[str | bytes]:
    if os.path.exists(filepath):
        with open(file=filepath, mode="r", encoding="utf-8") as f:
            return f.read()
    return None


def get_config_url(
    url: str,
    basic_auth: Optional[Tuple[str, str]] = None,
    headers: Optional[Dict[str, str]] = None,
) -> Optional[str | bytes]:
    bAuth: HTTPBasicAuth | None = HTTPBasicAuth(*basic_auth) if basic_auth else None
    r: Response = req_get(url, timeout=30, auth=bAuth, headers=headers)

    if r.status_code >= 200 and r.status_code < 300:
        return r.text
    return None


def read_config(
    data: str | bytes,
    file_type: Literal["ini", "json", "yaml", "toml", "raw"],
) -> dict:
    c = {}
    if len(data) > 0:
        if isinstance(data, bytes):
            data_str: str = data.decode("utf-8")
        elif isinstance(data, str):
            data_str = data
        else:
            raise Exception("Invalid data type")
        if file_type == "ini":
            cfg = ConfigObj(StringIO(data_str))
            c = cfg.dict()
        elif file_type == "json":
            cfg = json.loads(data_str)
            c = dict(cfg)
        elif file_type == "yaml":
            c = yaml.load(StringIO(data_str), Loader=Loader)
        elif file_type == "toml":
            c = tomllib.loads(data_str)
        else:
            return {"raw": data_str}
    return c
