import hashlib
from typing import OrderedDict
from urllib.parse import quote_plus


def sign_body(body: OrderedDict, sign_key: str) -> str:
    value_ary = []
    for key in body:
        if key == 'callbackUrl':
            value_ary.append(quote_plus(body[key]))
        elif key == 'fingerprint':
            value_ary.append(quote_plus(body[key]))
        else:
            value_ary.append(body[key])
    value_ary.append(sign_key)
    return hashlib.md5(''.join(value_ary).encode('utf8')).hexdigest()
