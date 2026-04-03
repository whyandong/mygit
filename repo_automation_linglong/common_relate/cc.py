import time
import requests
import json
from frame.aes_cbc import AESHelper

password = "1FVcC1z2G4dh1hv2TaR12o307ugbhG1B"
# 偏移量 取的秘钥的前16为作为向量
iv = password[0:16]
aes = AESHelper(password, iv)

headers={}
url = "https://gray-update-pre.uniontech.com/api/v1/update/status"
data = {"serialNumber":"xdhwjhdjwhdfjwh4968",
    "machineID":"dhwkhdfwhqfkwhkdfjwkdjwk2763",
    "status":0,
    "msg":"msg11111",
	"timestamp": 1640135630
}


data["timestamp"] = int(time.time())
dataStr = json.dumps(data)
sourceStr = iv + dataStr
encrypt = aes.encrypt(sourceStr)

re=requests.post(url=url ,data=encrypt ,headers=headers)
res = re.json()["code"]

print(re.json())