import pandas as pd
import numpy as np
import os

args = r"C:\Users\Admin\Desktop"
month = '1月'

# 使用函数读取表格
ad_data1 = pd.read_excel(fr'{args}\月推广费\标准推广_2025-{month}.xlsx',dtype = 'str')
ad_data1['消耗(元)'] = pd.to_numeric(ad_data1['消耗(元)'], errors='coerce')
ad_data1['直接成交订单数'] = pd.to_numeric(ad_data1['直接成交订单数'], errors='coerce')
ad_data1['成交订单成本'] = np.where(ad_data1['直接成交订单数'] != 0, round(ad_data1['消耗(元)'] / ad_data1['直接成交订单数'], 2), 0)

ad_data2 = pd.read_excel(fr'{args}\月推广费\全域推直播_2025-{month}.xlsx',dtype = 'str')
ad_data2 = ad_data2.rename(columns={'整体消耗':'消耗(元)','整体成交订单数':'直接成交订单数','整体成交金额':'直接成交金额(元)','整体支付ROI':'直接支付ROI','整体成交订单成本':'成交订单成本','整体成交智能优惠券金额': '成交智能优惠券金额',})

ad_data3 = pd.read_excel(fr'{args}\月推广费\全域推商品_2025-{month}.xlsx',dtype = 'str')
ad_data3 = ad_data3.rename(columns={'整体消耗':'消耗(元)','整体成交订单数':'直接成交订单数','整体成交金额':'直接成交金额(元)','整体支付ROI':'直接支付ROI','整体成交订单成本':'成交订单成本','整体成交智能优惠券金额': '成交智能优惠券金额',})

all_data = pd.concat([ad_data1, ad_data2, ad_data3], ignore_index=True)

all_data = all_data.replace(',', '', regex=True)

for i in ['消耗(元)','点击率(%)','转化率(%)','转化成本(元)','7日总支付ROI','直接成交金额(元)','直接支付ROI','直接下单金额(元)','直接下单ROI','7日间接成交金额(元)','成交订单成本','成交智能优惠券金额']:
    all_data[i] = all_data[i].fillna(0).astype(float)

for i in ['展示次数','点击次数','转化数','直接成交订单数','直接下单订单数','播放数','3s播放数','播放完成数']:
    all_data[i] = all_data[i].fillna(0).astype(int)

# 获取所有 DataFrame 的所有唯一列
all_columns = pd.unique(
    ad_data1.columns.append(
        ad_data2.columns).append(
        ad_data3.columns)
)

# 确保基础列顺序（来自 ad_data1）保持不变，同时将新列添加到末尾
base_columns = list(ad_data1.columns)
new_columns = [col for col in all_columns if col not in base_columns]
final_columns_order = base_columns + new_columns

# 按照最终确定的列顺序调整合并后的 DataFrame
all_data_new = all_data[final_columns_order]

all_data_new = all_data_new[all_data_new['推广类型'].notna() & (all_data_new['推广类型'] != '')]

all_data_new.to_excel(fr'{args}\月推广费\推广费_2025-{month}.xlsx', index=False)