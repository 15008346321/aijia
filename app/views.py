import os
import re
from datetime import datetime
from utils import status_code
from utils.functions import random_check_code, is_login
from flask import Blueprint, request, render_template,\
    redirect, url_for, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

from app.form import UserRegisterForm
from app.models import User, db, House, Facility, HouseImage, Order
from utils.settings import MEDIA_PATH, UPLOAD_DIR

blue = Blueprint('user', __name__)


# +++++++++++++++++++++++++++++++++++++++++++++登录注册主页++++++++++++++++++++++++++++++++++++++++++++++++++
@blue.route('/create_db/')
def create_db():
    db.create_all()
    return 'success'


# 注册
@blue.route('/register/', methods=['GET', 'POST'])
def register():

    if request.method == 'GET':
        check_code = random_check_code()
        return render_template('register.html',check_code=check_code)

    if request.method == 'POST':
        mobile = request.form.get('mobile')
        imagecode = request.form.get('imagecode')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if mobile:
            pass
        else:
            return jsonify({'code': 10001, 'msg': '该手机号已注册'})
        if imagecode == session['check_code']:
            pass
        else:
            return jsonify({'code': 10002, 'msg': '验证码错误'})
        if password == password2:
            # 保存
            user = User()
            user.phone = mobile
            user.pwd_hash = generate_password_hash(password)
            user.add_update()
            return jsonify({'code':200, 'msg': '注册成功'})
        else:
            return jsonify({'code':10003, 'msg': '密码不一致'})


# 登录
@blue.route('/login/', methods=['GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')


@blue.route('/login/', methods=['POST'])
def my_login():
    if request.method == 'POST':
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        # 校验字段的完整性
        if not all([mobile, password]):
            return jsonify({'code': 10001, 'msg': '请填写完整参数'})
        # 判断用户是否注册
        user = User.query.filter(User.phone==mobile).first()
        if not user:
            return jsonify({'code': 10002, 'msg': '用户没有注册请去注册'})
        # 校验密码
        if not check_password_hash(user.pwd_hash, password):
            return jsonify({'code': 10003, 'msg': '密码不正确'})
        session['user_id'] = user.id
        user_avatar = user.avatar
        return jsonify({'code': 200, 'msg': '请求成功'})


# app主页
@blue.route('/index/')
def index():
    try:
        if session['user_id']:
            user = User.query.filter(User.id == session['user_id']).first()
            return render_template('index.html', user=user )
    except:
        return render_template('login.html')


@blue.route('/index_info/')
def index_info():
    latest_three_house = House.query.filter().order_by('-id')[0:3]
    three_house = [house.to_dict() for house in latest_three_house]
    return jsonify(code=status_code.SUCCESS, three_house=three_house)


# 注销
@blue.route('/logout/', methods=['GET'])
@is_login
def user_logout():
    session.clear()
    # return redirect(url_for('user.login'))
    return jsonify(status_code.SUCCESS)
# +++++++++++++++++++++++++++++++++++++++++++++++用户界面++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# 用户主页
@blue.route('/my/', methods=['GET', 'POST'])
@is_login
def my():
    if request.method == 'GET':
        if session['user_id']:
            user = User.query.filter(User.id == session['user_id']).first()
            return render_template('my.html', name=user.name, mobile=user.phone, avatar=user.avatar)
        else:
            return render_template('login.html')


# 用户信息修改
@blue.route('/profile/', methods=['GET', 'POST'])
@is_login
def profile():
    if request.method == 'GET':
        user = User.query.filter(User.id == session['user_id']).first()
        return render_template('profile.html', user=user)

    if request.method == 'POST':
        name = request.form.get('username')
        avatar = request.files.get('avatar')
        if avatar:
            path = os.path.join(MEDIA_PATH, avatar.filename)
            avatar.save(path)
            user = User.query.filter(User.id==session['user_id']).first()
            user.avatar = avatar.filename
            user.add_update()
            return jsonify({'code': 200, 'msg': '保存成功'})
        if name:
            user = User.query.filter(User.id == session['user_id']).first()
            user.name = name
            user.add_update()
            return jsonify({'code': 200, 'msg': '保存成功'})


# 实名认证
@blue.route('/auth/', methods=['GET', 'POST'])
@is_login
def auth():
    if request.method == 'GET':
        user = User.query.filter(User.id == session['user_id']).first()
        real_name = user.id_name
        id_card = user.id_card
        if ([real_name, id_card]):
            return render_template('auth.html', user=user, real_name=real_name, id_card=id_card)

    if request.method == 'POST':
        real_name = request.form.get('real_name')
        id_card = request.form.get('id_card')

        if not all([real_name, id_card]):
            return jsonify({'code':10001, 'msg':'请输入完整信息'})

        if not re.match(r'^[1-9]\d{17}$', id_card):
            return jsonify({'code':10002, 'msg':'身份证不符合规范'})

        user = User.query.get(session['user_id'])
        user.id_name = real_name
        user.id_card = id_card
        user.add_update()
        return jsonify({'code': 200, 'msg': '信息上传成功'})


# 我的房源
@blue.route('/myhouse/', methods=['GET'])
@is_login
def myhouse():
    if request.method == 'GET':
        user = User.query.filter(User.id == session['user_id']).first()
        real_name = user.id_name
        id_card = user.id_card
        if real_name != '' and id_card != '':
            return render_template('myhouse.html', auth=1)
        else:
            return render_template('myhouse.html', unauth=1)


# 我的房源简单信息
@blue.route('/house_info/', methods=['GET'])
@is_login
def house_info():
    user = User.query.get(session['user_id'])
    if user.id_card:
        # 实名认证成功
        houses = House.query.filter(House.user_id == session['user_id']).order_by('-id')
        houses_list = [house.to_dict() for house in houses]
        return jsonify({'code': 200, 'houses_list': houses_list})
    else:
        return jsonify({'unauth':1})


# 发布新房源
@blue.route('/newhouse/', methods=['GET', 'POST'])
@is_login
def newhouse():
    if request.method == 'GET':
        return render_template('newhouse.html')

    if request.method == 'POST':
        house_dict = request.form

        house = House()
        house.user_id = session['user_id']
        house.area_id = house_dict.get('area_id')  # 所在城区
        house.title = house_dict.get('title')  # 房屋标题
        house.price = house_dict.get('price')  # 每晚入住价格
        house.address = house_dict.get('address')  # 详细地址
        house.room_count = house_dict.get('room_count')  # 出租房间数目
        house.acreage = house_dict.get('acreage')  # 房屋面积
        house.unit = house_dict.get('unit')  # 户型描述
        house.capacity = house_dict.get('capacity')  # 宜住人数
        house.beds = house_dict.get('capacity')  # 卧床配置
        house.deposit = house_dict.get('deposit')  # 押金数额
        house.min_days = house_dict.get('min_days')  # 最少入住天数
        house.max_days = house_dict.get('max_days')  # 最多入住天数

        facilitys = house_dict.getlist('facility')
        for facility_id in facilitys:
            facility = Facility.query.get(facility_id)
            house.facilities.append(facility)
        house.add_update()
        return jsonify({'code':200, 'house_id': house.id})


# 新房源图片
@blue.route('/house_images/', methods=['POST'])
@is_login
def house_images():
    # 创建房屋图片
    house_id = request.form.get('house_id')
    image = request.files.get('house_image')

    # 保存图片  /static/media/upload/xxx.jpg
    save_url = os.path.join(UPLOAD_DIR, image.filename)
    image.save(save_url)
    # 保存房屋和图片信息
    house_image = HouseImage()
    house_image.house_id = house_id
    image_url = os.path.join('upload', image.filename)
    house_image.url = image_url
    house_image.add_update()
    # 创建房屋首图
    house = House.query.get(house_id)
    if not house.index_image_url:
        house.index_image_url = image_url
        house.add_update()
    return jsonify({'code':200, 'image_url':image_url})


# 房屋详细
@blue.route('/detail/', methods=['GET'])
def detail():
    return render_template('detail.html')


@blue.route('/house_detail/<int:id>/', methods=['GET'])
def house_detail(id):
    house = House.query.get(id)
    house_info = house.to_full_dict()
    booking = 1
    try:
        if session['user_id']:
            if house.user_id == session['user_id']:
                return jsonify(code=status_code.OK, house_info=house_info)
            else:
                return jsonify(code=status_code.OK, house_info=house_info, booking=booking)
    except:
        return jsonify(code=status_code.OK, house_info=house_info, booking=booking)


# +++++++++++++++++++++++++++++++++++++++++++++订单++++++++++++++++++++++++++++++++++++++++++++++++++


# 预定页面
@blue.route('/booking/', methods=['GET'])
@is_login
def booking():
    if request.method == 'GET':
        return render_template('booking.html')


@blue.route('/booking_info/', methods=['GET', 'POST'])
def booking_info():
    if request.method == 'GET':
        house_id = request.form.get('id')
        house_info = House.query.filter(id=house_id).to_full_dict()
        return jsonify({'code': 200, 'house_info': house_info})

    if request.method == 'POST':
        begin_date = datetime.strptime(request.form.get('begin_date'), '%Y-%m-%d')
        end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
        user_id = session['user_id']
        house_id = request.form.get('house_id')
        house = House.query.get(house_id)
        house_price = house.price

        order = Order()
        order.house_price = house_price
        order.user_id = user_id
        order.house_id = house_id
        order.begin_date = begin_date
        order.end_date = end_date
        order.days = (end_date - begin_date).days +1
        order.amount = order.days * house.price
        order.add_update()
        return jsonify(status_code.SUCCESS)


# 主页搜索
@blue.route('/search/', methods=['GET'])
def search():
    if request.method == 'GET':
        return render_template('search.html')


@blue.route('/search_info/', methods=['GET'])
def search_info():
    if request.method == 'GET':
        houses = House.query.filter().order_by('-id')
        houses_list = [house.to_dict() for house in houses]
        return jsonify({'code': 200, 'houses_list': houses_list})


# 我的订单
@blue.route('/orders/', methods=['GET'])
def orders():
    return render_template('orders.html')


# 我定别人的房子,下单客户id为我的id
@blue.route('/orders_info/', methods=['GET'])
def orders_info():
    orders = Order.query.filter(Order.user_id==session['user_id'])
    order_list = [order.to_dict() for order in orders]
    return jsonify(code=status_code.OK, order_list=order_list)


# 客户订单
@blue.route('/lorders/', methods=['GET'])
def lorders():
    return render_template('lorders.html')


# 别人定别我的房子,房源id为我的房源的id
@blue.route('/lorders_info/', methods=['GET'])
def lorders_info():
    houses = House.query.filter(House.user_id == session['user_id'])
    my_houses_id = [house.id for house in houses]
    lorders = Order.query.filter(Order.house_id.in_(my_houses_id))
    lorder_list = [lorder.to_dict() for lorder in lorders]
    return jsonify(code=status_code.OK, lorder_list=lorder_list)