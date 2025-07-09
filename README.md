

# Get_Qianchuan

千川商品和直播的消耗明细接口拉取

## 项目简介

本项目旨在通过调用千川平台相关接口，自动拉取商品与直播的消耗明细数据，便于数据分析与业务决策。项目支持定时任务、数据保存、异常处理等功能，适合数据分析师和开发者二次开发与集成。

## 主要功能

- 自动化获取千川商品消耗明细
- 自动化获取千川直播消耗明细
- 数据可保存为本地文件（如 CSV/Excel）
- 支持接口调用异常处理与重试机制
- 代码结构清晰，便于扩展

## 环境要求

- Python 3.7 及以上
- 推荐使用虚拟环境（venv 或 conda）

## 依赖库

请先安装依赖库，可直接使用 pip 安装：

```bash
pip install -r requirements.txt
```

常用依赖（如有不同请按实际 requirements.txt 为准）：

- requests
- pandas
- openpyxl
- tqdm
- jupyter

## 使用方法

### 1. 配置接口参数

请在 `config.py` 或 `.env` 文件中填写千川接口所需的参数，如 AccessToken、AppID、Secret 等。

```python
# config.py 示例
ACCESS_TOKEN = 'your_access_token'
APP_ID = 'your_app_id'
APP_SECRET = 'your_app_secret'
```

### 2. 拉取商品消耗明细

```python
from qianchuan import fetch_goods_report

# 示例调用
fetch_goods_report(date='2024-07-01')
```

### 3. 拉取直播消耗明细

```python
from qianchuan import fetch_live_report

# 示例调用
fetch_live_report(date='2024-07-01')
```

### 4. 数据保存与分析

数据默认保存在 `output/` 目录下（如有不同请按实际目录为准），支持 CSV/Excel 格式。可用 pandas 进一步分析。

```python
import pandas as pd

df = pd.read_csv('output/goods_report_2024-07-01.csv')
print(df.head())
```

### 5. Jupyter Notebook 演示

本项目附带 Jupyter Notebook 示例，便于交互式探索数据。运行方法：

```bash
jupyter notebook
```

打开 `example.ipynb` 并按需修改参数运行。

## 目录结构

```text
Get_Qianchuan/
├── qianchuan/           # 核心代码包
│   ├── __init__.py
│   ├── goods.py         # 商品明细相关
│   ├── live.py          # 直播明细相关
├── output/              # 数据输出目录
├── example.ipynb        # Jupyter Notebook 示例
├── requirements.txt     # 依赖说明
├── config.py            # 配置文件
├── README.md
```

## 注意事项

- 接口有调用频率和权限限制，建议合理设置定时任务频率
- AccessToken 等信息请妥善保管，避免泄露
- 如需定制化开发，请参考源码注释

## 常见问题 FAQ

**Q: 如何获取千川 AccessToken？**  
A: 请参考千川开放平台的官方文档，完成开发者认证后即可获取。

**Q: 数据拉取失败怎么办？**  
A: 请检查网络、参数配置以及接口权限，日志会输出具体的错误信息。

## 贡献方式

欢迎提交 Issue 和 Pull Request，提出你的宝贵建议或补丁！

## 许可证

本项目采用 MIT License。

---

如需进一步个性化（如添加接口文档、参数列表、运行截图等），请提供相关内容，我可以帮你补充！
