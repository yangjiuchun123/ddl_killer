import base64

from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

key = b'-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQCt1/hVqW9pxTAp6vbJu5+5myvAF8wvsEqM7FdIAKe5hhD1paQh\nPcG/RkPFzQG1u0jeQcwNJIddhmk/jqAK0v2GbHhVUEw/rQ8AATFxLTitXWhjFPC2\nquAlGRzRby4LALxlWBziGNzKU6BERsI1nawJb1Ifi/+q/qgZMCAGKY1EAwIDAQAB\nAoGABp4Tk8vEWKqGf9RGUYa1AfPc5g4K/r9xono68gm3xnhKt4zSeee+oL7osmQn\nQF3ckzy+PU3V9CdNiXtlrsheveC1l88wgirqg5F80W6DTY9X8ZgYzU8hppyCzuaz\ntNIHaMbTuaHnolIpRMxjwbwZYuA48osefsHr/DiL+VjbgEECQQDJ4v3wuJH85M99\nb13FPLVxLXK+qOV6QNfI5vz/tUiWaxctTPu2w48Ft6tH+fp0i8LSgCW2587vjMK1\nKCLqkxwhAkEA3HC6JHsaCZOsjJKlTuZPDTEfkOSPPk3DN+BWQI6x9xHg8aHdoBxJ\neMkzdEP9Md2MTOKUdGUODKBb1cssF477owJBALb2kvGQNC4fJ7QkM7VG2aEicTU9\nWAs9rNIUFQGhR5GaqDyT4iO2g23JEN+AO21YJE4leQiUeMQ8q1EGeO5iOEECQCyD\njvMi8KUSbvuL+VmvZDMzwj4OCWb5aPx1jrVGm2Va9OOWXhyg2a1MY9mMiSpypIw6\nDORcK7QdBa5scqDnPKUCQFQN75mXm21IMYwnAaiikZatsAoh2BdUQR+GmMVECxf2\nJswmQCyFRcc2wd2bDYvE+7tXkkr2gClVPDf9e2Y4DC4=\n-----END RSA PRIVATE KEY-----'

def creat_key():
    """
    生成密钥对
    :return:
    """
    # 伪随机数的方式生成RSA公私钥对
    random_generator = Random.new().read
    rsa = RSA.generate(1024, random_generator)
    # 私钥
    pri_key = rsa.exportKey().decode('utf-8')
    # 公钥
    pub_key = rsa.publickey().exportKey().decode('utf-8')

    # 以列表形式返回密钥对
    return [pri_key, pub_key]


def decode(input_data):
    """
    解密数据
    :param input_data:
    :param key:
    :return:
    """
    try:
        # 分组解密默认长度128
        default_length = 128
        # 创建私钥对象
        pri_key = RSA.importKey(key.decode('utf-8'))
        cipher = PKCS1_v1_5.new(pri_key)
        # 现将base64编码格式的数据解码，然后解密，并用decode转成str
        input_data_b64 = base64.b64decode(input_data.encode('utf-8'))
        # 获取密文长度
        length = len(input_data_b64)
        # 直接解密
        if length < default_length:
            output_data = cipher.decrypt(input_data_b64, sentinel='error').decode('utf-8')
        # 分组解密
        else:
            offset = 0
            res = []
            while length - offset > 0:
                if length - offset > default_length:
                    res.append(cipher.decrypt(input_data_b64[offset: offset + default_length], sentinel='error'))
                else:
                    res.append(cipher.decrypt(input_data_b64[offset:], 'error'))
                offset += default_length
            output_data = b''.join(res)
            output_data = output_data.decode('utf-8')
        # print(output_data)
        return output_data
    except Exception as e:
        # print(e)
        return e
