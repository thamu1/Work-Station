import aspose.words as aw
import os

save_word = "D:/thamu/others/Rajesh - samsung/image_pdf_comparision/imgcom/pi.pdf"
pa = "D:/thamu/others/Rajesh - samsung/image_pdf_comparision/imgcom/pdf2image/"

filename="mht_test1"
pa=pa+'/'+filename
if not os.path.exists(pa):
    os.makedirs(pa)

word_path=save_word
doc=aw.Document(save_word)

pc=doc.page_count  
img=0
for page in range(pc):
    expage=doc.extract_pages(page,1)
    expage.save(pa+"/"+str(img)+".jpg")
    img+=1
