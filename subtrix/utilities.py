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
import difflib
import json
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import dirname, join
from typing import Optional

# ======================================3rd Party Library Modules=====================================================||
from uuid_extensions import uuid7

# ======================================Solutions Brewer Library Modules==============================================||

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||


# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


def diff_dicts(dict1, dict2):
    # 1. Convert dicts to sorted, indented JSON strings to make them comparable line-by-line
    # sort_keys=True is crucial to ensure order doesn't trigger "fake" differences
    str1 = json.dumps(dict1, indent=2, sort_keys=True).splitlines()
    str2 = json.dumps(dict2, indent=2, sort_keys=True).splitlines()
    # 2. Generate a unified diff
    diff = difflib.unified_diff(str1, str2, fromfile="original", tofile="current", lineterm="")
    # 3. Join and return or print
    result = "\n".join(diff)
    # if result:
    # print("Dictionaries differ:", file=sys.stderr)
    # print(result, file=sys.stderr)
    return result


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
    from condor import condor
    from condor.utils import thingify

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
# def thingify(thing, module=None, path=None, test=False):
#     """Import dotted path text and return the attribute/class"""
#     if test:
#         if module is None:
#             module_path, thing = thing.rsplit(".", 1)
#             module = import_module(module_path)
#         obj = getattr(module, thing)
#         return obj
#     else:
#         if module is None:
#             try:
#                 module_path, thing = thing.rsplit(".", 1)
#                 module = import_module(module_path)
#             except Exception as e:
#                 logma.warning(f"Thingify Module Path {thing} Failed {e}")
#                 logma.warning(f"From this Path {path}")
#                 traceback.print_exc()
#                 raise e
#         try:
#             obj = getattr(module, thing)
#         except AttributeError as e:
#             logma.warning(f"Thingification Failed due to {e}")
#             traceback.print_exc()
#             raise e
#         return obj


def uuid(n=None):
    """"""
    uuid_ = str(uuid7())
    if n is None:
        return uuid_
    return uuid_[len(uuid_) - n :]


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
