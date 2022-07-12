import pymysql


def insert_sql(sql, value):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='zhangjin123',
                           database='intelligentCustomerSys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, value)
    conn.commit()
    cursor.close()
    conn.close()


def select_target(sql, value):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='zhangjin123',
                           database='intelligentCustomerSys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, value)
    target = cursor.fetchone()
    cursor.close()
    conn.close()
    return target


def select_all_target(sql, value):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='zhangjin123',
                           database='intelligentCustomerSys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, value)
    target = cursor.fetchall()
    cursor.close()
    conn.close()
    return target


def edit_sql(sql, value):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='zhangjin123',
                           database='intelligentCustomerSys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, value)
    conn.commit()
    cursor.close()
    conn.close()


def data_center_online():
    import datetime
    import time
    current_date = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d")
    online_sql =f"SELECT a1.date,session_created_cnt,session_used_cnt,session_transfer_cnt,session_feedback_cnt,satisfy_feedback_cnt,simple_feedback_cnt,unsatisfy_feedback_cnt, chat_cnt, no_answer_cnt, tranfer_request_cnt FROM ( SELECT date, count( session_id ) AS session_created_cnt, count( feedback ) AS session_feedback_cnt, sum( CASE WHEN feedback > 3 THEN 1 ELSE 0 END ) AS satisfy_feedback_cnt, sum( CASE WHEN feedback = 3 THEN 1 ELSE 0 END ) AS simple_feedback_cnt, sum( CASE WHEN feedback < 3 THEN 1 ELSE 0 END ) AS unsatisfy_feedback_cnt  FROM ( SELECT * FROM robot_session WHERE date = '{current_date}' ) AS aa1 GROUP BY date ) AS a1 JOIN ( SELECT date, count(distinct session_id) as session_used_cnt,count( chat_id ) AS chat_cnt, sum( CASE WHEN rsp_message = 'NO ANSWER' THEN 1 ELSE 0 END ) AS no_answer_cnt FROM ( SELECT * FROM robot_chat WHERE date = '{current_date}' ) AS aa2 ) AS a2 ON a1.date = a2.date JOIN ( SELECT date, count( request_id ) AS tranfer_request_cnt, count( session_id ) AS session_transfer_cnt FROM ( SELECT * FROM transfer_service WHERE date = '{current_date}' ) AS aa3 ) AS a3 ON a1.date = a3.date"
    res = select_all_target(online_sql,[])
    return res


def data_center_history():
    history_sql = "SELECT a1.date,session_created_cnt,session_used_cnt,session_transfer_cnt,session_feedback_cnt,satisfy_feedback_cnt,simple_feedback_cnt,unsatisfy_feedback_cnt, chat_cnt, no_answer_cnt, tranfer_request_cnt FROM ( SELECT date, count( session_id ) AS session_created_cnt, count( feedback ) AS session_feedback_cnt, sum( CASE WHEN feedback > 3 THEN 1 ELSE 0 END ) AS satisfy_feedback_cnt, sum( CASE WHEN feedback = 3 THEN 1 ELSE 0 END ) AS simple_feedback_cnt, sum( CASE WHEN feedback < 3 THEN 1 ELSE 0 END ) AS unsatisfy_feedback_cnt  FROM ( SELECT * FROM robot_session ) AS aa1 GROUP BY date ) AS a1 JOIN ( SELECT date, count(distinct session_id) as session_used_cnt , count( chat_id ) AS chat_cnt, sum( CASE WHEN rsp_message = 'NO ANSWER' THEN 1 ELSE 0 END ) AS no_answer_cnt FROM ( SELECT * FROM robot_chat  ) AS aa2  GROUP BY date ) AS a2 ON a1.date = a2.date JOIN ( SELECT date, count( request_id ) AS tranfer_request_cnt, count( session_id ) AS session_transfer_cnt FROM ( SELECT * FROM transfer_service ) AS aa3 GROUP BY date ) AS a3 ON a1.date = a3.date"
    res = select_all_target(history_sql, [])
    return res
