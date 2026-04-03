iv = password[0:16]
import random
import time
import json
vi = "aaaa"+ str(random.randint(1000, 5000000))
        #系列号
        #ser = str(time.time()) + str(random.randint(1000, 5000000))
headers={}
url = "/api/v1/update/status"
data = {"sourceUrl": ["http://professional-packages-pre.chinauos.com/desktop-professional"],
    "serialNumber": vi,
"machineID": vi,
"status":0,
"msg":"",
"timestamp": 1640135630


}


data["timestamp"] = int(time.time())
dataStr = json.dumps(data)
sourceStr = iv + dataStr
encrypt = aes.encrypt(sourceStr)
with self.client.post(url=url ,data=encrypt ,headers=headers) as response:
    res = response.json()["code"]
    #进行断言
    if  int(res) == 0 :
        print('上报成功')
    else:
        print('上报失败')