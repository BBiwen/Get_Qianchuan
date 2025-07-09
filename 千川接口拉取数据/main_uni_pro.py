import def_normal
import def_uni_all
import def_plan

def uni_pro_main(plan_access_token,yesterday):

    start_date = f'{yesterday} 00:00:00'
    end_date = f'{yesterday} 23:59:59'

    ori_advertiser_info = def_normal.get_adv_info_from_flow(yesterday)

    marketing_goal = 'VIDEO_PROM_GOODS'

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

            all_ad_list = def_uni_all.get_uni_pro_mertics(plan_access_token, advertiser_id, start_date, end_date)
            if all_ad_list is None:
                re_advertiser_info.append(advertiser_info)
                continue
            
            Operation_status = 'normal'

            for ad_list in all_ad_list:

                #获取计划ID，若是获取失败则直接判定失败
                ad_id = ad_list.get('dimensions',{}).get('ad_id',{}).get('Value',None)
                if ad_id is None:
                    re_advertiser_info.append(advertiser_info)
                    Operation_status = None
                    break

                metrics = ad_list.get('metrics',{})
                stat_cost = metrics.get('stat_cost',{}).get('Value',0)
                total_cost_per_pay_order_for_roi2 = metrics.get('total_cost_per_pay_order_for_roi2',{}).get('Value',0)
                total_pay_order_count_for_roi2 = metrics.get('total_pay_order_count_for_roi2',{}).get('Value',0)
                total_pay_order_coupon_amount_for_roi2 = metrics.get('total_pay_order_coupon_amount_for_roi2',{}).get('Value',0)
                total_pay_order_gmv_for_roi2 = metrics.get('total_pay_order_gmv_for_roi2',{}).get('Value',0)
                total_prepay_and_pay_order_roi2 = metrics.get('total_prepay_and_pay_order_roi2',{}).get('Value',0)

                ad_detail = def_plan.get_ad_detail(plan_access_token,advertiser_id,ad_id)
                if ad_detail is None:
                    re_advertiser_info.append(advertiser_info)
                    Operation_status = None
                    break

                ad_name = ad_detail.get('ad_name','')
                product_id = ad_detail.get('product_id','')
                product_name = ad_detail.get('product_name','')
                aweme_id = ad_detail.get('aweme_id','')
                aweme_name = ad_detail.get('aweme_name','')
                aweme_uid = ad_detail.get('aweme_uid','')

                temp_ad_detail = ['全域推商品',advertiser_name,advertiser_id,ad_id,ad_name,product_id,product_name,aweme_id,aweme_name,yesterday,stat_cost,0,0,0,0,0,0,0,total_pay_order_count_for_roi2,total_pay_order_gmv_for_roi2,total_prepay_and_pay_order_roi2,0,0,0,0,0,0,0,'',aweme_uid,total_pay_order_coupon_amount_for_roi2,total_cost_per_pay_order_for_roi2]

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





                    


                    


