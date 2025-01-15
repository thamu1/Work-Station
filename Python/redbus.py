import numpy as np

from itertools import combinations

root_choice = list(combinations("123", 2))
fromtoend = ('1', '3')
root_choice.remove(fromtoend)

root = {"theni":1, "thirichi":2, "chennai":3}
root_num = {1:"theni", 2:"thirichi", 3:"chennai"}

seat = [1,2,3]

blocked = []

# 1:["(1,3), rem" (2,3), (1,2)] 
#  if val[1] empty => blocked
#  (1,2) => remove from 1 -> len() == 1 -> is in 1:(2,3) -> book remove -> empty blocked

seat_dic = {}
for i in seat:
    seat_dic.update({i:root_choice})
    
flag = 0
while(len(seat) != len(blocked)):
    
    boarding = input("enter boarding from : ")
    stop = input("enter stop : ")
    
    no = int(input("enter seat number : "))
    
    bs = (str(root[boarding]), str(root[stop]))
    
    if(no not in blocked):
        if(len(seat_dic[no]) > 0 ):
            if(bs == fromtoend):
                seat_dic[no] = []
                blocked.append(no)
                
            else:
                if(bs in seat_dic[no]):
                    dummy = seat_dic[no].copy()
                    dummy.remove(bs)
                    seat_dic[no] = dummy
                    if(len(seat_dic[no]) == 0):
                        blocked.append(no)
                else:
                    print("invalid booking..")
        else:
            print("already booked..")
            
    else:
        print("ticket already booked...")
                
    print("available seat and information : ", seat_dic)
    print("blocked : ", blocked)
                
    flag += 1
                
print("all the ticket has been booked..")

