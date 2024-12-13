from app.libraries.list_process import (
    appendEle,
    indexAt,
    makeList,
    updateIndex,
    xsLength,
)
from app.libraries.predefined import scanin, toint, tostr
import time

global_table = {
    "clock": lambda: time.time(),
    "scanin": scanin,
    "toint": toint,
    "tostr": tostr,
    "list": makeList,
    "indexAt": indexAt,
    "length": xsLength,
    "updateAt": updateIndex,
    "append": appendEle,
}
