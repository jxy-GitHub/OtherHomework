from conf import settings
from core import user
import logging.config
import hashlib
import json
import os


class PublicModel(object):
    """
    公共组件类
    """

    @staticmethod
    def users_dic(card_id):
        """
        读取用户信息
        :param card_id:
        :return: user_dict
        """
        with open(os.path.join(settings.user_path, str(card_id)+'.json'), 'r', encoding='utf-8') as f:
            user_dict = json.loads(f.read())
            return user_dict

    @staticmethod
    def auth(f):
        """
        判断是否登录的装饰器
        :param f:
        :return: inner
        """
        def inner():
            if settings.STATE:
                ret = f()
                return ret
            else:
                print('请先进行登录')
        return inner

    @staticmethod
    def hash_md5(info):
        """
        加密密码
        :param info:
        :return: md5.hexdigest()
        """
        md5 = hashlib.md5()
        md5.update(info.encode('utf-8'))
        return md5.hexdigest()

    @staticmethod
    def log_record(path, info):
        """
        生成日志
        :param path:
        :param info:
        :return: logger
        """
        logging.config.dictConfig(user.Log(path).logging_dic)  # 导入上面定义的logging配置
        logger = logging.getLogger(info)  # 生成一个log实例
        return logger

    @staticmethod
    def write_json(card_id, dic):
        """
        用户信息写入文件
        :param card_id:
        :param dic:
        :return: None
        """
        with open(os.path.join(settings.user_path, str(card_id) + '.json'), 'w',
                  encoding='utf-8') as f:
            f.write(json.dumps(dic))
