# -*- coding: utf-8 -*-
"""
@Time ： 2021/6/22 下午4:37
@Auth ： lizhouquan
@File ：get_public.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""
from Crypto.PublicKey import RSA
import base64
from Crypto.Cipher import PKCS1_v1_5
def account_encrypt(val,encode_str):
    """
    账号加密
    1,传入账号名，传入公钥
    2,使用公钥对账号进行加密，并base64编码
    :param val: 账号名称
    :param encode_str: 公钥
    :return:
    """
    encode_str = encode_str.encode()
    decode_str = base64.decodebytes(encode_str)
    key = decode_str.decode("utf8")
    publickey = RSA.importKey(key)
    # 进行加密
    pk = PKCS1_v1_5.new(publickey)
    # print("传入的用户信息：",val)
    encrypt_text = pk.encrypt(val.encode())
    # 加密通过base64进行编码
    result = base64.b64encode(encrypt_text)
    # print("rsa加密后的值：",result)
    return result.decode()

def encrypt_bytes(val,encode_str):
    """
    账号加密
    1,传入账号名，传入公钥
    2,使用公钥对账号进行加密，并base64编码
    :param val: 账号名称
    :param encode_str: 公钥
    :return:
    """
    encode_str = encode_str.encode()
    decode_str = base64.decodebytes(encode_str)
    key = decode_str.decode("utf8")
    publickey = RSA.importKey(key)
    # 进行加密
    pk = PKCS1_v1_5.new(publickey)
    # print("传入的用户信息：",val)
    encrypt_text = pk.encrypt(val)
    # 加密通过base64进行编码
    result = base64.b64encode(encrypt_text)
    # print("rsa加密后的值：",result)
    return result.decode()


def get_data_from_respone2(key,val):
    """
    解析返回体中的set-cookies中的参数值
    :param key: 参数值key
    :param val: 解析的对象
    :return:
    """
    return_data = None
    init_data = val.split(";")[0]
    key_val_data = init_data.split("&")
    Flag = True
    i = 0
    while Flag:
        if i < len(key_val_data):
            if key == key_val_data[i].split("=")[0]:
                return_data = key_val_data[i].split("=")[1]
                Flag = False
            else:
                i += 1
    print("取的键值对：%s  == %s"%(key, return_data))
    return "uniontech="+return_data
