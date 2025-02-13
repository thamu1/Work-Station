import numpy as np




# arr = np.array(li)

# print(arr[:,0])
# print(np.diagonal(arr))
# print(np.diagonal(np.flipud(arr)))

lis = [['','',''],['','',''],['','','']]

li = np.array(lis)

for i in li:
    print(i)

def xoxo(a,b,re):
    if(li[a][b] == ""):
        li[a][b] = re
    else:
        print("already taken choose something else")

    for i in li:
        print(i)

user = ("user1", "user2")
user_select = int(input("select user: 1 or 2 = "))

star = np.array(['*','*','*'])
zero = np.array(['0','0','0'])

a = 0
b = 0

count = 0


while(True):
    if((li[:,0] == star).all() or (li[:,0]==zero).all()
       or (li[:,1] == star).all() or (li[:,1]==zero).all()
       or (li[:,2] == star).all() or (li[:,2]==zero).all()
       or (li[0,:] == star).all() or (li[0,:]==zero).all()
       or (li[1,:] == star).all() or (li[1,:]==zero).all()
       or (li[2,:] == star).all() or (li[2,:]==zero).all()
       or ((np.diagonal(li) == star).all() or (np.diagonal(li) == star).all())
       or ((np.diagonal(np.flipud(li)) == star).all() or (np.diagonal(np.flipud(li)) == star).all())
       ):
        if(user_select == 2):
            print(f"The game is won by: {user_select-1}")
        else:
            print(f"The game is won by: {user_select+1}")
        break
    else:
        if(count == 9):
            print("Game is draw...")
            break
        else:
            n = int(input("enter your position 1-9 = "))
            if user_select == 1:
                if(n>=1 and n<=3):
                    a = 0
                    b = n-1
                elif(n>3 and n<=6):
                    a = 1
                    b = n-4
                elif(n>6 and n<=9):
                    a = 2
                    b = n-7
                xoxo(a,b,'*')
                user_select = 2
            else:
                if(n>=1 and n<=3):
                    a = 0
                    b = n-1
                elif(n>3 and n<=6):
                    a = 1
                    b = n-4
                elif(n>6 and n<=9):
                    a = 2
                    b = n-7
                xoxo(a,b,'0')
                user_select = 1
            count+=1


        


