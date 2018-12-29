import random
from flask import session, redirect, url_for
from functools import wraps


def get_sqlalchemy_uri(DATABASE):
    # mysql+pymysql://rott:123456@127.0.0.1:3306/flask7
    user = DATABASE['USER']
    password = DATABASE['PASSWORD']
    host = DATABASE['HOST']
    port = DATABASE['PORT']
    name = DATABASE['NAME']
    engine = DATABASE['ENGINE']
    driver = DATABASE['DRIVER']
    return '%s+%s://%s:%s@%s:%s/%s' % (engine, driver,
                                       user, password,
                                       host, port, name)


def random_check_code():
    list1 = []
    for i in range(4):
        statu = random.randint(1, 2)
        if statu == 1:  # 随机小写字母
            a = random.randint(97, 122)
            a_chr = chr(a)
            list1.append(a_chr)
        elif statu == 2:  # 0-9的随机数
            r = random.randint(0, 9)
            list1.append(str(r))
    check_code = "".join(list1)
    session['check_code'] = check_code
    return check_code


def is_login(view_func):
    """
    装饰器用于登录验证
    session['user_id']
    """
    @wraps(view_func)
    def check_login(*args, **kwargs):
        # 验证登录
        if 'user_id' in session:
            return view_func(*args, **kwargs)
        else:
            # 验证失败
            return redirect(url_for('user.login'))
    return check_login