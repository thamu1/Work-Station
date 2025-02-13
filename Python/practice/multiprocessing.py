import time
import concurrent.futures
from PIL import Image, ImageFilter

from multiprocessing.pool import ThreadPool as Pool
from datetime import datetime

img_names = [
    'tester0.jpg',
    'tester1.jpg',
    'tester2.jpg',
    'tester3.jpg',
    'tester4.jpg',
    'tester5.jpg',
    'tester6.jpg',
    'tester7.jpg',
    'tester8.jpg',
    'tester9.jpg',
    'tester10.jpg',
    'tester11.jpg',
    'tester12.jpg',
    'tester13.jpg',
    'tester14.jpg',
    'tester15.jpg',
    'tester16.jpg',
    'tester17.jpg',
    'tester18.jpg',
    'tester19.jpg']



t1 = time.perf_counter()

size = (1200, 1200)


def process_image(img_name):
    img = Image.open(img_name)

    img = img.filter(ImageFilter.GaussianBlur(15))

    img.thumbnail(size)
    img.save(f'processed/{img_name}')
    print(f'{img_name} was processed...')

st = time()

pool = Pool(10)
if __name__=="__main__":
    for path,var in pool.map(process_image,img_names):
        # pool_path.append(path)
        # pool_selected.append(var)
        pass
        
et=time()
print(et-st)
print(datetime.now())

print(f'Finished in {et-st} seconds')



