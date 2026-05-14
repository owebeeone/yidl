from __future__ import annotations
# this is from lark_v2_vertical.yidl:46
GETTERS = {'count': {'getter': 'plain'}, 'owner': {'getter': 'owner'}}

def getter_for(name: str) -> dict[str, str]:
    return GETTERS[name]
