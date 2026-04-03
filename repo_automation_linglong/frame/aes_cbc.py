import base64
from Crypto.Cipher import AES
import time,json

class AESHelper():
    def __init__(self, password, iv):
        self.password = bytes(password, encoding='utf-8')
        self.iv = bytes(iv, encoding='utf-8')

    def pkcs7padding(self, text):
        """
        明文使用PKCS7填充
        最终调用AES加密方法时，传入的是一个byte数组，要求是16的整数倍，因此需要对明文进行处理
        :param text: 待加密内容(明文)
        :return:
        """
        bs = AES.block_size  # 16
        length = len(text)
        bytes_length = len(bytes(text, encoding='utf-8'))
        # tips：utf-8编码时，英文占1个byte，而中文占3个byte
        padding_size = length if(bytes_length == length) else bytes_length
        padding = bs - padding_size % bs
        # tips：chr(padding)看与其它语言的约定，有的会使用'\0'
        padding_text = chr(padding) * padding
        return text + padding_text

    def pkcs7unpadding(self, text):
        """
        处理使用PKCS7填充过的数据
        :param text: 解密后的字符串
        :return:
        """
        length = len(text)
        unpadding = ord(text[length-1])
        return text[0:length-unpadding]

    def encrypt(self, content):
        """
        AES加密
        模式cbc
        填充pkcs7
        :param key: 密钥
        :param content: 加密内容
        :return:
        """
        cipher = AES.new(self.password, AES.MODE_CBC, self.iv)
        content_padding = self.pkcs7padding(content)
        encrypt_bytes = cipher.encrypt(bytes(content_padding, encoding='utf-8'))
        result = str(base64.b64encode(encrypt_bytes), encoding='utf-8')
        return result

    def decrypt(self, content):
        """
        AES解密
        模式cbc
        去填充pkcs7
        :param key:
        :param content:
        :return:
        """
        cipher = AES.new(self.password, AES.MODE_CBC, self.iv)
        encrypt_bytes = base64.b64decode(content)
        decrypt_bytes = cipher.decrypt(encrypt_bytes)
        result = str(decrypt_bytes, encoding='utf-8')
        result = self.pkcs7unpadding(result)
        return result

if __name__ == '__main__':
    # # 密码
    # password = "1FVcC1z2G4dh1hv2TaR12o307ugbhG1B"
    # # 偏移量 取的秘钥的前16为作为向量
    # iv = password[0:16]
    # # # 加密内容
    # #source_en = '{"SerialNumber": "GT529-DLCP9-YK563-LY5A7-FAA69","MachineID":"46008be23b0c3feab69af70e2f4e8b85d3a6eecdf3d38d53f55838c7ba4ae202","Status": 0,"Msg":"","Timestamp":int(time.Now().Unix()),}'
    #
    # source = '{"SerialNumber": "O749G-CXDP5-JJ3VF-KYCY9-FAAA9","MachineID":"ea1a9d35bcf713417570f152e32d88eba3e89f428c30fad9430befc1b55fa88f","Status": 1,"Msg":"12","Timestamp":2021122110,}'
    #
    #
    # aes = AESHelper(password, iv)
    # encrypt = aes.encrypt(source)
    # decrypt = aes.decrypt(encrypt)
    # print("加密后的内容")
    # print(encrypt)
    # 密码
    password = "1FVcC1z2G4dh1hv2TaR12o307ugbhG1B"
    # 偏移量 取的秘钥的前16为作为向量
    iv = password[0:16]
    # 加密内容
    # source = '{"serialNumber": "GT529-DLCP9-YK563-LY5A7-FAA69","machineID":"46008be23b0c3feab69af70e2f4e8b85d3a6eecdf3d38d53f55838c7ba4ae202","status":       0,"msg":          "","timestamp":   1640093614}'
    rt = int(time.time())
    source = {
        'serialNumber': 'GT529-DLCP9-YK563-LY5A7-FAA69',
        'machineID': '46008be23b0c3feab69af70e2f4e8b85d3a6eecdf3d38d53f55838c7ba4ae202',
        'status': 0,
        'msg': '',
        'timestamp': 1640135630
    }

    sourceStr = json.dumps(source)

    aes = AESHelper(password, iv)
    sourceStr = iv + sourceStr

    encrypt = aes.encrypt(sourceStr)

    print("加密后的内容")
    print(encrypt)


