from time import sleep

from requests import get

from def_normal import build_url

#全域——获取账户消耗
def get_uni_adv_cost(access_token,advertiser_id,start_date,end_date,marketing_goal,retry_limit=3):
    open_api_url = 'https://api.oceanengine.com/open_api/'
    url_params = 'v1.0/qianchuan/report/uni_promotion/get/'
    url = open_api_url + url_params
    json_params = {
        'advertiser_id':advertiser_id,
        'start_date':start_date,
        'end_date':end_date,
        'marketing_goal':marketing_goal,
        'lab_ad_type':'LAB_AD',
        'fields':['stat_cost'],
    }
    headers = {'Access-Token': access_token}
    try:
        retry_count = 1
        while retry_count <= retry_limit:
            format_url = build_url(url,json_params)
            rsp = get(format_url,headers=headers)
            rsp_data = rsp.json()
            if rsp_data['code'] == 0:
                cost = rsp_data['data'].get('stat_cost', 0)
                return cost
            else:
                retry_count += 1
                sleep(2)
        else:
            print(f'get_uni_adv_cost请求多次失败: {rsp_data}')
            return None
    except Exception as e:
        print(f'get_uni_adv_cost未成功发起请求: {e}')
        return None

#全域推商品-数据报表
def get_uni_pro_mertics(access_token, advertiser_id, start_date, end_date,retry_limit=3):
    open_api_url = 'https://api.oceanengine.com/open_api/'
    url_params = 'v1.0/qianchuan/report/uni_promotion/data/get/'
    url = open_api_url + url_params
    headers = {'Access-Token': access_token}
    page = 1
    mertic_info = []
    try:
        retry_count = 1
        while retry_count <= retry_limit:
            while True:
                json_params = {
                    'advertiser_id':advertiser_id,
                    'data_topic':'SITE_PROMOTION_PRODUCT_AD',
                    'dimensions':['ad_id'],
                    'metrics':['stat_cost','total_pay_order_count_for_roi2','total_pay_order_gmv_for_roi2','total_prepay_and_pay_order_roi2','total_cost_per_pay_order_for_roi2','total_pay_order_coupon_amount_for_roi2'],
                    'filters':[],
                    'start_time':start_date,
                    'end_time':end_date,
                    'order_by':[{'field':'stat_cost','type':2}],
                    'page':page,
                    'page_size':200
                }
                format_url = build_url(url,json_params)
                rsp = get(format_url,headers=headers)
                rsp_data = rsp.json()
                if rsp_data['code'] == 0:
                    total_page = rsp_data['data']['page_info'].get('total_page',1)
                    temp_data = rsp_data['data'].get('rows', [])
                    if temp_data:
                        mertic_info.extend(temp_data)
                        if page < total_page:
                            page = page + 1
                            sleep(2)
                        else:
                            return mertic_info
                    else:
                        return mertic_info
                else:
                    retry_count += 1
                    sleep(2)
                    break
        else:
            print(f'get_uni_pro_mertics请求多次失败: {rsp_data}')
            return None
    except Exception as e:
        print(f'get_uni_pro_mertics未成功发起请求: {e}')
        return None
    
#获取全域直播的推广列表——抖音号数据
def get_uni_room_info(access_token,advertiser_id,start_date,end_date,marketing_goal,retry_limit=3):
    open_api_url = 'https://api.oceanengine.com/open_api/'
    url_params = 'v1.0/qianchuan/uni_promotion/list/'
    url = open_api_url + url_params
    json_params = {
        'advertiser_id':advertiser_id,
        'start_time':start_date,
        'end_time':end_date,
        'marketing_goal':marketing_goal,
        'fields':['stat_cost','total_prepay_and_pay_order_roi2','total_pay_order_gmv_for_roi2','total_pay_order_count_for_roi2','total_cost_per_pay_order_for_roi2','total_pay_order_coupon_amount_for_roi2'],
        'order_type':'DESC',
        'order_field':'stat_cost',
        'page':1,
        'page_size':100
    }
    headers = {'Access-Token': access_token}
    try:
        retry_count = 1
        while retry_count <= retry_limit:
            format_url = build_url(url,json_params)
            rsp = get(format_url,headers=headers)
            rsp_data = rsp.json()
            if rsp_data['code'] == 0:
                ad_list = rsp_data['data'].get('ad_list', [])
                return ad_list
            else:
                retry_count += 1
                sleep(2)
        else:
            print(f'get_uni_room_info请求多次失败: {rsp_data}')
            return None
    except Exception as e:
        print(f'get_uni_room_info未成功发起请求: {e}')
        return None
    
#获取抖音号uid
def get_uni_aweme_uid(access_token,advertiser_id,ad_id,retry_limit=3):
    open_api_url = 'https://api.oceanengine.com/open_api/'
    url_params = 'v1.0/qianchuan/uni_promotion/ad/detail/'
    url = open_api_url + url_params
    json_params = {
        'advertiser_id':advertiser_id,
        'ad_id':ad_id
    }
    headers = {'Access-Token': access_token}
    try:
        retry_count = 1
        while retry_count <= retry_limit:
            format_url = build_url(url,json_params)
            rsp = get(format_url,headers=headers)
            rsp_data = rsp.json()
            if rsp_data['code'] == 0:
                aweme_uid = rsp_data['data'].get('aweme_id', '')
                return aweme_uid
            else:
                retry_count += 1
                sleep(2)
        else:
            print(f'get_uni_aweme_uid请求多次失败: {rsp_data}')
            return None
    except Exception as e:
        print(f'get_uni_aweme_uid未成功发起请求: {e}')
        return None