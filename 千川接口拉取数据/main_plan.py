import def_normal
import def_adv
import def_plan

def plan_main(plan_access_token,yesterday):

    ori_advertiser_info = def_normal.get_adv_info_from_flow(yesterday)

    #首先创建好Excel文件
    def_normal.create_plan_excel(yesterday)
    
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

            order_platform = 'QIANCHUAN'

            for advertiser_info in all_advertiser_info:

                advertiser_id = advertiser_info[0]
                advertiser_name = advertiser_info[1]

                Operation_status = 'normal'
                advertiser_main_list = []

                cost = def_adv.get_advertiser_cost(plan_access_token,advertiser_id,yesterday,yesterday,marketing_goal,order_platform)
                if cost is None:
                    re_advertiser_info.append(advertiser_info)
                    continue
                elif cost == 0:
                    continue

                ad_report = def_plan.get_ad_report(plan_access_token,advertiser_id,yesterday,yesterday,marketing_goal,order_platform)
                if ad_report is None:
                    re_advertiser_info.append(advertiser_info)
                    continue
                
                for ad_info in ad_report:

                    #判断数据返回格式，若是不是字典则返回数据错误
                    if not isinstance(ad_info, dict):
                        Operation_status = None
                        re_advertiser_info.append(advertiser_info)
                        break
                    
                    #计划消耗
                    stat_cost = ad_info['stat_cost']
                    if stat_cost == 0:
                        break

                    ad_id=ad_info['ad_id']

                    #获取计划详情数据
                    detail=def_plan.get_ad_detail(plan_access_token,advertiser_id,ad_id)
                    if detail is None:
                        Operation_status = None
                        re_advertiser_info.append(advertiser_info)
                        break

                    #账户ID
                    advertiser_id=str(advertiser_id)
                    #计划ID
                    ad_id=str(ad_id)
                    #计划名称
                    ad_name = detail['ad_name']
                    #商品id
                    product_id=detail['product_id']
                    #商品名称
                    product_name=detail['product_name']
                    #抖音号id
                    aweme_id=detail['aweme_id']
                    #抖音号名称
                    aweme_name=detail['aweme_name']
                    #抖音UID
                    aweme_uid=detail['aweme_uid']
                    #点击率(%)
                    ctr=ad_info['ctr']
                    #点击次数
                    click_cnt=ad_info['click_cnt']
                    #展示次数
                    show_cnt=ad_info['show_cnt']

                    #直接下单金额
                    create_order_amount=ad_info['create_order_amount']
                    #直接下单订单数
                    create_order_count=ad_info['create_order_count']
                    #直接下单ROI
                    create_order_roi=ad_info['create_order_roi']
                    #直接成交金额(元)
                    pay_order_amount=ad_info['pay_order_amount']
                    #直接支付ROI
                    prepay_and_pay_order_roi=ad_info['prepay_and_pay_order_roi']
                    #直接成交订单数
                    pay_order_count=ad_info['pay_order_count']
                    #7日总支付ROI
                    all_order_pay_roi_7days=ad_info['all_order_pay_roi_7days']
                    #7日间接成交金额(元)
                    indirect_order_pay_gmv_7days=ad_info['indirect_order_pay_gmv_7days']
                    #转化数
                    attribution_convert_cnt=ad_info['attribution_convert_cnt']
                    #转化率(%)
                    attribution_convert_rate=ad_info['attribution_convert_rate']
                    #转化成本(元)
                    attribution_convert_cost=ad_info['attribution_convert_cost']
                    #播放数
                    total_play=ad_info['total_play']
                    #3s播放数
                    play_duration_3s=ad_info['play_duration_3s']
                    #播放完成数
                    play_over=ad_info['play_over']
                    #广告类型
                    marketing_scene = detail['marketing_scene']
                    if marketing_scene == 'FEED':
                        marketing_scene = '通投广告'
                    elif marketing_scene == 'SEARCH':
                        marketing_scene = '搜索广告'
                    elif marketing_scene == 'SHOPPING_MALL':
                        marketing_scene = '商城广告'
                    else:
                        marketing_scene = '未知类型'
                    #成交智能优惠券
                    pay_order_coupon_amount = ad_info['pay_order_coupon_amount']
                    #整体订单成交成本
                    total_cost_per_pay_order_for_roi2 = 0 if pay_order_count == 0 else round(stat_cost / pay_order_count, 2)

                    ad_detail = [marketing_type, advertiser_name, advertiser_id, ad_id, ad_name,product_id, product_name, aweme_id, aweme_name, yesterday,stat_cost, show_cnt, ctr, click_cnt,attribution_convert_cnt, attribution_convert_rate, attribution_convert_cost,all_order_pay_roi_7days,pay_order_count, pay_order_amount, prepay_and_pay_order_roi,create_order_count, create_order_amount, create_order_roi,indirect_order_pay_gmv_7days,total_play, play_duration_3s, play_over,marketing_scene, aweme_uid, pay_order_coupon_amount,total_cost_per_pay_order_for_roi2]

                    advertiser_main_list.append(ad_detail)
                if Operation_status:
                    datafile.extend(advertiser_main_list)

            #判断报错账户ID列表是否为空
            if re_advertiser_info:
                all_advertiser_info = re_advertiser_info
            else:
                break
                
        #汇总后一起导出数据
        def_normal.write_data(datafile,yesterday)

