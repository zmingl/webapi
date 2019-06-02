from django.db import connection
from .models import Meetings
from .models import Users_Meetings
from .models import Users
from django.forms.models import model_to_dict
from django.db import transaction

#查找用户
def select_user(mobile,password):
        return model_to_dict(Users.objects.filter(mobile=mobile).filter(pwd=password).get())

def find_user_by_id(id):
        return model_to_dict(Users.objects.filter(id=id).get())
    

#查找参加的会议
def select_meeting_att(user_id):
        return Users_Meetings.objects.filter(user_id=user_id).values('status','meeting__name','meeting__id','meeting__start_at','meeting__end_at','meeting__founder__user')

#查找创建的会议
def select_meeting(founder_id):
        return Meetings.objects.filter(founder_id=founder_id).values('name','id','start_at','end_at','founder__user')

def meeting_total(meeting_id):
        with connection.cursor() as cursor:
                result = cursor.execute('select id from users_meetings where meeting_id=%s',[meeting_id])
                return result
def meeting_hc(meeting_id):
        with connection.cursor() as cursor:
                result = cursor.execute('select id from users_meetings where meeting_id=%s and status=%s',[meeting_id,'已签到'])
                return result

# 用户注册
def insert_user(username,password,mobile,upload):
    with connection.cursor() as cursor:
        cursor.execute("INSERT into users(user,pwd,mobile,group_id) values(%s,%s,%s,1)",[username,password,mobile])
        result = cursor.lastrowid
        print (result)
        with transaction.atomic():
                upload(result)
    return result   

# 会议创建    
def insert_meeting(founder_id,name,start,end):
    with connection.cursor() as cursor:
        cursor.execute("INSERT into meetings(founder_id,name,start_at,end_at) values(%s,%s,%s,%s)",[founder_id,name,start,end])
        result = cursor.lastrowid
        connection.commit()
    return result   

# 添加参会人员    
def insert_users_meeting(meeting_id,user_id):
    row = (meeting_id,user_id,'未签到')
    with connection.cursor() as cursor:
        result = cursor.execute("INSERT into users_meetings(meeting_id,user_id,status) values(%s,%s,%s)",row)
        connection.commit()
    return result   

#删除用户所在会议
def delete_users_meeting(meeting_id,user_id):
    with connection.cursor() as cursor:
        result = cursor.execute("DELETE FROM users_meetings WHERE meeting_id=%s and user_id=%s",[meeting_id,user_id])
        connection.commit()
        return result

#删除会议
def delete_meeting(meeting_id):
    with connection.cursor() as cursor:
        result1 = cursor.execute("DELETE FROM meetings WHERE id=%s",[meeting_id])
        result2 = cursor.execute("DELETE FROM users_meetings WHERE meeting_id=%s",[meeting_id])
        result = result1 and result2
        if result:
                connection.commit()
        return result

# 修改用户信息
def update_user(column,info,id):
    with connection.cursor() as cursor:
        if column == 'user':
                result = cursor.execute("UPDATE users SET user = %s WHERE id = %s",[info,id])
        elif column == 'pwd':
                result = cursor.execute("UPDATE users SET pwd = %s WHERE id = %s",[info,id])
        elif column == 'mobile':
                result = cursor.execute("UPDATE users SET mobile = %s WHERE id = %s",[info,id])
        elif column == 'group_id':
                result = cursor.execute("UPDATE users SET group_id = %s WHERE id = %s",[info,id])
        connection.commit()
        return result

# 修改会议信息        
def update_meeting(column,info,id):
    with connection.cursor() as cursor:
        if column == 'name':
                result = cursor.execute("UPDATE meetings SET name = %s WHERE id = %s",[info,id])
        elif column == 'start':
                result = cursor.execute("UPDATE meetings SET start_at = %s WHERE id = %s",[info,id])
        elif column == 'end':
                result = cursor.execute("UPDATE meetings SET end_at = %s WHERE id = %s",[info,id])
        connection.commit()
        return result


#修改会议状态
def update_user_meeting(status,meeting_id,user_id):
    with connection.cursor() as cursor:
        result = cursor.execute("UPDATE users_meetings SET status = %s WHERE meeting_id = %s and user_id = %s",[status,meeting_id,user_id])
        connection.commit()
        return result