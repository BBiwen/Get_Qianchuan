import os

import pandas as pd

import def_normal
import def_material

def uni_material_main(access_token,yesterday):

    start_time = f'{yesterday} 00:00:00'
    #end_day=pd.Timestamp.now().normalize().strftime('%Y-%m-%d')
    end_time = f'{yesterday} 23:59:59'

    all_advertiser_info = def_normal.get_adv_info_from_uni_product(yesterday)
    all_material_data = []

    while True:

        re_all_advertiser_info = []

        for advertiser_info in all_advertiser_info:

            advertiser_id = advertiser_info[0]
            advertiser_name = advertiser_info[1]
            plan_id = advertiser_info[2]
            plan_name = advertiser_info[3]

            operation_condition = 'normal'
            material_data = []

            for data_topic in ['SITE_PROMOTION_PRODUCT_POST_DATA_VIDEO','SITE_PROMOTION_PRODUCT_POST_DATA_IMAGE']:

                material_metrics = def_material.new_get_uni_ad_material_metrics(access_token,advertiser_id,plan_id,start_time,end_time,data_topic)

                if material_metrics is None:
                    operation_condition = None
                    re_all_advertiser_info.append(advertiser_info)
                    print(f'账户【{advertiser_id}】在计划【{plan_id}】的素材获取数据失败')
                    break
                elif material_metrics == 0:
                    continue
                
                for material_metric in material_metrics:

                    material_id = material_metric.get('dimensions',{}).get('material_id','')
                    material_name = material_metric.get('dimensions',{}).get('roi2_material_video_name',material_id)

                    metrics = material_metric.get('metrics',{})

                    stat_cost = metrics.get('stat_cost_for_roi2',0)
                    if isinstance(stat_cost, str):
                        stat_cost = float(stat_cost.replace(',', ''))
                    if stat_cost == 0:
                        continue

                    pay_order_amount = metrics.get('total_pay_order_gmv_for_roi2',0)
                    if isinstance(pay_order_amount, str):
                        pay_order_amount = float(pay_order_amount.replace(',', ''))

                    prepay_and_pay_order_roi = metrics.get('total_prepay_and_pay_order_roi2',0)
                    if isinstance(prepay_and_pay_order_roi, str):
                        prepay_and_pay_order_roi = float(prepay_and_pay_order_roi.replace(',', ''))
                    
                    pay_order_count = metrics.get('total_pay_order_count_for_roi2',0)
                    if isinstance(pay_order_count, str):
                        pay_order_count = float(pay_order_count.replace(',', ''))

                    pay_order_coupon_amount = metrics.get('total_pay_order_coupon_amount_for_roi2',0)
                    pay_order_coupon_amount = float(pay_order_coupon_amount.replace(',', ''))

                    product_show_count_for_roi2 = metrics.get('product_show_count_for_roi2',0)
                    if isinstance(product_show_count_for_roi2, str):
                        product_show_count_for_roi2 = float(product_show_count_for_roi2.replace(',', ''))

                    product_click_count_for_roi2 = metrics.get('product_click_count_for_roi2',0)
                    if isinstance(product_click_count_for_roi2, str):
                        product_click_count_for_roi2 = float(product_click_count_for_roi2.replace(',', ''))

                    video_play_count_for_roi2_v2 = metrics.get('video_play_count_for_roi2_v2',0)
                    if isinstance(video_play_count_for_roi2_v2, str):
                        video_play_count_for_roi2_v2 = float(video_play_count_for_roi2_v2.replace(',', ''))

                    video_play_finish_rate_for_roi2_v2 = metrics.get('video_play_finish_rate_for_roi2_v2',0)
                    if isinstance(video_play_finish_rate_for_roi2_v2, str):
                        video_play_finish_rate_for_roi2_v2 = video_play_finish_rate_for_roi2_v2.replace(',', '').rstrip('%')
                        video_play_finish_rate_for_roi2_v2 = float(video_play_finish_rate_for_roi2_v2)/100
                    if video_play_finish_rate_for_roi2_v2 != 0:
                        video_play_finish_for_roi2_v2 = video_play_count_for_roi2_v2 * video_play_finish_rate_for_roi2_v2
                    else:
                        video_play_finish_for_roi2_v2 = 0
                    
                    product_convert_rate_for_roi2 = metrics.get('product_convert_rate_for_roi2',0)
                    if isinstance(product_convert_rate_for_roi2, str):
                        product_convert_rate_for_roi2 = product_convert_rate_for_roi2.replace(',', '').rstrip('%')
                    product_convert_rate_for_roi2 = float(product_convert_rate_for_roi2)/100
                    if product_convert_rate_for_roi2 != 0:
                        product_convert_count_for_roi2 = product_click_count_for_roi2 * product_convert_rate_for_roi2
                    else:
                        product_convert_count_for_roi2 = 0

                    material_plan_info = ['全域推商品',str(advertiser_id), advertiser_name, str(plan_id), str(plan_name), str(material_id), str(material_name), '-', stat_cost, pay_order_amount, prepay_and_pay_order_roi, pay_order_count, pay_order_coupon_amount,product_show_count_for_roi2,product_click_count_for_roi2,video_play_count_for_roi2_v2,video_play_finish_for_roi2_v2,product_convert_count_for_roi2]

                    material_data.append(material_plan_info)

            if operation_condition:
                all_material_data.extend(material_data)

        if re_all_advertiser_info:
            all_advertiser_info = re_all_advertiser_info
        else:
            break

    def_normal.write_material_data(all_material_data,yesterday)