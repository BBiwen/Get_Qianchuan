from datetime import datetime

import def_normal
import def_adv
import def_aweme

def aweme_main(aweme_access_token,yesterday):

    ori_advertiser_info = def_normal.get_adv_info_from_flow(yesterday)
    
    marketing_goals = ['VIDEO_PROM_GOODS','LIVE_PROM_GOODS']

    for marketing_goal in marketing_goals:

        #初始化账户信息列表
        all_advertiser_info = ori_advertiser_info
        datafile = []

        #推广类型/营销目标
        if marketing_goal == 'VIDEO_PROM_GOODS':
            marketing_type = '标准推商品'
        elif marketing_goal == 'LIVE_PROM_GOODS':
            marketing_type = '标准推直播'

        while True:
            #异常处理id列表，用于存储请求报错的id，以便再次请求
            re_advertiser_info = []

            order_platform = 'ECP_AWEME'

            for advertiser_info in all_advertiser_info:

                advertiser_id = advertiser_info[0]
                advertiser_name = advertiser_info[1]

                Operation_status = 'normal'
                advertiser_main_list = []

                cost = def_adv.get_advertiser_cost(aweme_access_token,advertiser_id,yesterday,yesterday,marketing_goal,order_platform)
                if cost is None:
                    re_advertiser_info.append(advertiser_info)
                    continue
                elif cost == 0:
                    continue

                order_info_list = def_aweme.get_order_info(aweme_access_token,yesterday,yesterday,advertiser_id,marketing_goal)
                if order_info_list is None:
                    re_advertiser_info.append(advertiser_info)
                    continue

                for aweme_order in order_info_list:

                    #计划消耗
                    stat_cost = aweme_order['stat_cost']
                    if stat_cost == 0:
                        break
                    
                    #随心推订单ID
                    order_id = aweme_order['order_id']
                    #计划ID
                    ad_id = aweme_order['ad_id']

                    order_detail = def_aweme.get_order_detail(aweme_access_token,order_id,advertiser_id)
                    if order_detail is None:
                        Operation_status = None
                        re_advertiser_info.append(advertiser_info)
                        break
                    
                    #抖音ID
                    aweme_id = order_detail['aweme_id']
                    #抖音名称
                    aweme_name = order_detail['aweme_name']
                    #抖音UID
                    aweme_uid = order_detail['aweme_uid']
                    #商品ID
                    product_id = order_detail['product_id']
                    #商品名称
                    product_name = order_detail['product_name']
                    #截取日期中的月份与日期
                    order_create_time = order_detail['order_create_time']
                    date_part, time_part = order_create_time.split(' ')
                    #将原始日期字符串解析为日期对象
                    date_object = datetime.strptime(date_part, '%Y-%m-%d')
                    #重新格式化日期对象为所需的格式，并确保结果是字符串
                    formatted_date_string = date_object.strftime('%m.%d')

                    #计划名称
                    ad_name = f'小店推广_{formatted_date_string}_短视频带货_{time_part}_{order_id}'

                    #直接成交金额
                    pay_order_amount = aweme_order['pay_order_amount']
                    #点击率(%)
                    ctr=aweme_order['ctr']
                    #点击次数
                    click_cnt=aweme_order['click_cnt']
                    #展示次数
                    show_cnt=aweme_order.get('show_cnt',0)
                    #播放数
                    total_play=aweme_order.get('total_play',0)
                    #5s播放数
                    play_duration_5s_rate=aweme_order.get('play_duration_5s_rate',0)
                    if total_play == 0:
                        play_duration_5s = 0
                    else:
                        play_duration_5s = int(float(play_duration_5s_rate)*float(total_play))
                    #直接支付ROI
                    prepay_and_pay_order_roi=aweme_order['prepay_and_pay_order_roi']
                    #直接成交订单数
                    pay_order_count=aweme_order['pay_order_count']
                    #7日总支付ROI
                    all_order_pay_roi_7days=0
                    #7日间接成交金额(元)
                    indirect_order_pay_gmv_7days=0
                    #转化数
                    attribution_convert_cnt=aweme_order['ecp_convert_cnt']
                    #转化率(%)
                    if click_cnt == 0:
                        attribution_convert_rate = 0
                    else:
                        attribution_convert_rate=float(aweme_order['ecp_convert_cnt'])/float(click_cnt)
                    #转化成本(元)
                    attribution_convert_cost=aweme_order['ecp_cpa_platform']
                    #整体订单成交成本
                    total_cost_per_pay_order_for_roi2 = 0 if pay_order_count == 0 else round(stat_cost / pay_order_count, 2)

                    ad_detail = [marketing_type, advertiser_name, str(advertiser_id), str(ad_id), ad_name,str(product_id), product_name, str(aweme_id), aweme_name, yesterday,stat_cost, show_cnt, ctr, click_cnt,attribution_convert_cnt, attribution_convert_rate, attribution_convert_cost,all_order_pay_roi_7days,pay_order_count, pay_order_amount, prepay_and_pay_order_roi,0, 0, 0,indirect_order_pay_gmv_7days,total_play, play_duration_5s, 0,'小店随心推', str(aweme_uid), 0, total_cost_per_pay_order_for_roi2]
                    #将数组存入总数组中
                    advertiser_main_list.append(ad_detail)

                if Operation_status:
                    datafile.extend(advertiser_main_list)

            if re_advertiser_info:
                all_advertiser_info = re_advertiser_info
            else:
                break

        #汇总后一起导出数据
        def_normal.write_data(datafile,yesterday)
