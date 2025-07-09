import warnings as Warnings
from time import sleep

from requests import get

from def_normal import build_url

Warnings.filterwarnings('ignore')

def get_flow(access_token,advertiser_id,start_date,end_date,retry_limit=3):
    open_api_url = 'https://api.oceanengine.com/open_api/'
    url_params = 'v1.0/qianchuan/finance/detail/get/'
    url = open_api_url + url_params
    json_params = {
        'advertiser_id': advertiser_id,
        'end_date': end_date,
        'page': 1,
        'page_size': 200,
        'start_date': start_date
    }
    headers = {'Access-Token': access_token}
    try:
        retry_count = 1
        while retry_count <= retry_limit:
            format_url = build_url(url,json_params)
            rsp = get(format_url, headers=headers)
            rsp_data = rsp.json()
            if rsp_data['code'] == 0:
                flow_data = rsp_data.get('data', {}).get('list', [])
                if len(flow_data) > 0:
                    flow_data = flow_data[0]
                    return flow_data
                else:
                    return 0
            elif rsp_data['code'] == 40002:
                return 0
            else:
                retry_count += 1
                sleep(2)
        else:
            print(f'get_flow请求多次失败: {rsp_data}')
            return None
    except Exception as e:
        print(f'get_flow未成功发起请求: {e}')
        return None