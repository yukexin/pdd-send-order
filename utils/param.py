import hashlib
import common
import time
from utils import db


def data_param(adata):
    adata['client_id'] = common.client_id
    adata['grant_type'] = common.grant_type
    adata['client_secret'] = common.client_secret
    adata['timestamp'] = str(int(time.time()))
    access_token = db.find()
    if access_token == 'empty':
        adata['access_token'] = access_token


def data_sign(adata):
    # sign签名算法
    keys = list(adata.keys())
    sortkeys = sorted(keys)
    sign = common.client_secret
    s = sign
    for key in sortkeys:
        s = s + key + adata[key]
    s = s + sign
    adata['sign'] = hashlib.md5(s.encode('utf-8')).hexdigest().upper()
    return adata
