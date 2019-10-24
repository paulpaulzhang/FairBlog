import base64
import uuid

import config


def save_base64_img(img_info):
    ext = img_info.groupdict().get('ext')  # 后缀
    data = img_info.groupdict().get('data')  # 图片data

    image = base64.urlsafe_b64decode(data)
    filename = "{}.{}".format(uuid.uuid4(), ext)  # 文件名
    path = "{}{}".format(config.IMAGE_PATH, filename)  # 服务器图片存路径
    with open(path, mode='wb') as f:
        f.write(image)
    res_path = '{}{}'.format(config.FTP_HOST, filename)
    return res_path
