import os

import pandas as pd

import def_normal
import def_material

def material_main(access_token,yesterday):

    start_time = f'{yesterday} 00:00:00'
    #end_day=pd.Timestamp.now().normalize().strftime('%Y-%m-%d')
    end_time = f'{yesterday} 23:59:59'

    all_advertiser_info = def_normal.get_adv_info_from_product(yesterday)

    columns = ['推广类型','账户ID', '账户名称', '计划ID', '计划名', '素材ID', '素材标题', '素材来源', '消耗', '直接成交金额', '直接成交ROI', '直接成交订单数', '成交智能优惠券', '展示次数', '点击次数', '播放次数', '播放完成数', '转化数']

    # 创建一个空的DataFrame
    material_df = pd.DataFrame(columns=columns)

    while True:

        re_all_advertiser_info = []

        for advertiser_info in all_advertiser_info:

            advertiser_id = advertiser_info[0]
            advertiser_name = advertiser_info[1]
            plan_id = advertiser_info[2]
            plan_name = advertiser_info[3]

            operation_condition = 'normal'
            adv_material_df = pd.DataFrame(columns=columns)

            for material_type in ['VIDEO','IMAGE']:

                material_info_list = def_material.get_ad_material_info(access_token,advertiser_id,plan_id,start_time,end_time,material_type)
                if material_info_list is None:
                    operation_condition = None
                    re_all_advertiser_info.append(advertiser_info)
                    print('素材获取失败......')
                    break
                elif material_info_list == 0:
                    continue

                for material_info in material_info_list:

                    if material_type == 'VIDEO':
                        material = material_info.get('material_info',{}).get('video_material',{})
                    elif material_type == 'IMAGE':
                        material = material_info.get('material_info',{}).get('image_material',{})

                    if material is None:
                        operation_condition = None
                        re_all_advertiser_info.append(advertiser_info)
                        print('素材获取失败......')
                        break

                    material_id = material.get('material_id','-')
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

                        material_plan_info = ['标准推商品',str(advertiser_id), advertiser_name, str(plan_id), str(plan_name), str(material_id), str(material_title), source, stat_cost, pay_order_amount, prepay_and_pay_order_roi, pay_order_count, pay_order_coupon_amount,show_cnt,click_cnt,total_play,play_over,ecp_convert_cnt]

                        material_plan_info_df = pd.DataFrame([material_plan_info], columns=columns)

                        # 使用 concat 将新的数据添加到原始 DataFrame，并生成新的索引
                        adv_material_df = pd.concat([adv_material_df, material_plan_info_df], ignore_index=True)
                
                if operation_condition is None:
                    break
            
            if operation_condition:
                material_df = pd.concat([material_df, adv_material_df], ignore_index=True)

        if re_all_advertiser_info:
            all_advertiser_info = re_all_advertiser_info
        else:
            break

    dir = os.path.dirname(__file__)
    filepath = os.path.join(dir,'源表','素材报表',f'素材报表-{yesterday}.xlsx')
    material_df.to_excel(filepath, index=False)

