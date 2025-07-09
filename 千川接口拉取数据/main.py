import sys
import schedule
from time import sleep
from datetime import datetime
import os

import pandas as pd

import def_adv
import def_normal
from main_flow import flow_main
from main_plan import plan_main
from main_aweme import aweme_main
from main_uni_pro import uni_pro_main
from main_uni_live import uni_live_main
from main_material import material_main
from main_uni_material import uni_material_main
from main_live_material import live_video_material_main,live_live_material_main
from main_uni_live_material import uni_live_videomaterial_main,uni_live_livematerial_main
from main_rewrite_id import process_fee_data
from feishu_robot import send_robot_message

def main_main():

    # 获取昨天的日期
    yesterday = (datetime.now() - pd.Timedelta(days=1)).strftime('%Y-%m-%d')

    dir = os.path.dirname(__file__)
    filepath = os.path.join(dir,'源表','推广费',f'推广费-{yesterday}.xlsx')
    flowpath = os.path.join(dir,'财务流水',f'财务流水-{yesterday}.xlsx')
    materialpath = os.path.join(dir,'源表','素材报表',f'素材报表-{yesterday}.xlsx')

    oc_base = "oc_745798cd5df80911c0c03de40edc5b0e"
    oc_material = "oc_34bee177d975cb3a819fcf8debe937ec"

    # 从配置中获取API tokens
    tokens_dict = def_normal.get_token()
    ori_plan_tokens = tokens_dict['plan']
    ori_aweme_tokens = tokens_dict['aweme']

    # 更新计划推广的access token
    plan_appid = ori_plan_tokens['APP_ID']
    plan_secret = ori_plan_tokens['secret']
    plan_refreshtoken = ori_plan_tokens['refresh_token']
    new_plan_tokens = def_normal.re_access_token(plan_appid,plan_secret,plan_refreshtoken)
    if new_plan_tokens is not None:
        plan_access_token = new_plan_tokens[0]
        new_plan_refreshtoken = new_plan_tokens[1]
        print(plan_access_token,new_plan_refreshtoken)
        def_normal.re_refresh_token(new_plan_refreshtoken,token_type = 'plan')

    # 更新随心推的access token
    aweme_appid = ori_aweme_tokens['APP_ID']
    aweme_secret = ori_aweme_tokens['secret']
    aweme_refreshtoken = ori_aweme_tokens['refresh_token']
    new_aweme_tokens = def_normal.re_access_token(aweme_appid,aweme_secret,aweme_refreshtoken)
    if new_aweme_tokens is not None:
        aweme_access_token = new_aweme_tokens[0]
        new_aweme_refreshtoken = new_aweme_tokens[1]
        print(aweme_access_token,new_aweme_refreshtoken)
        def_normal.re_refresh_token(new_aweme_refreshtoken,token_type = 'aweme')

    # 获取店铺ID列表
    shop_id_list = def_normal.get_shop_id(plan_access_token)
    if shop_id_list is None:
        print('店铺ID获取失败')
        sys.exit()
    else:
        print(f'店铺ID获取成功: {shop_id_list}')

    # 依次执行各个模块的主函数，获取不同维度的数据
    all_advertiser_info = def_adv.get_adv_ids(plan_access_token,shop_id_list)
    if all_advertiser_info is None:
        return None

    print(f'财务流水开始:%s' % str(datetime.now()))
    flow_main(plan_access_token,all_advertiser_info,yesterday)

    # 导出推广费
    print(f'标准推广费开始:%s' % str(datetime.now()))
    plan_main(plan_access_token,yesterday)
    print(f'全域推商品开始:%s' % str(datetime.now()))
    uni_pro_main(plan_access_token,yesterday)
    print(f'全域推直播开始:%s' % str(datetime.now()))
    uni_live_main(plan_access_token,yesterday)
    print(f'标准随心推开始:%s' % str(datetime.now()))
    aweme_main(aweme_access_token,yesterday)
    process_fee_data()

    send_robot_message(flowpath,oc_base)
    send_robot_message(filepath,oc_base)

    # 导出素材数据
    print(f'标准推商品素材开始:%s' % str(datetime.now()))
    material_main(plan_access_token,yesterday)
    print(f'全域推商品素材开始:%s' % str(datetime.now()))
    uni_material_main(plan_access_token,yesterday)
    
    print(f'全域推直播素材开始:%s' % str(datetime.now()))
    uni_live_videomaterial_main(plan_access_token,yesterday)
    uni_live_livematerial_main(plan_access_token,yesterday)
    print(f'标准推直播素材开始:%s' % str(datetime.now()))
    live_video_material_main(plan_access_token,yesterday)
    live_live_material_main(plan_access_token,yesterday)

    #send_robot_message(materialpath,oc_material)

    print(f'全部数据导出完毕:%s' % str(datetime.now()))

main_main()

schedule.every().day.at("07:00").do(main_main)

while True:
    schedule.run_pending()
    sleep(30)