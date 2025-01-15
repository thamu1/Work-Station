import aspose.words as aw
import os

pa="C:/Users/ThamotharanC/OneDrive - Softcrylic LLC/Pictures/mht to img/"
save_word='C:/Users/ThamotharanC/OneDrive - Softcrylic LLC/Pictures/mht to img/word_sample1/test1.docx'

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