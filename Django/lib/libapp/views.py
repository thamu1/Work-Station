from django.shortcuts import render
from .models import tableColumn as tc
from .models import studentLogInDetails as sld
from datetime import datetime
from django.db import connection

def home(request):
    if request.method == 'POST':
        # data = tc.objects.all().values()
        if 'login_form' in request.POST:
            # name = request.POST['name']
            rollno = request.POST['rollno']
            cursor = connection.cursor()

            checkStudentsql = 'select rollno from student where rollno = %s'
            checkStudentval = [rollno]
            cursor.execute(checkStudentsql,checkStudentval)
            checkLength = cursor.fetchall()
            if(len(checkLength) == 1):
                
                sql = 'select * from studentlogindetails where rollno = %s order by id desc limit 1'
                val = [rollno]
                cursor.execute(sql,val)
                getresult = cursor.fetchall()

                # gesult = getresult[0][2]

                length = len(getresult)

                while(True):

                    if (length==0):
                        insertsql = 'insert into studentlogindetails(rollno,intime,outtime) values(%s,%s,%s)'
                        insertval = [rollno,datetime.now(),datetime.now()]
                        cursor.execute(insertsql,insertval) 
                        note = f"successfully {rollno} login"
                        break
                    else:
                        if getresult[0][2] == getresult[0][3]:
                            updatesql = 'update studentlogindetails set outtime = %s where id = %s'
                            updateval = [datetime.now() , getresult[0][0]]
                            cursor.execute(updatesql,updateval)
                            note = f"successfully {rollno} logout"
                            break
                        else:
                            length = 0
                    


                # studetail = tc.objects.filter(rollno = rollno).order_by('-id').values()[0]
                

                
                dic = {'stuinfo':note}
                return render(request,'home.html',dic)
            else:
                note = f"{rollno} - please register first"
                dic = {'stuinfo':note}
                return render(request,'home.html',dic)
            
        
        elif 'signup_form' in request.POST:
            signupname = request.POST['signupname']
            signuprollno = request.POST['signuprollno']

            cursor = connection.cursor()

            # form = tc()
            # form.name = signupname
            # form.rollno = signuprollno
            # form.save()

            sql_query = 'insert into student(name,rollno) values(%s,%s)'
            val = [signupname,signuprollno]
            cursor.execute(sql_query,val)

            # sql = 'select * from student where rollno = %s order by id desc limit 1'
            # sql = 'update student set name = %s where id = %s '
            # val = [signupname,'1']
            # cursor.execute(sql,val)
            # result = cursor.fetchall()




            # lastlogin = tc.objects.filter(rollno=signuprollno).order_by('-id').values()[0]
            
             


            st = f'successfully Registered by - {signuprollno}'

            signupdic = {'signup':st}

            return render(request,'home.html',signupdic)

        else:
            return render(request,'home.html',{'username':'Thamu'})
    else:
            return render(request,'home.html',{'username':'Thamu'})
    

# def signup(request):
#     name = request.POST['name']
#     rollno = request.POST['rollno']
#     return render(request,'home.html',{'stuinfo':[name,rollno]})

def signuppage(request):
    return render(request,'signup.html')
