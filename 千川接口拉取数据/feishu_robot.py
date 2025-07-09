import json
import os
import lark_oapi as lark
from lark_oapi.api.im.v1 import CreateFileRequest, CreateFileRequestBody, CreateFileResponse
from lark_oapi.api.im.v1 import CreateMessageRequest, CreateMessageRequestBody, CreateMessageResponse

def send_excel_to_feishu_group(app_id, app_secret, chat_id, file_path):
    """
    将Excel文件发送到飞书群聊
    
    参数:
    app_id: 飞书应用的App ID
    app_secret: 飞书应用的App Secret
    chat_id: 飞书群聊ID (以'oc_'开头)
    file_path: Excel文件的本地路径
    """
    # 创建飞书客户端
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()
    
    try:
        print(f"准备上传文件: {file_path}")
        
        # 确保文件存在
        if not os.path.exists(file_path):
            raise Exception(f"文件不存在: {file_path}")
        
        # 获取文件名
        file_name = os.path.basename(file_path)
        
        # 1. 上传Excel文件到飞书
        with open(file_path, 'rb') as file:
            # 构造文件上传请求
            upload_request = CreateFileRequest.builder() \
                .request_body(
                    CreateFileRequestBody.builder()
                    .file_type("xlsx")  # 根据官方示例，使用文件类型标识
                    .file_name(file_name)
                    .file(file)
                    .build()
                ) \
                .build()
            
            # 执行上传请求
            upload_response: CreateFileResponse = client.im.v1.file.create(upload_request)
            
            if not upload_response.success():
                error_msg = f"文件上传失败: 错误码 {upload_response.code}, 消息: {upload_response.msg}"
                if "invalid file_type" in upload_response.msg:
                    error_msg += "\n尝试使用 'xls' 或 'xlsx' 作为 file_type"
                raise Exception(error_msg)
            
            file_key = upload_response.data.file_key
            print(f"✅ 文件上传成功! 文件key: {file_key}")
        
        # 2. 发送文件到群聊
        send_request = CreateMessageRequest.builder() \
            .receive_id_type("chat_id") \
            .request_body(
                CreateMessageRequestBody.builder()
                .receive_id(chat_id)
                .msg_type("file")
                .content(json.dumps({"file_key": file_key}))
                .build()
            ) \
            .build()
        
        send_response: CreateMessageResponse = client.im.v1.message.create(send_request)
        
        if not send_response.success():
            error_msg = f"消息发送失败: 错误码 {send_response.code}, 消息: {send_response.msg}"
            if "no permission" in send_response.msg:
                error_msg += "\n可能原因：1. 应用缺少 'im:message' 权限\n2. 机器人未加入该群聊"
            raise Exception(error_msg)
        
        print(f"✅ Excel文件已成功发送到群聊! 消息ID: {send_response.data.message_id}")
        return True
    
    except Exception as e:
        print(f"❌ 操作失败: {str(e)}")
        print("请检查以下内容:")
        print(f"1. 应用ID: {app_id} 和密钥是否正确")
        print(f"2. 群聊ID: {chat_id} 是否有效（以'oc_'开头）")
        print(f"3. 文件路径: {file_path} 是否存在")
        print(f"4. 应用权限是否已申请并通过审批")
        print(f"5. 文件大小是否超过100MB限制")
        return False

def send_robot_message(file_path,oc_secret):
    
    APP_ID = "cli_a8b4e1580d2dd01c"       # 替换为你的飞书应用ID
    APP_SECRET = "a9fxalBOrugk5xVrJtYpSdRLNYgbQtmr"        # 替换为你的飞书应用密钥
    CHAT_ID = oc_secret        # 替换为目标群聊ID
    EXCEL_FILE = file_path  # 替换为你的Excel文件路径
    
    # ===== 执行发送 =====
    print("开始发送Excel文件到飞书群聊...")
    result = send_excel_to_feishu_group(APP_ID, APP_SECRET, CHAT_ID, EXCEL_FILE)
    
    if result:
        print("🎉 操作成功完成!")
    else:
        print("⚠️ 操作未完成，请检查错误信息")