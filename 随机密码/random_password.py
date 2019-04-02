import random


def create_password(length: int) -> str:
    """[随机生成制定长度的密码]

    去掉易混淆的 i, l, o, z
    :param
        length: 密码长度

    :returns: 密码字符串
    """
    pass_list = list(
        "1234567890qwertyupkjhgfdsaxcvbnmABCDEFGHJKMNPQRSTUVWXY!@#$%^&*")

    return "".join([random.choice(pass_list) for _ in range(length)])


print(create_password(10))
