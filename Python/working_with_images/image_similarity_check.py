import cv2
from multiprocessing.pool import ThreadPool as Pool
import os
import pandas as pd
import numpy as np
from time import time
from datetime import datetime

output_path="C:/Users/ThamotharanC/OneDrive - Softcrylic LLC/Desktop/Django/facerec/facerecapp/static/img"
pa=output_path
new_img_path = f"{output_path}/thamu.png"

newcv=cv2.imread(new_img_path)      #small

image = newcv.copy()

print("crop after click spacebar")

roi=cv2.selectROI(image)
print(roi)

roi = [167, 29, 267, 343]

im_cropped = image[int(roi[1]):int(roi[1]+roi[3]),int(roi[0]):int(roi[0]+roi[2])]
cv2.destroyAllWindows()

# cv2.imshow("frame", im_cropped)
# key = cv2.waitKey(1)

check = []

def templatenew(i): 


    var=""
    if(i.endswith('.bmp') or i.endswith('.jpg') or i.endswith('.png') or i.endswith('.jpeg')):
        
        newcv= im_cropped

        serread=cv2.imread(i)  #big 
        sercv=serread.copy()
#             sercv=serread[300:500, :]
#             sercv=sercv[int(roi[1]):int(roi[1]+roi[3]),int(roi[0]):int(roi[0]+roi[2])]
        nh,nw,ns=newcv.shape
        sh,sw,ss=sercv.shape
        if(sh>=nh and sw>=nw and ss>=ns):
            res=cv2.matchTemplate(sercv,newcv,cv2.TM_CCOEFF_NORMED)
            th=0.80
            loc=np.where(res>=th)
            if(len(loc[0])>0 and len(loc[1])):
                var="yes"
                savepath=pa+"/"+str(time())+".png"
                for pt in zip(*loc[::-1]):
                    cv2.rectangle(sercv,pt,(pt[0]+nw,pt[1]+nh),(0,255,255),2)
                cv2.imwrite(savepath,sercv)
                # cv2.destroyAllWindows()
            else:
                var="no"
        else:
            var="no"

        return (var)
           

search_path="C:/Users/ThamotharanC/OneDrive - Softcrylic LLC/Desktop/Django/facerec/facerecapp/static/img"
path_list=[search_path+"/"+i for i in os.listdir(search_path)]


from multiprocessing.pool import ThreadPool as Pool

pool = Pool(10)
if __name__=="__main__":
    for var in pool.map(templatenew,path_list):
        check.append(var)
        pass
        
print("process finished.")
print(check)