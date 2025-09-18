# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name:
	description: >
	    Utility functions for Subtrix templating engine.
	version: 0.0.0.0.0.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
import datetime as dt
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import dirname, join
from typing import Optional

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from condor.utils import thingify
from ogma.logma import Logma
# ======================================3rd Party Library Modules=====================================================||
from uuid_extensions import uuid7

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


def now() -> str:
    """
    Get current timestamp as string.

    Returns:
        Current timestamp in YYYYMMDDHHMMSS format
    """
    return dt.datetime.now().strftime("%Y%m%d%H%M%S")


def today() -> str:
    """
    Get current date as string.

    Returns:
        Current date in YYYYMMDD format
    """
    return dt.date.today().strftime("%Y%m%d")


def uuid_generator(n: Optional[int] = None) -> str:
    """
    Generate a UUID string.

    Args:
        n: Optional length to return from end of UUID

    Returns:
        UUID string or last n characters
    """
    try:
        from uuid_extensions import uuid7

        uuid_str = str(uuid7())
    except ImportError:
        import uuid

        uuid_str = str(uuid.uuid4())

    if n is None:
        return uuid_str
    return uuid_str[-n:]


def get_doc(file_path: str) -> str:
    """
    Read document from file.

    Args:
        file_path: Path to file

    Returns:
        File contents as string
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def get_variable_data(term):
    """"""
    cfg = condor.Instruct(join(here, "_data_", "varr.yaml")).load().dikt["knowns"]
    if "<(" in term:
        # found, within = search(cfg, [], [], [term])
        # varobj = found[0]
        varobj = cfg[term]
        if varobj.get("object", None):
            data_function = thingify(varobj["object"])
            if varobj.get("outs", None):
                function_data = getattr(data_function(), varobj["outs"])
            else:
                function_data = data_function()
            data_term = function_data
        elif varobj.get("tmplt", None):
            data_term = varobj["tmplt"]
        else:
            data_term = term
    return data_term


#
# def now():
#     """"""
#     return dt.datetime.now().strftime("%Y%m%d%H%M%S")
#
#
# def today():
#     """"""
#     return dt.date.today().strftime("%Y%m%d")


def uuid(n=None):
    """"""
    uuid_ = str(uuid7())
    if n is None:
        return uuid_
    return uuid_[len(uuid_) - n :]


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
