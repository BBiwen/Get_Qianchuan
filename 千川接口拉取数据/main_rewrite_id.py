import pandas as pd
import datetime
import os

def process_fee_data():

    # ================== 预处理阶段 ==================
    # 日期处理（避免重复计算）
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    formatted_yesterday = yesterday.strftime("%Y-%m-%d")

    # ================== 数据加载阶段 ==================
    # 使用OpenPyXL引擎提升读取性能
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '源表', '推广费', f'推广费-{formatted_yesterday}.xlsx')
    df = pd.read_excel(
        file_path,
        dtype={col: str for col in ['账户ID', '计划ID', '商品ID', '抖音号ID', '达人uid']},
        engine='openpyxl'
    )

    # 最终空值处理（避免多次fillna调用）
    null_mask = df[['抖音号名称','达人uid','抖音号ID']].isna().all(axis=1)
    df.loc[null_mask, ['抖音号名称','抖音号ID','达人uid']] = '无'
    
    # ================== 数据补齐优化 ==================
    # 预加载映射文件并建立双向字典
    mapping_path = os.path.join(base_dir, '抖音达人映射.csv')
    df_mapping = pd.read_csv(
        mapping_path, 
        usecols=['抖音号','抖音uid'],
        dtype={'抖音号': str, '抖音uid': str},
        encoding='GBK'
    ).apply(lambda x: x.str.strip()).drop_duplicates()
    
    # 创建复合映射字典（优先使用当日数据，其次历史映射数据）
    uid_map = pd.Series(
        df_mapping['抖音号'].values, 
        index=df_mapping['抖音uid']
    ).to_dict()
    id_map = pd.Series(
        df_mapping['抖音uid'].values, 
        index=df_mapping['抖音号']
    ).to_dict()

    # 第一轮填充：使用当日数据建立映射
    valid_mask = df[['达人uid','抖音号ID']].notna().all(axis=1)
    uid_id_map = df[valid_mask].drop_duplicates(['达人uid']).set_index('达人uid')['抖音号ID'].to_dict()
    id_uid_map = df[valid_mask].drop_duplicates(['抖音号ID']).set_index('抖音号ID')['达人uid'].to_dict()

    # 合并映射关系（当日数据优先）
    uid_map = {**uid_map, **uid_id_map}
    id_map = {**id_map, **id_uid_map}

    # 向量化填充操作
    df['抖音号ID'] = df['抖音号ID'].fillna(df['达人uid'].map(uid_map))
    df['达人uid'] = df['达人uid'].fillna(df['抖音号ID'].map(id_map))

    # 导出填充后的文件
    df.to_excel(
        file_path,
        index=False,
        engine='openpyxl'
    )

if __name__ == "__main__":
    process_fee_data()