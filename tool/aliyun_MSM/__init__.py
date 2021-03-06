# -*- coding: utf-8 -*-
import sys
from .aliyunsdkdysmsapi.request import SendSmsRequest
from .aliyunsdkdysmsapi.request import QuerySendDetailsRequest
from .aliyunsdkcore.client import AcsClient
import uuid

"""
短信业务调用接口示例，版本号：v20170525

Created on 2017-06-12

"""

REGION = "cn-hangzhou"
# ACCESS_KEY_ID/ACCESS_KEY_SECRET 根据实际申请的账号信息进行替换
ACCESS_KEY_ID = "LTAIuFzvhUVplTQT"
ACCESS_KEY_SECRET = "NnXJl91Z3AZSsTjXOWVgzVC0GMJs3r"

acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)


def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name);

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理

    return smsResponse