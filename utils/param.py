import hashlib
import common
import time


def data_param(adata):
    adata['client_id'] = common.client_id
    adata['grant_type'] = common.grant_type
    adata['client_secret'] = common.client_secret
    adata['timestamp'] = str(int(time.time()))
    adata['access_token'] = 'e3eb824958be45df8362cd12d5e6432f8b55532a'


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
