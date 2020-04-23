def login_menu():
    """
    菜单头部
    :return: None
    """
    print("\033[34m=" * 14, "Bank of JXY", "=" * 14, "\n")
    print("{:^42}".format("ATM"), "\n")
    print("=" * 14, "Bank of JXY\033[0m", "\033[34m=\033[0m" * 14, "\n")


def server_menu():
    """
    服务选项菜单
    :return: None
    """
    print("\033[32m=" * 16, "用户操作界面", "=" * 15, "\n")
    print("{0:2} {1:12} {2:12} {3:12}".format(" ", "1. 登录", "2. 注册", "3. 查询",), "\n")
    print("{0:2} {1:12} {2:12} {3:12}".format(" ", "4. 取款", "5. 存款", "6. 转账"), "\n")
    print("{0:2} {1:11} {2:10} {3:12}\033[0m".format(" ", "7. 修改密码", "8. 查看流水", "9. 退出"), "\n")
    print("\033[32m=\033[0m" * 43, "\n")