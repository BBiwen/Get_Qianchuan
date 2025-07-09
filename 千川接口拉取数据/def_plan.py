from time import sleep

from requests import get

from def_normal import build_url

#获取千川PC广告计划数据
def get_ad_report(access_token,advertiser_id,start_date,end_date,marketing_goal,order_platform,retry_limit=3):
    open_api_url = 'https://ad.oceanengine.com/open_api/'
    url_params = 'v1.0/qianchuan/report/ad/get/'
    url = open_api_url + url_params
    json_params = {
        'advertiser_id':advertiser_id,
        'fields':['stat_cost','show_cnt','ctr','click_cnt','pay_order_count','create_order_amount','create_order_count','pay_order_amount','create_order_roi','prepay_and_pay_order_roi','total_play','play_duration_3s','play_over','attribution_convert_cnt','attribution_convert_rate','attribution_convert_cost','indirect_order_pay_gmv_7days','all_order_pay_roi_7days','pay_order_coupon_amount'],
        'page_size':500,
        'start_date':start_date,
        'end_date':end_date,
        'order_type':'DESC',
        'time_granularity':'TIME_GRANULARITY_DAILY', 
        'filtering': {
            'marketing_goal':marketing_goal,
            'order_platform':order_platform,
        }
    }
    headers = {'Access-Token': access_token}
    try:
        retry_count = 1
        while retry_count <= retry_limit:
            format_url = build_url(url,json_params)
            rsp = get(format_url, headers=headers)
            rsp_data = rsp.json()
            if rsp_data['code'] == 0:
                ad_report = rsp_data['data'].get('list', [])
                return ad_report
            else:
                retry_count += 1
                sleep(2)
        else:
            print(f'get_ad_report请求多次失败: {rsp_data}')
            return None
    except Exception as err:
        print(f"get_ad_report未成功发起请求: {err}")
        return None
    
#获取计划详细数据
def get_ad_detail(access_token,advertiser_id,ad_id,retry_limit=3):
    open_api_url = 'https://ad.oceanengine.com/open_api/'
    url_params = 'v1.0/qianchuan/ad/detail/get/'
    url = open_api_url + url_params
    json_params = {
        'advertiser_id':advertiser_id,
        'ad_id':ad_id,
        'request_material_url':False,
        'version':'v2'
    }
    headers = {'Access-Token': access_token}

    try:
        retry_count = 1
        while retry_count <= retry_limit:
            format_url = build_url(url,json_params)
            rsp = get(format_url, headers=headers)
            rsp_data = rsp.json()
            if rsp_data['code'] == 0:
                data = rsp_data['data']
                #计划名称
                ad_name = data.get('name', '')
                # 达人信息
                if 'aweme_info' in data and isinstance(data['aweme_info'], list) and len(data['aweme_info']) > 0:
                    aweme_info = data['aweme_info'][0]
                else:
                    aweme_info = {}
                aweme_name = aweme_info.get('aweme_name', '')
                aweme_id = aweme_info.get('aweme_show_id', '')
                aweme_uid = aweme_info.get('aweme_id', '')
                # 商品信息
                if 'product_info' in data and isinstance(data['product_info'], list) and len(data['product_info']) > 0:
                    product_info = data['product_info'][0]
                else:
                    product_info = {}
                product_name = product_info.get('name', '')
                product_id = product_info.get('id', '')
                # 营销场景
                marketing_scene = data.get('marketing_scene', '')

                detail = {
                    'ad_name': ad_name,
                    'product_id': str(product_id),
                    'product_name': product_name,
                    'aweme_id': str(aweme_id),
                    'aweme_name': aweme_name,
                    'marketing_scene': marketing_scene,
                    'aweme_uid': str(aweme_uid)
                }
                return detail
            else:
                retry_count += 1
                sleep(2)
        else:
            print(f'get_ad_detail请求多次失败: {rsp_data}')
            return None
    except Exception as err:
        print(f"get_ad_detail未成功发起请求: {err}")
        return None