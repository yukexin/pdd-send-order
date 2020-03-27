import xlrd
import requests
from utils import param
import json
import common


def read_excel_send(file_name):
    data = xlrd.open_workbook(file_name)
    table = data.sheet_by_index(0)
    name = table.name
    row_num = table.nrows
    col_num = table.ncols
    for i in range(1, col_num):
        order_sn = table.cell_value(i, 2)
        tracking_number = table.cell_value(i, 13)
        print(order_sn)
        print(tracking_number)
        adata = {
            'type': 'pdd.logistics.online.send',
            'order_sn': order_sn,
            'tracking_number': tracking_number,
            # 韵达
            'logistics_id': '121'
        }
        param.data_param(adata)
        response = requests.post(common.url,
                                 headers=common.aheaders,
                                 data=json.dumps(param.data_sign(adata)))
        print(response.json())


if __name__ == '__main__':
    read_excel_send()
