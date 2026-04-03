import hashlib
import base64
from urllib import parse


def method_256(str):

    secret = "1D1z0Aoj00mhI3vY"
    str = str + secret
    # print("str", str)
    hd = hashlib.sha256(str.encode("utf-8")).digest()
    # print(hd)

    sig = base64.b64encode(hd)
    dataEncrypt = parse.quote(sig)

    # 加密后的内容
    return dataEncrypt



def method_systemupdatelogs(str):

    secret = "okaW1Z1F1Qkq8LuT"
    str = str + secret
    # print("str", str)
    hd = hashlib.sha256(str.encode("utf-8")).digest()
    # print(hd)

    sig = base64.b64encode(hd)
    dataEncrypt = parse.quote(sig)

    # 加密后的内容
    return dataEncrypt





if __name__ ==  "__main__":
    data = '[{"customer_name": "设天北铁我识","message_id": "97","license_machine_id": "72","status": 1},{"license_machine_id": "49","status": 1,"customer_name": "安始日自专","message_id": "52"}]'
    cc=method_256(data)
    # print(cc)

