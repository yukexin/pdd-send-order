import hashlib
import common

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
