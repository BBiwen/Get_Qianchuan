import os

import pandas as pd

import def_normal
import def_material

def live_video_material_main(access_token,yesterday):

    start_time = f'{yesterday} 00:00:00'
    end_time = f'{yesterday} 23:59:59'

    all_advertiser_info = def_normal.get_adv_info_from_live(yesterday)

    if all_advertiser_info is None:
        print('无数据')
        return None

    all_material_data = []

    while True:

        re_all_advertiser_info = []

        for advertiser_info in all_advertiser_info:

            advertiser_id = advertiser_info[0]
            advertiser_name = advertiser_info[1]
            plan_id = advertiser_info[2]
            plan_name = advertiser_info[3]

            material_data = []

            operation_condition = 'normal'

            material_type = 'VIDEO'

            material_info_list = def_material.get_ad_material_info(access_token,advertiser_id,plan_id,start_time,end_time,material_type)
            if material_info_list is None:
                operation_condition = None
                re_all_advertiser_info.append(advertiser_info)
                print('素材获取失败......')
                break
            elif material_info_list == 0:
                continue

            for material_info in material_info_list:

                material = material_info.get('material_info',{}).get('video_material',{})

                if material is None:
                    operation_condition = None
                    re_all_advertiser_info.append(advertiser_info)
                    print('素材获取失败......')
                    break

                material_id = material.get('material_id','-')
                if material_id == '-':
                    continue
                material_title = material.get('title','-')
                source = material.get('source','-')
                if source == 'AWEME':
                    source = '抖音主页视频'
                elif source == 'E_COMMERCE':
                    source = '本地上传'
                elif source == 'STAR':
                    source = '星图&即合共享素材'
                elif source == 'BP':
                    source = '巨量纵横共享素材'
                elif source == 'AI_GENERATE':
                    source = 'AI合成'

                material_metrics = def_material.get_ad_material_data(access_token,advertiser_id,plan_id,material_id,start_time,end_time,material_type)
                
                if material_metrics is None:
                    operation_condition = None
                    re_all_advertiser_info.append(advertiser_info)
                    print('素材获取失败......')
                    break
                else:
                    pay_order_coupon_amount = round(material_metrics.get('pay_order_coupon_amount',0),2)
                    stat_cost = round(material_metrics.get('stat_cost',0),2)
                    pay_order_amount = round(material_metrics.get('pay_order_amount',0),2)
                    if stat_cost != 0:
                        prepay_and_pay_order_roi = round(pay_order_amount / stat_cost, 2)
                    else:
                        prepay_and_pay_order_roi = 0.00
                    pay_order_count = round(material_metrics.get('pay_order_count',0),0)

                    show_cnt = material_metrics.get('show_cnt',0)
                    click_cnt = material_metrics.get('click_cnt',0)
                    total_play = material_metrics.get('total_play',0)
                    play_over = material_metrics.get('play_over',0)
                    ecp_convert_cnt = material_metrics.get('ecp_convert_cnt',0)

                    material_plan_info = ['标准推直播',str(advertiser_id), advertiser_name, str(plan_id), str(plan_name), str(material_id), str(material_title), source, stat_cost, pay_order_amount, prepay_and_pay_order_roi, pay_order_count, pay_order_coupon_amount,show_cnt,click_cnt,total_play,play_over,ecp_convert_cnt]

                    material_data.append(material_plan_info)

            if operation_condition:
                all_material_data.extend(material_data)

        if re_all_advertiser_info:
            all_advertiser_info = re_all_advertiser_info
        else:
            break

    def_normal.write_material_data(all_material_data,yesterday)

def live_live_material_main(access_token,yesterday):

    start_time = f'{yesterday} 00:00:00'
    #end_day=pd.Timestamp.now().normalize().strftime('%Y-%m-%d')
    end_time = f'{yesterday} 23:59:59'

    all_advertiser_info = def_normal.get_aweme_info_from_live(yesterday)

    if all_advertiser_info is None:
        print('无数据')
        return None

    all_material_data = []

    while True:

        re_all_advertiser_info = []

        for advertiser_info in all_advertiser_info:

            advertiser_id = advertiser_info[0]
            advertiser_name = advertiser_info[1]
            plan_id = advertiser_info[2]
            plan_name = advertiser_info[3]
            aweme_uid = int(advertiser_info[4])

            material_data = []

            operation_condition = 'normal'

            material_type = 'LIVE_ROOM'

            material_metrics = def_material.get_ad_material_data(access_token,advertiser_id,plan_id,aweme_uid,start_time,end_time,material_type)
            
            if material_metrics is None:
                operation_condition = None
                re_all_advertiser_info.append(advertiser_info)
                print('素材获取失败......')
                continue
            elif material_metrics == 0:
                continue
            else:
                pay_order_coupon_amount = round(material_metrics.get('pay_order_coupon_amount',0),2)
                stat_cost = round(material_metrics.get('stat_cost',0),2)
                pay_order_amount = round(material_metrics.get('pay_order_amount',0),2)
                if stat_cost != 0:
                    prepay_and_pay_order_roi = round(pay_order_amount / stat_cost, 2)
                else:
                    prepay_and_pay_order_roi = 0.00
                pay_order_count = round(material_metrics.get('pay_order_count',0),0)

                show_cnt = material_metrics.get('show_cnt',0)
                click_cnt = material_metrics.get('click_cnt',0)
                total_play = material_metrics.get('total_play',0)
                play_over = material_metrics.get('play_over',0)
                ecp_convert_cnt = material_metrics.get('ecp_convert_cnt',0)

                material_plan_info = ['标准推直播',str(advertiser_id), advertiser_name, str(plan_id), str(plan_name), str(aweme_uid), str(aweme_uid), '-', stat_cost, pay_order_amount, prepay_and_pay_order_roi, pay_order_count, pay_order_coupon_amount,show_cnt,click_cnt,total_play,play_over,ecp_convert_cnt]

                material_data.append(material_plan_info)

            if operation_condition:
                all_material_data.extend(material_data)

        if re_all_advertiser_info:
            all_advertiser_info = re_all_advertiser_info
        else:
            break

    def_normal.write_material_data(all_material_data,yesterday)