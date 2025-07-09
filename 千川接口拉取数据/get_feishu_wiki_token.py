import requests
import json

#获取token令牌
def get_tenant_access_token(app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {
        "app_id": app_id,
        "app_secret": app_secret
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()  # 返回的JSON中包含tenant_access_token
    else:
        print(f"Error: Received status code {response.status_code}")
        print(response.text)
        return None

#获取知识库下的表格token
#知识库：wiki，表格：sheet
def get_wiki_obj_token(access_token, wiki_node_token, obj_type="wiki"):
    url = "https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    params = {
        "token": wiki_node_token,
        "obj_type": obj_type
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data['code'] == 0:
            return data['data']['node']['obj_token']
        else:
            print(f"请求失败，错误代码：{data['code']}，错误信息：{data['msg']}")
            return None
    else:
        print(f"错误：{response.status_code}, {response.text}")
        return None

# 使用你的app_id和app_secret替换以下值
app_id = "cli_a7329bc488acd00d"
app_secret = "72HaDOdYdKhzeLX52AXWigjnHmR5VR0s"
# 输入wiki节点token值
wiki_node_token = "Bzy9wEb6QicI4TkLCRFc6yxlnw0"

token_info = get_tenant_access_token(app_id, app_secret)

if token_info and 'tenant_access_token' in token_info:
    print(f"请求成功,tenant_access_token: {token_info['tenant_access_token']}")
    tenant_access_token = token_info['tenant_access_token']
else:
    print("请求失败.")

obj_token = get_wiki_obj_token(tenant_access_token, wiki_node_token)

if obj_token:
    print(f"获取成功: {obj_token}")
else:
    print("Failed to retrieve obj_token.")