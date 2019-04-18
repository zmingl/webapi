from django.db import connection

def select(account,password):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user,pwd FROM accounts_users WHERE user=%s and pwd=%s", [account,password])
        row = cursor.fetchall()

    return row

def insert(account,password):
    with connection.cursor() as cursor:
        cursor.execute("INSERT into accounts_users(user,pwd) values(%s,%s)",[account,password])
        connection.commit()

def delete(account):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM accounts_users WHERE user=%s",[account])
        connection.commit()
