from time import sleep

from requests import get

from def_normal import build_url

#获取计划下素材列表
def get_ad_material_info(access_token,advertiser_id,ad_id,start_time,end_time,material_type,retry_limit=3):
    open_api_url = 'https://api.oceanengine.com/open_api/'
    url_params = 'v1.0/qianchuan/ad/material/get/'
    url = open_api_url + url_params
    headers = {'Access-Token': access_token}
    material_info = []
    try:
        retry_count = 1
        while retry_count <= retry_limit:
            json_params = {
                'advertiser_id': advertiser_id,
                'ad_id':ad_id,
                'filtering':{
                    'material_type':material_type,
                    'having_cost':'YES',
                    'start_time':start_time,
                    'end_time':end_time,
                },
                'page':1,
                'page_size':100
            }
            formatted_url = build_url(url,json_params)
            rsp = get(formatted_url,headers=headers)
            rsp_data = rsp.json()
            if rsp_data['code'] == 0:
                total_num = rsp_data['data'].get('page_info',{}).get('total_num',0)
                if total_num == 0:
                    return 0
                material_info = rsp_data['data'].get('ad_material_infos',[])
                if material_info:
                    return material_info
                else:
                    retry_count += 1
                    sleep(2)
            else:
                retry_count += 1
                sleep(2)
        else:
            print(f'get_ad_material_info请求多次失败: {rsp_data}')
            return None
    except Exception as e:
        print(f'get_ad_material_info未成功发起请求: {e}')
        return None

#获取计划下素材数据
def get_ad_material_data(access_token,advertiser_id,ad_id,material_id,start_date,end_date,material_type,retry_limit=3):
    open_api_url = 'https://api.oceanengine.com/open_api/'
    url_params = 'v1.0/qianchuan/report/ad/material/get/'
    url = open_api_url + url_params
    headers = {'Access-Token': access_token}

    json_params = {
        'advertiser_id': advertiser_id,
        'ad_id':ad_id,
        'start_date':start_date,
        'end_date':end_date,
        'fields':['pay_order_coupon_amount','stat_cost','pay_order_amount','pay_order_count', 'show_cnt', 'click_cnt', 'total_play', 'play_over', 'ecp_convert_cnt'],
        'filtering':{
            'object_ids':[material_id],
            'material_type':material_type
        }
    }
    try:
        retry_count = 1
        while retry_count <= retry_limit:
            formatted_url = build_url(url,json_params)
            rsp = get(formatted_url,headers=headers)
            rsp_data = rsp.json()
            if rsp_data['code'] == 0:
                material_data = rsp_data['data'].get('material_info',[])
                if material_data:
                    material_metrics = material_data[0].get('metrics',None)
                else:
                    material_metrics = 0
                return material_metrics
            else:
                retry_count += 1
                sleep(2)
        else:
            print(f'get_ad_material_data请求多次失败: {rsp_data}')
            return None
    except Exception as e:
        print(f'get_ad_material_data未成功发起请求: {e}')
        return None

#获取全域商品计划下素材列表
def new_get_uni_ad_material_metrics(access_token,advertiser_id,ad_id,start_time,end_time,data_topic,retry_limit=3):
    open_api_url = 'https://api.oceanengine.com/open_api/'
    url_params = 'v1.0/qianchuan/report/custom/get/'
    url = open_api_url + url_params
    headers = {'Access-Token': access_token}
    page = 1
    material_info = []
    if data_topic == 'SITE_PROMOTION_PRODUCT_POST_DATA_VIDEO':
        metrics = ['stat_cost_for_roi2','total_pay_order_gmv_for_roi2','total_prepay_and_pay_order_roi2','total_pay_order_count_for_roi2','total_pay_order_coupon_amount_for_roi2','product_show_count_for_roi2', 'product_click_count_for_roi2','video_play_count_for_roi2_v2','video_play_finish_rate_for_roi2_v2','product_convert_rate_for_roi2']
    elif data_topic == 'SITE_PROMOTION_PRODUCT_POST_DATA_IMAGE':
        metrics = ['stat_cost_for_roi2','total_pay_order_gmv_for_roi2','total_prepay_and_pay_order_roi2','total_pay_order_count_for_roi2','total_pay_order_coupon_amount_for_roi2','product_show_count_for_roi2', 'product_click_count_for_roi2','product_convert_rate_for_roi2']
    try:
        retry_count = 1
        while retry_count <= retry_limit:
            while True:
                json_params = {
                    'advertiser_id': advertiser_id,
                    'data_topic':data_topic, 
                    'dimensions':['material_id','roi2_material_video_name'],
                    'metrics':metrics,
                    'filters':[
                        {'field':'ad_id','type':1,'operator':7,'values':[str(ad_id)]},
                    ],
                    'start_time':start_time,
                    'end_time':end_time,
                    'order_by':[{'type':2,'field':'stat_cost_for_roi2'}],
                    'page':page,
                    'page_size':100
                }
                formatted_url = build_url(url,json_params)
                rsp = get(formatted_url,headers=headers)
                rsp_data = rsp.json()
                if rsp_data['code'] == 0:
                    total_number = rsp_data['data'].get('pagination',{}).get('total_num',0)
                    if total_number == 0:
                        return 0
                    total_page = rsp_data['data'].get('pagination',{}).get('total_page',1)
                    temp_data = rsp_data['data'].get('rows',[])
                    if temp_data:
                        for temp_data_info in temp_data:
                            stat_cost = temp_data_info.get('metrics',{}).get('stat_cost_for_roi2',0)
                            stat_cost = float(stat_cost.replace(',', ''))
                            if stat_cost == 0:
                                return material_info
                            else:
                                material_info.append(temp_data_info)
                        if page < total_page:
                            page += 1
                            sleep(2)
                        else:
                            return material_info
                    else:
                        return material_info
                else:
                    retry_count += 1
                    sleep(2)
                    break
        else:
            print(f'new_get_uni_ad_material_metrics请求多次失败: {rsp_data}')
            return None
    except Exception as e:
        print(f'new_get_uni_ad_material_metrics未成功发起请求: {e}')
        return None
    
#获取全域直播计划下素材列表
def new_get_uni_live_material_metrics(access_token,advertiser_id,anchor_id,start_time,end_time,data_topic,retry_limit=3):
    open_api_url = 'https://api.oceanengine.com/open_api/'
    url_params = 'v1.0/qianchuan/report/custom/get/'
    url = open_api_url + url_params
    headers = {'Access-Token': access_token}
    page = 1
    material_info = []
    try:
        retry_count = 1
        while retry_count <= retry_limit:
            while True:
                json_params = {
                    'advertiser_id': advertiser_id,
                    'data_topic':data_topic, 
                    'dimensions':['material_id','roi2_material_video_name'],
                    'metrics':['stat_cost_for_roi2','total_pay_order_gmv_for_roi2','total_prepay_and_pay_order_roi2','total_pay_order_count_for_roi2','total_pay_order_coupon_amount_for_roi2','live_show_count_for_roi2_v2', 'live_watch_count_for_roi2_v2','video_play_count_for_roi2_v2','video_play_finish_count_for_roi2_v2','live_convert_rate_for_roi2_v2'],
                    'filters':[
                        {'field':'anchor_id','type':1,'operator':7,'values':[str(anchor_id)]},
                    ],
                    'start_time':start_time,
                    'end_time':end_time,
                    'order_by':[{'type':2,'field':'stat_cost_for_roi2'}],
                    'page':page,
                    'page_size':100
                }
                formatted_url = build_url(url,json_params)
                rsp = get(formatted_url,headers=headers)
                rsp_data = rsp.json()
                if rsp_data['code'] == 0:
                    total_number = rsp_data['data'].get('pagination',{}).get('total_num',0)
                    if total_number == 0:
                        return 0
                    total_page = rsp_data['data'].get('pagination',{}).get('total_page',1)
                    temp_data = rsp_data['data'].get('rows',[])
                    if temp_data:
                        for temp_data_info in temp_data:
                            stat_cost = temp_data_info.get('metrics',{}).get('stat_cost_for_roi2',0)
                            stat_cost = float(stat_cost.replace(',', ''))
                            if stat_cost == 0:
                                return material_info
                            else:
                                material_info.append(temp_data_info)
                        if page < total_page:
                            page += 1
                            sleep(2)
                        else:
                            return material_info
                    else:
                        return material_info
                else:
                    retry_count += 1
                    sleep(2)
                    break
        else:
            print(f'new_get_uni_live_material_metrics请求多次失败: {rsp_data}')
            return None
    except Exception as e:
        print(f'new_get_uni_live_material_metrics未成功发起请求: {e}')
        return None
    
#获取全域直播计划下素材列表
def new_get_uni_live_metrics(access_token,advertiser_id,anchor_id,start_time,end_time,data_topic,retry_limit=3):
    open_api_url = 'https://api.oceanengine.com/open_api/'
    url_params = 'v1.0/qianchuan/report/custom/get/'
    url = open_api_url + url_params
    headers = {'Access-Token': access_token}
    try:
        retry_count = 1
        while retry_count <= retry_limit:
            json_params = {
                'advertiser_id': advertiser_id,
                'data_topic':data_topic, 
                'dimensions':['anchor_id','anchor_name'],
                'metrics':['stat_cost_for_roi2','total_pay_order_gmv_for_roi2','total_prepay_and_pay_order_roi2','total_pay_order_count_for_roi2','total_pay_order_coupon_amount_for_roi2','live_show_count_exclude_video_for_roi2','live_watch_count_exclude_video_for_roi2','live_convert_rate_exclude_video_for_roi2'],
                'filters':[
                    {'field':'anchor_id','type':1,'operator':7,'values':[str(anchor_id)]},
                ],
                'start_time':start_time,
                'end_time':end_time,
                'order_by':[],
                'page':1,
                'page_size':100
            }
            formatted_url = build_url(url,json_params)
            rsp = get(formatted_url,headers=headers)
            rsp_data = rsp.json()
            if rsp_data['code'] == 0:
                total_number = rsp_data['data'].get('pagination',{}).get('total_num',0)
                if total_number == 0:
                    return 0
                material_info = rsp_data['data'].get('rows',[])
                if material_info:
                    return material_info
                else:
                    retry_count += 1
                    sleep(2)
            else:
                retry_count += 1
                sleep(2)
        else:
            print(f'new_get_uni_live_metrics请求多次失败: {rsp_data}')
            return None
    except Exception as e:
        print(f'new_get_uni_live_metrics未成功发起请求: {e}')
        return None