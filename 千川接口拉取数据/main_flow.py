import os

import pandas as pd

import def_adv
from def_flow import get_flow

def flow_main(access_token, all_advertiser_info, yesterday):

    # 假设 flow 是一个空的 DataFrame，需要根据实际情况调整
    flow = pd.DataFrame(columns=['账户ID'] + ['advertiser_name'] + ['deduction_cost', 'cost', 'cash_cost', 'grant_cost', 'income', 'transfer_in', 'transfer_out', 'cash_balance', 'grant_balance', 'total_balance', 'share_cost', 'qc_aweme_cost', 'qc_aweme_cash_cost', 'qc_aweme_grant_cost', 'share_wallet_cost', 'coupon_cost'])

    keys = ['deduction_cost', 'cost', 'cash_cost', 'grant_cost', 'income', 'transfer_in', 'transfer_out', 'cash_balance', 'grant_balance', 'total_balance', 'share_cost', 'qc_aweme_cost', 'qc_aweme_cash_cost', 'qc_aweme_grant_cost', 'share_wallet_cost', 'coupon_cost']

    for advertiser_info in all_advertiser_info:
        advertiser_id = advertiser_info.get('advertiser_id')
        advertiser_name = advertiser_info.get('advertiser_name')

        if advertiser_id is None or advertiser_name is None:
            continue

        flow_info = get_flow(access_token, advertiser_id, yesterday, yesterday)
        if flow_info is None:
            return None
        elif flow_info == 0:
            format_flow_info = {key: 0 for key in keys}
        else:
            format_flow_info = {key: flow_info[key] / 100000 for key in keys}
        
        format_flow_info['账户ID'] = str(advertiser_id)
        format_flow_info['advertiser_name'] = advertiser_name

        # 使用 pd.concat 替代 append
        new_row = pd.DataFrame([format_flow_info])
        flow = pd.concat([flow, new_row], ignore_index=True)

    column_mapping = {'advertiser_name': '账户名称', 'deduction_cost': '消返红包消耗', 'cost': '余额总消耗', 'cash_cost': '非赠款消耗', 'grant_cost': '赠款消耗', 'income': '总存入', 'transfer_in': '总转入', 'transfer_out': '总转出', 'cash_balance': '非赠款余额', 'grant_balance': '赠款余额', 'total_balance': '总余额', 'share_cost': '共享赠款消耗', 'qc_aweme_cost': '随心推消耗', 'qc_aweme_cash_cost': '随心推非赠款消耗', 'qc_aweme_grant_cost': '随心推赠款消耗', 'share_wallet_cost': '共享钱包消耗', 'coupon_cost': '优惠券消耗'}

    # 重命名 DataFrame 的列名
    flow_renamed = flow.rename(columns=column_mapping)
    # 去重所有列
    flow_renamed = flow_renamed.drop_duplicates()

    # 检查目录是否存在，如果不存在则创建
    dir_path = os.path.dirname(__file__)
    output_dir = os.path.join(dir_path, '财务流水')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        output_file = os.path.join(output_dir, f'财务流水-{yesterday}.xlsx')
        flow_renamed.to_excel(output_file, index=False)
    except Exception as e:
        print(f"导出文件时出错: {e}")