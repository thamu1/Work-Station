from PIL import Image
import os
import cv2
import numpy as np

img_path = "D:/thamu/others/Rajesh - samsung/image_pdf_comparision/imgcom/imgs/from_img.png"
pdf_path = "D:/thamu/others/Rajesh - samsung/image_pdf_comparision/imgcom/imgs/from_pdf.png"
save_path = "D:/thamu/others/Rajesh - samsung/image_pdf_comparision/imgcom/pdf2image/"

newcv=cv2.imread(img_path)
sercv=cv2.imread(pdf_path)

nh,nw,ns=newcv.shape
sh,sw,ss=sercv.shape
n = 0

res=cv2.matchTemplate(sercv,newcv,cv2.TM_CCOEFF_NORMED)
th=0.80
loc=np.where(res>=th)
if(len(loc[0])>0 and len(loc[1])):
    print("similar..")
    savepath = f"{save_path}{n}.png"
    for pt in zip(*loc[::-1]):
        cv2.rectangle(sercv,pt,(pt[0]+nw,pt[1]+nh),(0,255,255),2)
    cv2.imwrite(savepath,sercv)
    cv2.destroyAllWindows()
    n += 1
else:
    print("not similar..")