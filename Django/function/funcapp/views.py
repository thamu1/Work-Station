
from django.shortcuts import render, redirect
from .models import *
from django.db import connection
from django.contrib.auth import login,logout,authenticate
import cgi
import mysql.connector as mc

# conn = mc.connect(
#     host='127.0.0.1',
#     user='root',
#     password='Mysql.08',
#     database='functions'
#     )

# cursor = conn.cursor()

cursor = connection.cursor()
tableName = 'Thamu'

def selectAll():
    getsql = f"select * from functions.{tableName} order by id desc"
    cursor.execute(getsql)
    result = cursor.fetchall()
    context = {'all':result}
    return context

def login(request):
    if(request.method == 'POST'):
        email = request.POST['email']
        password = request.POST['password']
        if(email == 'thamu@gmail.com' and password == '123'):
            request.session['user'] = email
            # request.session['user'] = userName
            request.session.save()
            # session_key=request.session.session_key
            return redirect('get')
        else:
            context = {'failed':'Login failed'}
            return render(request , 'emptyhome.html',context)
            
    else:
        return render(request, 'login.html')
    
    # logout(request)
    # request.session.flush()
    
def lo(request):
    if request.session.has_key('user'):
        del request.session['user']
        return redirect('login')
    else:
        return redirect('get')
    
    
def get(request):
    if 'user' in request.session:
        if(request.method == "POST"):
            if('update' in request.POST):
                id = request.POST['id']
                city = request.POST['city']
                name1 = request.POST['name1']
                name2 = request.POST['name2']
                amount = request.POST['amount']
                extra = request.POST['extra']
                updateSql = f"update functions.{tableName} set city=%s, name1=%s, name2=%s, amount=%s, extra_special=%s where id=%s;"
                updateVal = [city,name1,name2,amount,extra,id]
                cursor.execute(updateSql,updateVal)
                # conn.commit()
                status = "data updated successfully"
                context = selectAll()
                context['status'] = status
                return render(request, 'adHome.html',context)
            elif('delete' in request.POST):
                # id = request.POST['id']
                # deleteSql = f"delete from functions.{tableName} where id=%s;"
                # deleteVal = [id]
                # cursor.execute(deleteSql,deleteVal)
                # conn.commit()
                status = f"delete operation is disabled"
                context = selectAll()
                context['status'] = status
                return render(request, 'adHome.html',context)
            elif('insert' in request.POST):
                city = request.POST['city']
                name1 = request.POST['name1']
                name2 = request.POST['name2']
                amount = request.POST['amount']
                extra = request.POST['extra']
                
                check_sql = f"select * from functions.{tableName} where city = %s and name1 = %s and name2 = %s ;"
                check_val = [city, name1, name2]
                cursor.execute(check_sql, check_val)
                count = cursor.fetchall()
                if(len(count) == 0):    
                    inssql = f'insert into functions.{tableName}(city,name1,name2,amount,extra_special) values(%s,%s,%s,%s,%s)'
                    insval = [city,name1,name2,amount,extra]
                    cursor.execute(inssql,insval) 
                    status = f'insert successfully...'
                else:
                    status = "This have been already Placed"
                context = selectAll()
                context['status'] = status
                return render(request, 'adHome.html',context)
                
                
        else:
            cresql = f"""create table if not exists functions.{tableName}
                    (id int primary key auto_increment,city varchar(100),name1 varchar(100),name2 varchar(100),amount int,extra_special varchar(255))
                    """
            cursor.execute(cresql)
            
            status = "Here you are"
            context = selectAll()
            context['status'] = status
            return render(request, 'adHome.html',context)
    else:
        context = {'empty':"you are not logged in.."}
        return render(request, 'emptyhome.html',context)


def home(request):

    if 'user' in request.session:
        val = request.session['user']
        context = {'check':val}
        if(len(val) != 0):
            if(request.method == 'POST'):
                if 'insert' in request.POST:
                    city = request.POST['city']
                    name1 = request.POST['name1']
                    name2 = request.POST['name2']
                    amount = request.POST['amount']
                    extra = request.POST['extra']

                    inssql = f'insert into {tableName}(city,name1,name2,amount,extra_special) values(%s,%s,%s,%s,%s)'
                    insval = [city,name1,name2,amount,extra]
                    cursor.execute(inssql,insval) 

                    text = f'{name1}-{name2} insert {amount} successfully...'

                    context = {'insert':text}

                    return render(request , 'home.html',context)
                

                elif 'get' in request.POST:
                    selsql = f'select * from functions.{tableName} order by id desc limit 1'
                    cursor.execute(selsql)
                    result = cursor.fetchall()
                    context = {'get':result}

                    return render(request , 'home.html',context)
                

                elif 'update' in request.POST:
                    id = request.POST['id']
                    ucity = request.POST['ucity']
                    uname1 = request.POST['uname1']
                    uname2 = request.POST['uname2']
                    uamount = request.POST['uamount']
                    uextra = request.POST['uextra']
                    upsql = f'update {tableName} set city=%s,name1=%s,name2=%s,amount=%s,extra_special=%s where id=%s'
                    upval = [ucity,uname1,uname2,uamount,uextra,id]
                    cursor.execute(upsql,upval)
                    result = [ucity,uname1,uname2,uamount,uextra]
                    context = {'update':result}

                    return render(request , 'home.html',context)
            return render(request , 'home.html',context)
        else:
            return render(request , 'emptyhome.html',context)
    else:
        return redirect('emptyhome')
    
def emptyhome(request):
    return render(request, 'emptyhome.html')







