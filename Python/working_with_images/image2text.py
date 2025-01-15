import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import easyocr
reader = easyocr.Reader(['en'])

img_path = "D:/thamu/others/Rajesh - samsung/image_pdf_comparision/imgcom/imgs/from_img.png"
pdf_path = "D:/thamu/others/Rajesh - samsung/image_pdf_comparision/imgcom/imgs/from_pdf.png"
save_path = "D:/thamu/others/Rajesh - samsung/image_pdf_comparision/imgcom/pdf2image/"


output1 =reader.readtext(img_path,detail = 0)
print(output1)

output2 =reader.readtext(pdf_path,detail = 0)
print(output2)

a= ' '.join(output1).lower()
b = ' '.join(output2).lower()

if(a == b):
    print("yes")
else:
    print("no")