from datetime import datetime

import def_normal
import def_uni_all

def uni_live_main(plan_access_token,yesterday):

    start_date = f'{yesterday} 00:00:00'
    end_date = f'{yesterday} 23:59:59'

    ori_advertiser_info = def_normal.get_adv_info_from_flow(yesterday)

    marketing_goal = 'LIVE_PROM_GOODS'

    #初始化账户信息列表
    all_advertiser_info = ori_advertiser_info

    datafile = []

    while True:

        #异常处理id列表，用于存储请求报错的id，以便再次请求
        re_advertiser_info = []

        for advertiser_info in all_advertiser_info:
            
            advertiser_main_list = []

            advertiser_id = advertiser_info[0]
            advertiser_name = advertiser_info[1]
            
            cost = def_uni_all.get_uni_adv_cost(plan_access_token,advertiser_id,start_date,end_date,marketing_goal)
            if cost is None:
                re_advertiser_info.append(advertiser_info)
                continue
            elif cost == 0:
                continue

            all_ad_list = def_uni_all.get_uni_room_info(plan_access_token,advertiser_id,start_date,end_date,marketing_goal)
            if all_ad_list is None:
                re_advertiser_info.append(advertiser_info)
                continue
            
            Operation_status = 'normal'

            for ad_list in all_ad_list:

                ad_id = ad_list.get('ad_info',{}).get('id','')
                ad_name = ad_list.get('ad_info',{}).get('name','')
                room_info = ad_list.get('room_info',[])
                if room_info:
                    aweme_id = room_info[0].get('anchor_id','')
                    aweme_id = str(aweme_id)
                    aweme_name = room_info[0].get('anchor_name','')
                    aweme_name = str(aweme_name)

                stats_info = ad_list.get('stats_info',{})
                stat_cost = stats_info.get('stat_cost',0) / 100000
                if stat_cost == 0:
                    continue
                total_pay_order_count_for_roi2 = stats_info.get('total_pay_order_count_for_roi2',0)
                total_pay_order_gmv_for_roi2 = stats_info.get('total_pay_order_gmv_for_roi2',0) / 100000
                total_prepay_and_pay_order_roi2 = stats_info.get('total_prepay_and_pay_order_roi2',0)
                total_pay_order_coupon_amount_for_roi2 = stats_info.get('total_pay_order_coupon_amount_for_roi2',0) / 100000
                total_cost_per_pay_order_for_roi2 = stats_info.get('total_cost_per_pay_order_for_roi2',0) / 100000

                aweme_uid = def_uni_all.get_uni_aweme_uid(plan_access_token,advertiser_id,ad_id)
                if aweme_uid is None:
                    aweme_uid = ''
                else:
                    aweme_uid = str(aweme_uid)

                ad_id = str(ad_id)
                ad_name = str(ad_name)

                temp_ad_detail = ['全域推直播',advertiser_name,advertiser_id,ad_id,ad_name,'','',aweme_id,aweme_name,yesterday,stat_cost,0,0,0,0,0,0,0,total_pay_order_count_for_roi2,total_pay_order_gmv_for_roi2,total_prepay_and_pay_order_roi2,0,0,0,0,0,0,0,'',aweme_uid,total_pay_order_coupon_amount_for_roi2,total_cost_per_pay_order_for_roi2]

                #将数组存入总数组中
                advertiser_main_list.append(temp_ad_detail)

            if Operation_status:
                datafile.extend(advertiser_main_list)

        if re_advertiser_info:
            all_advertiser_info = re_advertiser_info
        else:
            break

    #汇总后一起导出数据
    def_normal.write_data(datafile,yesterday)




                    


                    


