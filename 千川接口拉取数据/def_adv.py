from time import sleep

from requests import get

from def_normal import build_url

#获取店铺下的所有广告主账户————账户ID
def get_adv_ids(access_token,shop_id_list,retry_limit=3):
    open_api_url = 'https://ad.oceanengine.com/open_api/'
    url_params = '2/customer_center/advertiser/list/'
    url = open_api_url + url_params
    all_advertisers = []
    for shop_id in shop_id_list:
        json_params = {
            'cc_account_id': shop_id,
            'account_source': 'QIANCHUAN',
            'page': 1,
            'page_size': 100,
        }
        headers = {'Access-Token': access_token}
        try:
            retry_count = 1
            while retry_count <= retry_limit:
                format_url = build_url(url,json_params)
                rsp = get(format_url, headers=headers)
                rsp_data = rsp.json()
                if rsp_data['code'] == 0:
                    advertisers = rsp_data['data'].get('list',[])
                    break
                else:
                    retry_count += 1
                    sleep(2)
            else:
                print(f'get_adv_ids请求多次失败: {rsp_data}')
                return None
        except Exception as err:
            print(f'get_adv_ids未成功发起请求: {err}')
            return None
        all_advertisers.extend(advertisers)
    return all_advertisers

#根据账户ID获取账户名
def get_advertiser_name(access_token, advertiser_id,retry_limit=3):
    open_api_url = 'https://ad.toutiao.com/open_api/'
    url_params = '2/advertiser/public_info/'
    url = open_api_url + url_params
    json_params = {'advertiser_ids': [advertiser_id]}
    headers = {'Access-Token': access_token}
    try:
        retry_count = 1
        while retry_count <= retry_limit:
            format_url = build_url(url,json_params)
            rsp = get(format_url, headers=headers)
            rsp_data = rsp.json()
            if rsp_data.get('code') == 0:
                adv_info = rsp_data['data']
                if isinstance(adv_info, list) and len(adv_info) > 0:
                    advertiser_name = adv_info[0].get('name', '获取失败')
                    return advertiser_name
                else:
                    advertiser_name = '获取失败'
            else:
                retry_count += 1
                sleep(2)
        else:
            print(f'get_advertiser_name请求多次失败: {rsp_data}')
            return None
    except Exception as err:
        print(f'get_advertiser_name未成功发起请求: {err}')
    return None

#获取账户数据，判定账户千川标准消耗
def get_advertiser_cost(access_token,advertiser_id,start_date,end_date,marketing_goal,order_platform,retry_limit=3):
    open_api_url_prefix = 'https://ad.oceanengine.com/open_api/'
    url_params = 'v1.0/qianchuan/report/advertiser/get/'
    url = open_api_url_prefix + url_params
    # 请求参数
    json_params = {
        'advertiser_id': advertiser_id,
        'start_date': start_date,
        'end_date': end_date,
        'fields': ['stat_cost'],
        'filtering': {
            'marketing_goal': marketing_goal,
            #'QIANCHUAN'：千川，'ECP_AWEME':随心推
            'order_platform': order_platform
        }
    }
    headers = {'Access-Token': access_token}
    try:
        retry_count = 1
        while retry_count <= retry_limit:
            format_url = build_url(url,json_params)
            rsp = get(format_url, headers=headers)
            rsp_data = rsp.json()
            if rsp_data.get('code') == 0:
                adv_info = rsp_data['data'].get('list',None)
                if adv_info is not None and len(adv_info) > 0:
                    cost = adv_info[0].get('stat_cost',0)
                else:
                    cost = 0
                return cost
            else:
                retry_count += 1
                sleep(2)
        else:
            print(f'get_advertiser_cost请求多次失败: {rsp_data}')
            return None
    except Exception as err:
        print(f"get_advertiser_cost未成功发起请求: {err}")
    return None

#获取账户数据，判定账户千川全域消耗
def get_advertiser_uni_cost(access_token,advertiser_id,start_date,end_date,marketing_goal,retry_limit=3):
    open_api_url_prefix = 'https://ad.oceanengine.com/open_api/'
    url_params = 'v1.0/qianchuan/report/uni_promotion/get/'
    url = open_api_url_prefix + url_params
    # 请求参数
    json_params = {
        'advertiser_id': advertiser_id,
        'start_date': start_date,
        'end_date': end_date,
        'fields': ['stat_cost'],
        'filtering': {
            'marketing_goal': marketing_goal,
        }
    }
    headers = {'Access-Token': access_token}
    try:
        retry_count = 1
        while retry_count <= retry_limit:
            format_url = build_url(url,json_params)
            rsp = get(format_url, headers=headers)
            rsp_data = rsp.json()
            if rsp_data.get('code') == 0:
                stat_cost = rsp_data['data'].get('stat_cost',0)
                return stat_cost
            else:
                retry_count += 1
                sleep(2)
        else:
            print(f'get_advertiser_uni_cost请求多次失败: {rsp_data}')
            return None
    except Exception as err:
        print(f"get_advertiser_uni_cost未成功发起请求: {err}")
    return None