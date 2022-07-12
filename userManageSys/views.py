from django.http import HttpResponse
from django.shortcuts import render,redirect, HttpResponse
from intellCstSys.sql_help import insert_sql, select_target, edit_sql, select_all_target, data_center_online, data_center_history
from intellCstSys.aliyun import ChatRobot, one_chat
import time, datetime

def index(request):
    return render(request, 'userManagerSys/index.html')


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username.strip() and password:  # 确保用户名和密码都不为空
            if username[0] not in ['U', 'S', 'M']:
                return render(request, 'userManagerSys/login.html', {'message': '账号不存在'})
            if username[0] == 'U':   # user
                target = select_target("SELECT user_id, user_name, user_pwd FROM user_info WHERE user_name = %s", username)
                if target is None:
                    return render(request, 'userManagerSys/login.html', {'message': '账号不存在'})
                elif target['user_pwd'] != password:
                    return render(request, 'userManagerSys/login.html', {'message': '账号密码不一致'})
                else:
                    return redirect('/user_homepage/' + '?uid=' + str(target['user_id']))
            if username[0] == 'S':   # service
                target = select_target("SELECT service_id,service_uid, service_pwd FROM service_info1 WHERE service_uid = %s", username)
                if target is None:
                    return render(request, 'userManagerSys/login.html', {'message': '账号不存在'})
                elif target['service_pwd'] != password:
                    return render(request, 'userManagerSys/login.html', {'message': '账号密码不一致'})
                else:
                    return redirect('/service_homepage/' + '?uid=' + str(target['service_id']))
            if username[0] == 'M':   # manager
                target = select_target("SELECT manager_id,manager_uid, manager_pwd FROM manager_info WHERE manager_uid = %s", username)
                if target is None:
                    return render(request, 'userManagerSys/login.html', {'message': '账号不存在'})
                elif target['manager_pwd'] != password:
                    return render(request, 'userManagerSys/login.html', {'message': '账号密码不一致'})
                else:
                    return redirect('/manager_homepage/' + '?uid=' + str(target['manager_id']))
    return render(request, 'userManagerSys/login.html')


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pwd1 = request.POST.get('password1')
        pwd2 = request.POST.get('password2')
        email = request.POST.get('email')
        if username.strip() and pwd1 and pwd2 and email:  # 确保用户名和密码都不为空
            if username[0] != 'U' or len(username) < 10:
                return render(request, 'userManagerSys/register.html', {'msg_info1': '提示：U开头,长度为不小于10',
                                                                        'message_warning': '账号格式不正确'})
            target = select_all_target("SELECT user_name, user_pwd FROM user_info", [])
            user_name_list = [i['user_name'] for i in target]
            if username in user_name_list:
                return render(request, 'userManagerSys/register.html', {'msg_info1': '提示：U开头,长度为不小于10',
                                                                        'message_warning': '账号已存在'})
            if pwd1 != pwd2:
                return render(request, 'userManagerSys/register.html', {'msg_info1': '提示：U开头,长度为不小于10',
                                                                        'message_warning': '两次密码不一致'})
            if '@' not in email or email[-4:] !='.com':
                return render(request, 'userManagerSys/register.html', {'msg_info1': '提示：U开头,长度为不小于10',
                                                                        'message_warning': '邮箱不正确'})

            # 全部验证完成，将用户数据写入数据库
            insert_sql("insert into user_info(user_name,user_pwd,user_email) value(%s,%s,%s)",
                           [username, pwd1, email])
            return redirect('/login/')
    return render(request, 'userManagerSys/register.html', {'msg_info1': '提示：U开头,长度为不小于10'})


def edit(request):
    if request.method == "POST":
        username = request.POST.get('username')
        old_pwd = request.POST.get('old_password')
        pwd1 = request.POST.get('password1')
        pwd2 = request.POST.get('password2')
        if username.strip() and pwd1 and pwd2 and old_pwd:  # 确保用户名和密码都不为空
            if pwd1 != pwd2:
                return render(request, 'userManagerSys/edit.html', {'message_warning': '两次密码不一致'})
            if username[0] not in ['U','S','M']:
                return render(request, 'userManagerSys/edit.html', {'message_warning': '账号不存在'})
            if username[0] == 'U':
                target = select_target("SELECT user_name, user_pwd FROM user_info WHERE user_name = %s", username)
                if target is None:
                    return render(request, 'userManagerSys/edit.html', {'message_warning': '账号不存在'})
                elif target['user_pwd'] != old_pwd:
                    return render(request, 'userManagerSys/edit.html', {'message_warning': '账号密码不一致'})
                else:
                    edit_sql("update user_info set user_pwd=%s where user_name = %s", [pwd1,username])
                    return render(request, 'userManagerSys/edit.html', {'message_success': '密码修改成功'})
            if username[0] == 'S':
                target = select_target("SELECT service_uid, service_pwd FROM service_info1 WHERE service_uid = %s", username)
                if target is None:
                    return render(request, 'userManagerSys/edit.html', {'message_warning': '账号不存在'})
                elif target['service_pwd'] != old_pwd:
                    return render(request, 'userManagerSys/edit.html', {'message_warning': '账号密码不一致'})
                else:
                    edit_sql("update service_info1 set service_pwd=%s where service_uid = %s", [pwd1,username])
                    return render(request, 'userManagerSys/edit.html', {'message_success': '密码修改成功'})
            if username[0] == 'M':
                target = select_target("SELECT manager_uid, manager_pwd FROM manager_info WHERE manager_uid = %s", username)
                if target is None:
                    return render(request, 'userManagerSys/edit.html', {'message_warning': '账号不存在'})
                elif target['manager_pwd'] != old_pwd:
                    return render(request, 'userManagerSys/edit.html', {'message_warning': '账号密码不一致'})
                else:
                    edit_sql("update manager_info set manager_pwd=%s where manager_uid = %s", [pwd1, username])
                    return render(request, 'userManagerSys/edit.html', {'message_success': '密码修改成功'})
                pass
    return render(request, 'userManagerSys/edit.html')


def find(request):
    pass


def user_homepage(request):
    uid = request.GET.get('uid')
    session_id = str(time.time()).replace('.', '') + str(uid)
    return render(request, 'userManagerSys/user_homepage.html',{'uid':uid,
                                                                'sessionid':session_id})

def goods_detail(request):
    gid = request.GET.get('gid')
    uid = request.GET.get('uid')
    session_id = str(time.time()).replace('.', '') + str(uid)
    image_name_list = [['xiaomi_101', 'redmi_k40', 'Note9_pro', 'heisha'],
                       ['pro15', 'screen', 'redmiG'],
                       ['tv', 'project', 'robot'],
                       ['bracelet', 'nine_car', 'air_tool']]
    path_head = '/images/goods_images/'
    image_name = image_name_list[int(gid[0]) - 1][int(gid[1]) - 1]
    path = path_head + image_name + '.png'
    # return render(request, 'userManagerSys/goods_detail3.html', {'path': path})
    if int(gid[0]) - 1 == 0:
        return render(request, 'userManagerSys/goods_detail.html', {'path': path,
                                                                    'uid': uid,
                                                                    'sessionid':session_id})
    elif int(gid[0]) - 1 == 1:
        return render(request, 'userManagerSys/goods_detail1.html', {'path': path,
                                                                     'uid': uid,
                                                                     'sessionid':session_id})
    elif int(gid[0]) - 1 == 2:
        return render(request, 'userManagerSys/goods_detail2.html',{'path': path,
                                                                    'uid': uid,
                                                                    'sessionid':session_id})
    elif int(gid[0]) - 1 == 3:
        return render(request, 'userManagerSys/goods_detail3.html',{'path': path,
                                                                    'uid': uid,
                                                                    'sessionid':session_id})

def service_homepage(request):
    goods_list = select_all_target("SELECT goods_id, goods_name, goods_price, goods_content, goods_type_id FROM goods_info1", [])
    status = ['咨询离线', '咨询在线']
    status_tran = request.GET.get('status')
    if status_tran == '1':
        return render(request, 'userManagerSys/service_homepage.html',{'status': status[1],
                                                                       'goods_list': goods_list} )
    if status_tran == '2':
        return render(request, 'userManagerSys/service_homepage.html',{'status': status[0],
                                                                       'goods_list': goods_list} )
    return render(request, 'userManagerSys/service_homepage.html', {'status': status[1],
                                                                    'goods_list': goods_list} )

def add_goods(request):
    if request.method == "GET":
        return render(request, 'userManagerSys/add_goods.html',{'goods_names_msg': '商品名称',
                                                                'goods_price_msg': '商品价格',
                                                                'goods_content_msg': '商品描述',
                                                                'goods_type_msg': '商品类型'})
    else:
        goods_name = request.POST.get("goods_name")
        goods_price = request.POST.get("goods_price")
        goods_content = request.POST.get("goods_content")
        goods_type = request.POST.get("goods_type")
        try:
            int(goods_price)
            int(goods_type)
        except:
            message = '商品价格和商品类型应当是数字'
            return render(request, 'userManagerSys/add_goods.html',{'message': message,
                                                                    'goods_names_msg': '商品名称',
                                                                    'goods_price_msg': '商品价格',
                                                                    'goods_content_msg': '商品描述',
                                                                    'goods_type_msg': '商品类型'
                                                                    })

        insert_sql("insert into goods_info1(goods_name, goods_price, goods_content, goods_type_id) value(%s,%s,%s,%s)",
                             [goods_name, goods_price, goods_content, goods_type])
        return redirect("/service_homepage/")


def add_service(request):
    if request.method == "GET":
        return render(request, 'userManagerSys/add_service.html',{'username_msg': '客服登录名',
                                                                  'name_msg':'客服姓名',
                                                                  'password_msg':'客服密码',
                                                                  'email_msg':'客服邮箱',
                                                                  'serviceGourp_msg':'客服所属客服组'})
    else:
        username = request.POST.get("username")
        name = request.POST.get("name")
        password = request.POST.get("password")
        email = request.POST.get("email")
        serviceGourp = request.POST.get("serviceGourp")
        if username[0] != 'S' or len(username) < 10:
            return render(request, 'userManagerSys/add_service.html',{'username_msg': '客服登录名',
                                                                     'name_msg':'客服姓名',
                                                                     'password_msg':'客服密码',
                                                                     'email_msg':'客服邮箱',
                                                                     'serviceGourp_msg':'客服所属客服组',
                                                                     'message':'账号格式不正确. 提示：账号以S开头且不少于10个长度'})
        target = select_all_target("SELECT service_uid FROM service_info1", [])
        user_name_list = [i['service_uid'] for i in target]
        if username in user_name_list:
            return render(request, 'userManagerSys/add_service.html', {'username_msg': '客服登录名',
                                                                      'name_msg': '客服姓名',
                                                                      'password_msg': '客服密码',
                                                                      'email_msg': '客服邮箱',
                                                                      'serviceGourp_msg': '客服所属客服组',
                                                                      'message': '客服登录账号已存在'})
        insert_sql("insert into service_info1(service_uid, service_name, service_pwd, service_email,service_group_id) value(%s,%s,%s,%s,%s)",
                   [username, name, password, email, serviceGourp])
        return redirect("/manager_homepage/")


def del_goods(request):
    gid = request.GET.get('gid')
    insert_sql("delete from goods_info1 where goods_id = %s ", gid)
    return redirect("/service_homepage/")


def del_service(request):
    sid = request.GET.get('sid')
    insert_sql("delete from service_info1 where service_id = %s ", sid)
    return redirect("/manager_homepage/")


def edit_service(request):
    if request.method == 'GET':
        sid = request.GET.get('sid')
        target = select_target("SELECT service_id, service_uid, service_name, service_email, service_group_id FROM service_info1 WHERE service_id = %s",sid)
        return render(request, 'userManagerSys/edit_service.html', {'service_id': target['service_id'],
                                                                    'name_msg': target['service_name'],
                                                                    'email_msg': target['service_email'],
                                                                    'serviceGourp_msg': target['service_group_id']
                                                                    })
    else:
        sid = request.GET.get('sid')
        name = request.POST.get("name")
        email = request.POST.get("email")
        serviceGourp = request.POST.get("serviceGourp")
        edit_sql("update service_info1 set service_name=%s,service_email=%s,service_group_id=%s where service_id = %s",
            [name, email, serviceGourp, sid])
        return redirect("/manager_homepage/")


def edit_goods(request):
    if request.method == 'GET':
        gid = request.GET.get('gid')
        target = select_target("SELECT goods_id, goods_name, goods_price, goods_content, goods_type_id FROM goods_info1 WHERE goods_id = %s", gid)
        return render(request, 'userManagerSys/edit_goods.html', {'goods_names_msg': target['goods_name'],
                                                                  'goods_price_msg': target['goods_price'],
                                                                  'goods_content_msg': target['goods_content'],
                                                                  'goods_type_msg': target['goods_type_id'],
                                                                  'goods_id': target['goods_id']})
    else:
        gid = request.GET.get('gid')
        goods_name = request.POST.get("goods_name")
        goods_price = request.POST.get("goods_price")
        goods_content = request.POST.get("goods_content")
        goods_type = request.POST.get("goods_type")
        edit_sql("update goods_info1 set goods_name=%s,goods_price=%s,goods_content=%s,goods_type_id=%s where goods_id = %s",
                 [goods_name, goods_price, goods_content, goods_type, gid])
        return redirect("/service_homepage/")


def chat_room(request):
    """
    :param request:
    :return:
      此部分设计三个数据库的使用。
      1. 人机会话
         涉及字段：session_id    会话id     varchar(50)    - 生成逻辑 time.time + uid
                 uid           用户id     varchar(10)
                 date          日期
                 feedback      反馈       varchar(1)     -
      2. 人机对话：chat_id       对话id     varchar(50)    - 生成逻辑 time.time + uid
                 send_message  发送内容    varchar(255)
                 rsp_message   回答内容    varchar(255)
                 session_id    会话id外键  varchar(50)
                 date          日期
      3. 转人工清：request_id    转人工id    varchar(50)    - 生成逻辑 time.time + uid
                 session_id    会话id外键   varchar(50)
                 date
    """
    uid = request.GET.get('uid')
    session_id = request.GET.get('sessionid')
    date = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d")
    feedback = ''
    if request.method == "POST":
        question = request.POST.get('question')
        if question == '转人工':
            request_id = str(time.time()).replace('.', '') + str(uid)
            insert_sql("insert into transfer_service(request_id,session_id,date) value(%s,%s,%s)",
                        [request_id, session_id, date])
        if len(question) == 2 and question[1] == '分':
            # 会话结束且有反馈，更新数据库
            feedback = question[0]
            edit_sql("update robot_session set feedback=%s where session_id = %s", [feedback, session_id])
            return HttpResponse('感谢您的评价')
        else:
            chat_id = str(time.time()).replace('.', '') + str(uid)
            answer = one_chat(question)
            if answer == '这个问题我回答不了，我会尽快学习的~':
                answer_db = 'NO ANSWER'
                insert_sql(
                    "insert into robot_chat(chat_id, send_message,rsp_message,session_id,date) value(%s,%s,%s,%s,%s)",
                    [chat_id, question, answer_db, session_id, date])
            else:
                insert_sql("insert into robot_chat(chat_id, send_message,rsp_message,session_id,date) value(%s,%s,%s,%s,%s)",
                       [chat_id, question, answer, session_id, date])
            # 写入形成一次对话，写入数据库
            return HttpResponse(answer)
    if request.method == "GET":
        insert_sql("insert into robot_session(session_id,uid,date) value(%s,%s,%s)",
                   [session_id, uid, date])
        return render(request, 'userManagerSys/chat_room.html',{'uid': uid,
                                                                'sessionid': session_id})


def manager_homepage(request):
    service_list = select_all_target(
        "SELECT service_id, service_uid, service_name, service_email, service_group_id FROM service_info1", [])
    return render(request, 'userManagerSys/manage_service_homepage.html',{'service_list': service_list})


def online_data_center(request):
    result = data_center_online()[0]
    session_created_cnt = int(result['session_created_cnt'])
    session_used_cnt = int(result['session_used_cnt'])
    session_feedback_cnt = int(result['session_feedback_cnt'])
    session_transfer_cnt = int(result['session_transfer_cnt'])
    chat_cnt = int(result['chat_cnt'])
    no_answer_cnt = int(result['no_answer_cnt'])
    request_transfer_cnt = int(result['tranfer_request_cnt'])
    satisfy_feedback_cnt = int(result['satisfy_feedback_cnt'])
    simple_feedback_cnt = int(result['simple_feedback_cnt'])
    unsatisfy_feedback_cnt = int(result['unsatisfy_feedback_cnt'])
    satif_ratio = round(satisfy_feedback_cnt / session_feedback_cnt,3)
    simple_ratio = round(simple_feedback_cnt / session_feedback_cnt,3)
    unsatif_ratio = round(unsatisfy_feedback_cnt / session_feedback_cnt,3)
    return render(request, 'userManagerSys/manage_data_online.html', {'session_created_cnt':session_created_cnt,
                                                                      'session_used_cnt':session_used_cnt,
                                                                      'session_feedback_cnt':session_feedback_cnt,
                                                                      'session_transfer_cnt':session_transfer_cnt,
                                                                      'chat_cnt':chat_cnt,
                                                                      'no_answer_cnt':no_answer_cnt,
                                                                      'request_transfer_cnt': request_transfer_cnt,
                                                                      'satisfy_feedback_cnt': satisfy_feedback_cnt,
                                                                      'simple_feedback_cnt': simple_feedback_cnt,
                                                                      'unsatisfy_feedback_cnt': unsatisfy_feedback_cnt,
                                                                      'satif_ratio': satif_ratio,
                                                                      'simple_ratio': simple_ratio,
                                                                      'unsatif_ratio': unsatif_ratio
                                                                      })


def history_data_center(request):
    result = data_center_history()
    days_diff = [6, 5, 4, 3, 2, 1, 0]
    current_date = [datetime.datetime.fromtimestamp(time.time() - i * 24 * 3600).strftime("%m-%d") for i in days_diff]
    return render(request, 'userManagerSys/manage_data_history.html',{'current_date':current_date})


def test(request):
    return render(request, 'userManagerSys/radar-multiple.html')





