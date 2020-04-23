from core import login_menu, server_menu
from lib import PublicModel
from conf import settings
import datetime
import random
import string
import os
#import sys
#sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class Log(object):
    """
    日志类
    """
    def __init__(self, log_path):
        """
        日志初始化及配置
        :param log_path:
        """
        self.standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                               '[%(levelname)s][%(message)s]'
        self.simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        self.id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'

        self.logging_dic = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': self.standard_format
                },
                'simple': {
                    'format': self.simple_format
                },
                'id_simple': {
                    'format': self.id_simple_format
                }
            },
            'filters': {},
            'handlers': {
                # 'screen': {
                #     'level': 'DEBUG',
                #     'class': 'logging.StreamHandler',
                #     'formatter': 'id_simple'
                # },
                'file': {
                    'level': 'INFO',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'formatter': 'id_simple',
                    'filename': log_path,
                    'maxBytes': 4096,
                    'backupCount': 5,
                    'encoding': 'utf-8',
                },
            },
            'loggers': {
                '': {
                    'handlers': ['file'],
                    'level': 'DEBUG',
                    'propagate': True,
                },
            },
        }


class ATMVerify(object):
    """
    用户验证类
    """

    @staticmethod
    def login():
        """
        用户登录
        :return: None
        """
        try:
            if not settings.STATE:
                card_number = int(input('\033[35m请输入银行卡卡号 >>> \033[0m'))
                password = input('\033[35m请输入银行卡密码 >>> \033[0m').strip()
                count = 3

                while count > 0:
                    count -= 1
                    verifi_code = ''
                    for _ in range(4):
                        verifi_code += random.choice(string.ascii_letters+string.digits)
                    print('验证码： {}'.format(verifi_code))
                    user_verifi = input('\033[36m请输入验证码 >>> \033[0m').strip()
                    if user_verifi == verifi_code:
                        print('\033[34m验证码输入正确\033[0m')
                        break
                    else:
                        if count == 0:
                            print('\033[31m验证码错误, 退出程序\033[0m')
                        else:
                            print('\033[31m验证码错误, 请重新输入, 还有 {} 次机会\033[0m'.format(count))

                if count != 0:
                    password_md5 = PublicModel.hash_md5(password)

                    dic = PublicModel.users_dic(card_number)

                    if dic['card_number'] == str(card_number) and dic['password'] == password_md5:
                        settings.STATE = True

                    user_log_dir = os.path.join(settings.log_path, str(card_number))
                    log_path = os.path.join(user_log_dir, 'account.log')

                    if settings.STATE:
                        PublicModel.log_record(log_path, '登录').info('用户： {} 登录成功'.format(card_number))
                        print('\033[34m登录成功\033[0m')

                    else:
                        PublicModel.log_record(log_path, '登录').warning('用户： {} 登录失败'.format(card_number))
                        print('\033[31m卡号密码错误, 请重新登录\033[0m')

                else:
                    exit()

            else:
                print('\033[31m请勿重复登录\033[0m')

        except ValueError and FileNotFoundError:
            print('\033[31m卡号或密码错误\033[0m')

    @staticmethod
    def register():
        """
        用户注册
        :return: None
        """
        if not settings.STATE:
            while True:
                card_number = ''
                for _ in range(6):
                    card_number += str(random.randint(0, 9))

                if card_number[0] == '0':
                    card_number = ''
                    card_number = card_number[1:] + str(random.randint(1, 9))

                if card_number+'.json' not in os.listdir(settings.user_path):
                    print('\033[34m您的卡号为： {}\033[0m'.format(card_number))

                    while True:
                        user_name = input('\033[35m请输入您的姓名 >>> \033[0m').strip()
                        password = input('\033[35m请输入密码 >>> \033[0m').strip()

                        if 6 <= len(password) <= 14:
                            password = PublicModel.hash_md5(password)

                            settings.user_dict['user_name'], settings.user_dict['card_number'] = user_name, card_number
                            settings.user_dict['password'], settings.user_dict['balance'] = password, 0
                            settings.user_dict['login_date'] = str(datetime.datetime.now())

                            PublicModel.write_json(card_number, settings.user_dict)

                            user_log_dir = os.path.join(settings.log_path, card_number)

                            if not os.path.exists(user_log_dir):
                                os.mkdir(user_log_dir)

                            with open(os.path.join(user_log_dir, 'account.log'), 'w', encoding='utf-8'):
                                pass

                            with open(os.path.join(user_log_dir, 'acc_flow.log'), 'w', encoding='utf-8'):
                                pass

                            print('\033[34m注册成功\033[0m')

                            break

                        else:
                            print('\033[31m密码长度在6-14范围内, 请重新输入\033[0m')
                            continue

                    break

                else:
                    continue

        else:
            print('\033[31m已在登录状态, 请勿注册\033[0m')


class ATMUserServer(object):
    """
    用户服务类
    """

    @staticmethod
    @PublicModel.auth
    def search():
        """
        查询余额
        :return: None
        """
        dic = PublicModel.users_dic(settings.user_dict["card_number"])
        balance = dic['balance']

        user_log_dir = os.path.join(settings.log_path, str(settings.user_dict['card_number']))
        log_path = os.path.join(user_log_dir, 'acc_flow.log')

        PublicModel.log_record(log_path, '查询余额').info('用户： {} 查询余额成功'.format(settings.user_dict['card_number']))

        print('\033[34m您的卡内余额为： {} 元\033[0m'.format(balance))

    @staticmethod
    @PublicModel.auth
    def withdraw():
        """
        取款
        :return: None
        """
        try:
            money_num = int(input('\033[35m请输入您的取款金额 >>> \033[0m'))
            user_dic = PublicModel.users_dic(settings.user_dict["card_number"])
            user_dic['balance'] = int(user_dic['balance'])

            if money_num > user_dic['balance']:
                print('\033[31m您的余额不足, 请重新输入取款金额\033[0m')

            else:
                confirm = input('\033[33m是否确认？( y or n ) >>> \033[0m').strip()

                if confirm == 'y':
                    user_dic['balance'] -= money_num
                    PublicModel.write_json(user_dic["card_number"], user_dic)

                    user_log_dir = os.path.join(settings.log_path, str(settings.user_dict['card_number']))
                    log_path = os.path.join(user_log_dir, 'acc_flow.log')

                    PublicModel.log_record(log_path, '取款').info('用户： {} 取款 {}元 成功'.format(
                                                                settings.user_dict['card_number'], str(money_num)))

                    print('\033[34m您当前余额为： {} 元\033[0m'.format(user_dic['balance']))

                elif confirm == 'n':
                    pass

                else:
                    print('\033[31m输入错误\033[0m')

        except ValueError:
            print('\033[31m输入非法\033[0m')

    @staticmethod
    @PublicModel.auth
    def deposit():
        """
        存款
        :return: None
        """
        try:
            deposit_num = int(input('\033[35m请输入存款的钱数 >>> \033[0m'))

            user_dic = PublicModel.users_dic(settings.user_dict["card_number"])
            user_dic['balance'] = int(user_dic['balance'])
            user_dic['balance'] += deposit_num
            PublicModel.write_json(user_dic["card_number"], user_dic)

            user_log_dir = os.path.join(settings.log_path, str(settings.user_dict['card_number']))
            log_path = os.path.join(user_log_dir, 'acc_flow.log')

            PublicModel.log_record(log_path, '存款').info('用户： {} 存款 {}元 成功'.format(
                                                                settings.user_dict['card_number'], str(deposit_num)))

            print('\033[34m存款成功\033[0m')

        except ValueError:
            print('\033[31m输入非法\033[0m')

    @staticmethod
    @PublicModel.auth
    def transfer():
        """
        转账
        :return: None
        """
        account_id = int(input('\033[35m请输入对方银行卡号 >>> \033[0m'))

        if os.path.exists(os.path.join(settings.user_path, str(account_id) + '.json')):
            user_dic = PublicModel.users_dic(settings.user_dict["card_number"])
            user_dic['balance'] = int(user_dic['balance'])

            transfer_num = int(input('\033[37m请输入转账金额 >>> \033[0m'))

            if transfer_num > user_dic['balance']:
                print('\033[31m当前账户余额不足\033[0m')

            else:
                user_dic = PublicModel.users_dic(account_id)
                user_dic['balance'] = int(user_dic['balance'])
                user_dic['balance'] += transfer_num
                PublicModel.write_json(account_id, user_dic)

                user_dic = PublicModel.users_dic(settings.user_dict['card_number'])
                user_dic['balance'] = int(user_dic['balance'])
                user_dic['balance'] -= transfer_num
                PublicModel.write_json(settings.user_dict['card_number'], user_dic)

                user_log_dir = os.path.join(settings.log_path, str(settings.user_dict['card_number']))
                log_path = os.path.join(user_log_dir, 'acc_flow.log')

                PublicModel.log_record(log_path, '转账').info('用户： {} 向 {} 用户, 转账 {}元 成功'.format(
                                                        settings.user_dict['card_number'], str(account_id),
                                                        str(transfer_num)))

                print('\033[34m转账成功\033[0m')

        else:
            print('\033[31m查无此账户\033[0m')

    @staticmethod
    @PublicModel.auth
    def change_pwd():
        """
        修改密码
        :return: None
        """
        user_log_dir = os.path.join(settings.log_path, str(settings.user_dict['card_number']))
        log_path = os.path.join(user_log_dir, 'account.log')

        while True:
            pwd = input('\033[35m输入新密码 >>> \033[0m').strip()
            pwd2 = input('\033[35m再次确认新密码 >>> \033[0m').strip()

            if 6 <= len(pwd) <= 14:
                if pwd == pwd2:
                    user_dic = PublicModel.users_dic(settings.user_dict['card_number'])
                    user_dic['password'] = PublicModel.hash_md5(pwd2)

                    PublicModel.write_json(user_dic['card_number'], user_dic)
                    settings.STATE = False

                    PublicModel.log_record(log_path, '改密').info('用户： {} 更改密码成功'.format(
                                                                                settings.user_dict['card_number']))
                    print('\033[34m密码修改完成, 请重新登录\033[0m')

                    break

                else:
                    print('\033[31m两次密码输入不一致, 请重新输入\033[0m')

            else:
                print('\033[31m密码格式不正确\033[0m')

    @staticmethod
    @PublicModel.auth
    def account_book():
        """
        查看流水
        :return: None
        """
        user_log_dir = os.path.join(settings.log_path, str(settings.user_dict['card_number']))
        log_path = os.path.join(user_log_dir, 'acc_flow.log')

        with open(log_path, 'r', encoding='utf-8') as f:
            for item in f:
                print(item)
    @staticmethod
    def exits():
        """
        退出
        :return: None
        """
        settings.STATE = False
        
        print("退出成功！")
       
       


       


class ATMControl(object):
    """
    ATM 总控制类
    """
    control_dic = {
        1: ATMVerify.login,
        2: ATMVerify.register,
        3: ATMUserServer.search,
        4: ATMUserServer.withdraw,
        5: ATMUserServer.deposit,
        6: ATMUserServer.transfer,
        7: ATMUserServer.change_pwd,
        8: ATMUserServer.account_book,
        9: ATMUserServer.exits
    }

    def __init__(self):
        """
        ATM 服务控制菜单初始化
        """
        login_menu()

        while True:
            server_menu()

            try:
                choose = int(input('\033[33m请输入操作选项 >>> \033[0m'))
                self.control_dic[choose]()

            except ValueError:
                print('\033[31m非法输入\033[0m')
