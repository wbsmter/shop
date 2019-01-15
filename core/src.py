from conf import settings
from lib import common
import time

logger=common.get_logger(__name__)

current_user={'user':None,'login_time':None,'timeout':int(settings.LOGIN_TIMEOUT)}
def auth(func):
    def wrapper(*args,**kwargs):
        if current_user['user']:
            interval=time.time()-current_user['login_time']
            if interval < current_user['timeout']:
                return func(*args,**kwargs)
        count = 0
        while(True):
            if count ==3:
                logger.info('禁止登陆！')
                break
            name = input('name>>: ')
            password = input('password>>: ')
            db = common.conn_db()
            if db.get(name):
                if password == db.get(name).get('password'):
                    logger.info('登录成功')
                    current_user['user']=name
                    current_user['login_time']=time.time()
                    return func(*args,**kwargs)
            else:
                logger.error('用户名不存在')
                count+=1

    return wrapper


def buy():
    prod_list = {
        1: ['洗衣机', 100],
        2: ['手机', 20],
        3: ['毛巾', 3]
    }
    name = input('name>>: ')
    db = common.conn_db()
    salary = db.get(name).get('money')
    goods=[]
    print("商品列表:\n编号  名称   价格")
    for list in prod_list:
        print('{:^2} {:^7}{:^4}'.format(list, prod_list[list][0], prod_list[list][1]))
    while (True):
        number = (input("请输入你要选择的商品编号(输入no可退出)："))
        if number == 'no':
            tag = False
            break
        number = int(number)
        if prod_list[number][1] < salary:
            salary = salary - prod_list[number][1]
            balance = salary
            goods.append(prod_list[number][0])

        else:
            print("余额不足")

@auth
def run():

    print('''
购物
查看余额
转账
    ''')
    while True:
        choice = input('>>: ').strip()
        if not choice:continue
        if choice == '1':
            buy()
