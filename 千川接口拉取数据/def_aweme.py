from time import sleep

from requests import get

from def_normal import build_url 

#获取订单数据
def get_order_info(access_token,start_date,end_date,advertiser_id,marketing_goal,retry_limit=3):
    open_api_url = 'https://api.oceanengine.com/open_api/'
    url_params = 'v1.0/qianchuan/aweme/report/order/get/'
    url = open_api_url + url_params
    headers = {'Access-Token': access_token}
    page = 1
    order_info = []
    try:
        retry_count = 1
        while retry_count <= retry_limit:
            while True:
                json_params = {
                    'advertiser_id':advertiser_id,
                    'start_date':start_date,
                    'end_date':end_date,
                    'fields':['pay_order_amount','stat_cost','prepay_and_pay_order_roi','total_play','show_cnt','ctr','click_cnt','pay_order_count','ecp_convert_cnt','ecp_cpa_platform','play_duration_5s_rate'],
                    'order_type':'DESC',
                    'filtering':{
                        'marketing_goal':marketing_goal
                    },
                    'page':page,
                    'page_size':200
                }
                format_url = build_url(url,json_params)
                rsp = get(format_url, headers=headers)
                rsp_data = rsp.json()
                if rsp_data['code'] == 0:
                    total_page = rsp_data['data']['page_info'].get('total_page',1)
                    temp_data = rsp_data['data'].get('list',[])
                    if temp_data:
                        order_info.extend(temp_data)
                        if page < total_page:
                            page += 1
                            sleep(2)
                        else:
                            return order_info
                    else:
                        return order_info
                else:
                    retry_count += 1
                    sleep(2)
                    break
        else:
            print(f'get_order_info请求多次失败: {rsp_data}')
            return None
    except Exception as e:
        print(f'get_order_info未成功发起请求: {e}')
        return None

#获取订单信息
def get_order_detail(access_token,order_id,advertiser_id,retry_limit=3):
    open_api_url_prefix = 'https://api.oceanengine.com/open_api/'
    url_params = 'v1.0/qianchuan/aweme/order/detail/get/'
    url = open_api_url_prefix + url_params
    json_params = {
        'advertiser_id':advertiser_id,
        'order_id':order_id
    }
    headers = {'Access-Token': access_token}
    try:
        retry_count = 1
        while retry_count <= retry_limit:
            format_url = build_url(url,json_params)
            rsp = get(format_url, headers=headers)
            rsp_data = rsp.json()
            if rsp_data['code'] == 0:
                order_info = rsp_data.get('data', None)
                if order_info:
                    ad_details = {
                        'order_create_time':order_info.get('order_create_time', ''),
                        'aweme_uid': order_info.get('aweme_info', {}).get('aweme_id', ''),
                        'aweme_id': order_info.get('aweme_info', {}).get('aweme_show_id', ''),
                        'aweme_name': order_info.get('aweme_info', {}).get('aweme_name', ''),
                        'product_id': order_info.get('product_info', {}).get('id', ''),
                        'product_name': order_info.get('product_info', {}).get('name', '')
                        }
                    return ad_details
                else:
                    retry_count += 1
                    sleep(2)
            else:
                retry_count += 1
                sleep(2)
        else:
            print(f"get_order_detail请求多次失败: {rsp_data}")
            return None
    except Exception as err:
        print(f"get_order_detail未成功发起请求: {err}")
        return None