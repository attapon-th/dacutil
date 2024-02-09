# Data Analytic Utils

## Install

```bash
pip install dacutil
```
or dev
```bash
pip install git+https://github.com/attapon-th/dacutil@main
```

## Usage

```python
from dacutil import (
    datediff,
    get_config,
    check_mod11,
    df_strip,
    worker,
    Addict
)
```

# Functions

## `get_config`
support file type:
- [x] ini
- [x] json
- [x] yaml
- [x] toml
  
### Example 
```python
from dacutil import get_config, Addict

# get config from file
config: Addict = get_config("path/to/file.ini")
# or
config: Addict  = get_config("file://path/to/file.ini")

# get config from url
config: Addict  = get_config("http://example.com/file.json")
# or
config: Addict  = get_config("https://example.com/file.json")
```
