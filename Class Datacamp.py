#Class that takes in Course Link and creates a Dict
import requests 
from bs4 import BeautifulSoup as bs 
import bs4
import copy 
from fake_useragent import UserAgent 
import os 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 

# Background on user-agents

ua = UserAgent() 

os.getcwd()
os.chdir('../')
os.listdir()

os.chdir('Python specialization')

header = {'user-agent':ua.chrome} 

downloaded_list = open('Data_camp.txt')
courses = {}
for line in downloaded_list.readlines(): 
    line = line.split('|')
    courses[line[0]] = [line[1], line[2]]

for k, v in courses.items():
    print(k, v[1][:-1], end='\n\n')

downloaded_list.close() 

len(courses.keys()) 

slides.split('/') 
'/'.join(slides.split('/')[:5])  

class DataCamp:
    session = requests.session()
    home = 'https://www.datacamp.com/users/sign_in'
    log_status = False
    head = {'user-agent':ua.chrome}
    chrome_path = 'd:\\Courses\\Python specialization//chrome//chromedriver.exe'
    audio_url = 'https://s3.amazonaws.com/videos.datacamp.com/mp3'
    slides_url = 'https://s3.amazonaws.com/assets.datacamp.com/production'


    def __init__(self, link, ids, version, spec=''):
        self.link = link
        self.html_page = None
        self.bs_soup = None
        name = self.link.split('/')[-1]
        name = name.split('-')
        self.name = ' '.join([i.capitalize() for i in name])

        self.ids = str(ids)
        self.version = version 

        if spec:
            course = spec.replace(' ', '_')
        else:
            course = self.name.lower().replace(' ', '_') 

        self.audio_base = '{}/{}/{}'.format(self.audio_url, '_'.join([self.ids, course]), self.version)
        self.slides_base = '{}/course_{}/slides'.format(self.slides_url, self.ids) 

        self.saved_html = False 
        self.headers = None
        self.h_desc = None 
        self.ol = None 
        self._course = None
        self.completed = False # indicates whether the course is downloaded or not 

    def login_status(self):
        return self.log_status

    def login(self):
        page = self.session.get(self.home, headers=self.head)
        soup = bs(page.content, 'lxml')
        token = soup.find('input', attrs={'name':'authenticity_token'})['value']    
        payload = {'user[email]': 'hemanth.shendye@gmail.com',
                   'user[password]': 'hyperface', 'authenticity_token': token}
        result = self.session.post(self.home, data=payload, headers=self.head)
        if str(result.status_code)[0] != '2':
            return 'Login Not Successful' 
        else:
            self.log_status = True 
            return 'Login Successful' 
    
    def get(self, ret=False):
        if self.html_page is None:
            self.html_page = self.session.get(self.link, headers=self.head)
            self.bs_soup = bs(self.html_page.content, 'lxml')
            return 'Page Downloaded'
        else:
            return 'Page Already Downloaded'
    
    def soup(self):
        if self.log_status != True:
            return 'Please Login'
        elif self.html_page is None:
            return 'Download the page using \'get\' method'
        return self.bs_soup

    def save_html(self):
        if self.saved_html == True:
            return 'Already saved'
        elif self.html_page is None:
            return 'Download the page using \'get\' method'
        files = open('{}.html'.format(self.name), 'wb')
        files.write(self.html_page.content)
        files.close()
        self.save_html = True 
        return 'Html file Saved'
    
    def get_hd(self): # Get Headers and description
        if self.headers is not None:
            return self.headers[:], self.h_desc[:]
        self.ol = self.bs_soup.find('ol', class_='chapters chapters--single-column')
        self.headers, self.h_desc = [], []
        for i in self.ol.children:
            if isinstance(i, bs4.element.Tag):
                self.headers.append(i.h4.get_text().strip())
                self.h_desc.append(i.p.get_text().strip())
        return self.headers[:], self.h_desc[:]

    def course_dict(self):
        assert self.ol is not None, "Use 'get_hd' method first"
        if self._course is not None:
            return copy.deepcopy(self._course)

        self._course = {}
        ul = self.ol.find_all('ul', class_='chapter__exercises hidden')

        for i, chapters in enumerate(ul):
            h5 = chapters.find_all('h5')
            links = chapters.find_all('a')
            span = chapters.find_all('img')
            ch = {(c['alt'].split()[2], a.get_text()): b['href'] for a, b, c in zip(h5, links, span)}
            self._course['Chapter {}. {}'.format(i+1, self.headers[i])] = ch   
        return copy.deepcopy(self._course) 

    def save_video(self, link, title=None):
        base = ' '.join(link.split('/')[:-1])
        start = link.split('/')[-1][-8:]
        i = 1
        page = base + '/' + start + str(i).rjust(5, '0') + '.ts'
        video = open('{}.ts'.format(title), 'wb')
        video.close()
        result = self.session.get(page, stream=True, headers=self.head)
        while str(result.status_code)[0] == '2':
            print(page.split('/')[-1])
            video = open('{}.ts'.format(title), 'ab')
            for chuck in result.iter_content(chunk_size=2048*2048):
                if chuck:
                    video.write(chuck)
            video.close()
            i += 1
            page = base + '/' + start + str(i).rjust(5, '0') + '.ts'
            result = self.session.get(page, stream=True, headers=self.head) 
        
    def PrintCourse(self, course_dict):
        print(self.name.center(100, '#'), end = '\n\n\n')
        for i, chapter in enumerate(course_dict.keys()):
            print('--'*25, end='\n\n') 
            print(chapter.center(100, '*'), end='\n\n') 
            print(self.h_desc[i], end = '\n\n\n')
            k = 0
            for lesson, links in course_dict[chapter].items():
                string = str(k+1) + ' ' + lesson[1] +  '({})'.format(lesson[0])
                string2 = 'Links  --> ' + links[35:]
                print(string)
                print(string2)
                print('-'*len(string2))
                k += 1 
    
    def save_mp3(self, link, name, rate):
        print('Link --> {}'.format(link), end= '  ')
        mp3 = self.session.get(link, stream=True, headers=self.head)
        new = None 
        if str(mp3.status_code)[0] != '2':
            print('Link Failed SC:{}'.format(mp3.status_code))
            i = 1
            old = self.version
            new = 'v1' 
            while True: 
                print('New Link --> {}'.format(link.replace(old, new)), end='  ')
                mp3 = self.session.get(link.replace(old, new), stream=True, headers=self.head)
                
                new = new.replace(str(i), str(i+1))  
                 
                i += 1
                if str(mp3.status_code)[0] == '2':
                    print('Link Successful SC:{}'.format(mp3.status_code))
                    break  
                elif i > 10:
                    break
                print('Link Failed SC:{}'.format(mp3.status_code))   
            
        else:
            print('Link Successful')

        if new is None:
            new = self.version 

        print('Downloading {} from {}'.format(name, new), end=' ')
        try:
            save = open('{}.mp3'.format(name) , 'wb')
        except:
            save = open('{}.mp3'.format(name[0]) , 'wb')
        i = 0
        for chunk in mp3.iter_content(chunk_size=1024*rate):
            if chunk:
                if i%500 == 0 and i != 0:
                    print('*')
                else:
                    print('*', end = '')
                save.write(chunk)
                i += 1
        save.close() 
        print('')
        print('-'*50)

    
    def driver_logged(self):
        print('Starting Chrome Driver')
        driver = webdriver.Chrome(executable_path=self.chrome_path)     
        driver.get('https://www.datacamp.com/users/sign_in')   
        driver.find_element_by_name('user[email]').send_keys('hemanth.shendye@gmail.com')
        driver.find_element_by_name('user[email]').send_keys(Keys.RETURN) 
        driver.find_element_by_name('user[password]').send_keys('hyperface')
        driver.find_element_by_name('user[password]').send_keys(Keys.RETURN)
        driver.maximize_window() 
        print('Logged in to Data Camp', end = '\n\n')

        return driver 

    def get_pdf(self, link, rate):
        pdf = self.session.get(link, stream=True, headers=self.head)
        pdf_name = link.split('/')[-1] 
        print('Downloading {}'.format(pdf_name), end=' ')  
        i = 0
        with open(pdf_name, 'wb') as pdf_file:
            for chunk in pdf.iter_content(chunk_size=1024*rate):
                if chunk:
                    if i%200 == 0 and i != 0:
                        print('*')
                    else:
                        print('*', end='')
                    pdf_file.write(chunk)
                    i += 1
        print('')
        print('-'*50)

    def take_screenshot(self, link, cdriver, name, no, clicks):
        d = cdriver 
        for i in range(clicks):
            print('{} Taking Screenshots of {} Exercise {}'.format(no, name, i+1))
            time.sleep(3) 
            d.get_screenshot_as_file('{} {} {}.png'\
                .format(no, 'Ex{}'.format(i+1), name))
            try:
                hint = d.find_element_by_partial_link_text('Take Hint')
                hint.click()
            except:
                print('\n Take Hint not found \n')

            try: 
                answer = d.find_element_by_partial_link_text('Show Answer')
                answer.click()
            except:
                print('\n Show Answer not found')
                       
            d.get_screenshot_as_file('{} {} {}.png'\
                .format(no, 'Sol{}'.format(i+1), name))

            time.sleep(2)   

            submit = d.find_elements_by_class_name('dc-btn__content')
            for sub in submit:
                if 'run solution' in sub.text.lower():
                    run = sub
                elif 'submit answer' in sub.text.lower():
                    run = sub 
                
            if i != clicks - 1:
                print('Waiting for the Page to load')
                try:
                    run.click()
                    time.sleep(6)
                except:
                    print('Run Solution not found') 
                print('Submitted')
        print('-'*50)
    

    def get_exer_no(self, cdriver, link):
        d = cdriver
        d.get(link)
        time.sleep(0.5) 

        inst = d.find_elements_by_class_name('dc-panel__title')
        try:
            for i in inst:
                if 'inst' in i.text.lower():
                    no_of_exer = i
                    try:
                        print(i.text)
                    except:
                        print('Instructions -->')
        except:
            pass 

        try:        
            check = no_of_exer.text.split()
        except:
            check = ['Instruction']
            
        if len(check) == 1:
            return 1
        else:
            try:    
                exer = no_of_exer.text.split()[1]
                exer = exer.split('/')[1]
                return int(exer)
            except:
                return 3

    def get_mc(self, cdriver, link, name, no):
        d = cdriver
        d.get(link)
        print('Taking Screenshot of MC')
        time.sleep(1.5)
        try:
            hint = d.find_element_by_partial_link_text('Take Hint')
            hint.click()
        except:
            print('Hint not found')
            print('>'*50)
        try: 
            sc = d.get_screenshot_as_file('{} MC {}.png'.format(no, name)) 
        except:
            sc = d.get_screenshot_as_file('{} MC.png'.format(no))
        if sc != True:
            print('Screenshoot Failed\nTrying again')
            again = d.save_screenshot('{} MC.png'.format(no))
            if again == True:
                print('Success')
            else:
                print('Failed to get screenshot')

    def audio_mp3(self, cdriver, link, name, http):
        d = cdriver
        d.get(link)
        time.sleep(1)

                
        iframe = d.find_element_by_tag_name('iframe')
        aud_v = iframe.get_attribute('src')
        d.get(aud_v)
        values = d.find_element_by_id('videoData').get_attribute('value')

        ind = values.find('mp4_link') + 11
        vid = values[ind:].split(',')[0][:-1]

        if http:
            vid = 'https:' + vid 
            
        try:
            download = self.session.get(vid, stream=True, headers=self.head)
        except:
            print('Failed Downloading', name)
            print('Link -->', vid)
        print('Downloading {}'.format(name), end=' ') 

        try:
            save = open('{}.mp4'.format(name), 'wb')
        except:
            save = open('{}.mp4'.format(name[0]), 'wb')
        try:
            for chuck in download.iter_content(chunk_size=1024*100):
                if chuck:
                    print('*', end='')
                    save.write(chuck)
            print('*')
        except:
            print('Could Not Donwload', name, end='\n\n')
        save.close()
        print('-'*50)

    def download(self, course_dict, rate, mp3=False, https=False, slide=False, path=None):
        if self.completed:
            return None 

        driver = self.driver_logged()

        if path:
            os.chdir(path)
        
        folder = os.getcwd() + '//{}'.format(self.name) 
        os.mkdir(folder)
        os.chdir(folder)
        mess = self.save_html()
        print(mess) 

        for no, chapter in enumerate(course_dict.keys()):
            name = os.getcwd() + '//' + chapter
            try:
                os.mkdir(name)
            except:
                name = os.getcwd() + '//chapter {}'.format(no+1)
                os.mkdir(name)
                   
            os.chdir(name)
            if slide:
                print('Custom Slide path')
                sl = self.slides_base + '/ch{}.pdf'.format(no+1)
            else:
                sl = self.slides_base + '/chapter{}.pdf'.format(no+1) 

            self.get_pdf(link=sl, rate=rate) 

            a = 0  #video_count

            for i, (label, link) in enumerate(course_dict[chapter].items()):
                if label[0] == 'video':
                    a += 1
                    if mp3 == 'True':
                        api = '_'.join([self.ids, 'ch{}_{}'.format(no+1, a)]) 
                        web_address = self.audio_base + '/{}'.format(api) + '.mp3' 
                        self.save_mp3(link=web_address, name=str(i+1)+' '+label[1], rate=rate)
                    elif mp3 == 'vid':
                        self.audio_mp3(cdriver=driver, link=link, name=str(i+1)+' '+label[1], http=https)
                         

                elif label[0] == 'interactive':
                    num = self.get_exer_no(cdriver=driver, link=link)
                    self.take_screenshot(link=link, cdriver=driver, name=label[1], no=i+1, clicks=num)

                else:
                    self.get_mc(cdriver=driver, link=link, name=label, no=i+1)
                    print('-'*50)
                
            os.chdir('../')
            print('\n\n')  

        self.completed = True 
        os.chdir('../')
        print('Download Completed')
        time.sleep(5)
        driver.quit()

        


dir(DataCamp) 
################################################################################
def prepare_link(link):
    base = ' '.join(link.split('/')[:-1])
    start = link.split('/')[-1][-8:]
    return base, start 

#os.chdir('../') 
os.getcwd() 


#(4015, 'https://www.datacamp.com/courses/network-analysis-in-python-part-2') ------------------
#(5702, slides https 'https://www.datacamp.com/courses/manipulating-time-series-data-in-python') ------------
#(3882, slides custom https 'https://www.datacamp.com/courses/importing-managing-financial-data-in-python')


to_download = [
(16561, 'https://www.datacamp.com/courses/experimental-design-in-python')
]
#(3882, slides custom https 'https://www.datacamp.com/courses/importing-managing-financial-data-in-python')
#(16561, 'https://www.datacamp.com/courses/experimental-design-in-python', v2)
#(16473, 'https://www.datacamp.com/courses/cleaning-data-with-apache-spark-in-python', v1)
#(16839, 'https://www.datacamp.com/courses/winning-a-kaggle-competition-in-python', v1)


for i in to_download:
    course_page = i[1]
    course = DataCamp(course_page, ids=i[0], version='v2')
    print('Name: {}\nid: {}'.format(course.name, course.ids))
    print(course.login_status())
    try:
        print(course.login())
    except:
        print('Already logged in')
    print(course.get())   
    print(course.get_hd()) 

    course_dict = course.course_dict() 
    course.PrintCourse(course_dict)

    if len(course_dict) == 0:
        print('{} failed'.format(i[1]))
        break
        
    start = time.time()
    course.download(course_dict=course_dict, rate=100, mp3='True')
    end = time.time()
    
    print('Time Taken', end - start) 
    Download_txt = open('Data_camp.txt', 'at')
    line = course.name + '|' + course.ids + '|'  + str(round(end-start, 2)) + '\n'
    Download_txt.write(line)
    Download_txt.close() 
    print('Details Saved') 
##################################################################################

Geo_dict 

Geo.PrintCourse(Geo_dict)  

p = path[:-18]
os.chdir(p)
os.getcwd() 
os.chdir('../')  

###################################################

video_links = {}
for i, lesson in enumerate(Geo_dict.keys()):
    video_links[i+1] = []
    k = 0
    for data, link in Geo_dict[lesson].items():
        if data[0].lower() == 'video':
            video_links[i+1].append(link) 
        k += 1

video_links 
####################################################
## Selenium   
os.chdir('../') 
os.getcwd() 
chromedriver = os.getcwd() + '//chrome' 
exe = os.listdir(chromedriver)[0]  
path = os.getcwd() + '//chrome' + '//' + exe 
path 

import time 

driver = webdriver.Chrome(executable_path=path)   

driver.get('https://www.datacamp.com/users/sign_in')   
driver.find_element_by_name('user[email]').send_keys('hemanth.shendye@gmail.com')


driver.find_element_by_name('user[email]').send_keys(Keys.RETURN) 

driver.find_element_by_name('user[password]').send_keys('hyperface') 
driver.find_element_by_name('user[password]').send_keys(Keys.RETURN)

driver.maximize_window() 

#driver.get(Geo.link) 
ch1 = list(list(Geo_dict.values())[3].values())  
ch1[2][-10:] 

exer = 'https://campus.datacamp.com/courses/customer-analytics-ab-testing-in-python/key-performance-indicators-measuring-business-success?ex=4'
new_exer = 'https://campus.datacamp.com/courses/extreme-gradient-boosting-with-xgboost/classification-with-xgboost?ex=1'

driver.get(new_exer)  # v is the first video link  
time.sleep(5) 

iframe = driver.find_element_by_tag_name('iframe')
iframe.get_attribute('src') 
aud_v = iframe.get_attribute('src')
driver.get(aud_v)
values = driver.find_element_by_id('videoData').get_attribute('value')

ind = values.find('mp4_link') + 11
vid = values[ind:].split(',')[0][:-1]

vid = ':'.join(values.split(':')[1:3])[:-18][1:]
vid
download = requests.get(vid, stream=True)
print('Downloading  ', end='') 
vid_test = open('vid_test.mp4', 'wb')
for chuck in download.iter_content(chunk_size=1024*100):
    if chuck:
        print('*', end='')
        vid_test.write(chuck)
print('*')
vid_test.close()

#-------------------bs--------------------------------------------
page = course.session.get(exer, headers=header) 
soup = bs(page.content, 'lxml') 

soup = bs(driver.page_source, 'lxml') 

for div in soup.find_all('div'):
    print(div.get('class'))

soup.find('iframe').attrs

soup.find_all('div', class_='vex-scroller')[0].iframe['src']
#-----------------------------------------------------------------

# To find no of exercise 
inst = driver.find_elements_by_class_name('dc-panel__title') 
for i in inst:
    if 'inst' in i.text.lower():
        no_of_exer = i
no_of_exer.text 

exer = no_of_exer.text.split()[1].split('/')[1] 
exer 

no_of_exer.text

num = 15
name = 'DataCamp'

exer = no_of_exer.text.split()[1].split('/')[1] 
exer 


for i in range(int(no)):
    driver.get_screenshot_as_file('{} {} {}.png'\
        .format(num, 'Exer_{}'.format(i+1), name))
    try:
        hint = driver.find_element_by_partial_link_text('Take Hint')
        hint.click()
    except:
        print('Hint not Found')
        pass
    answer = driver.find_element_by_partial_link_text('Show Answer')
    answer.click()
    driver.get_screenshot_as_file('{} {} {}.png'\
        .format(num, 'Sol_{}'.format(i+1), name))
    submit = driver.find_elements_by_class_name('dc-btn__content')
    for sub in submit:
        if 'solution' in sub.text.lower():
            run = sub
        
    if i != int(no) - 1:
        print('Waiting for the Page to load')
        run.click()
        time.sleep(20) 
        print('Submitted')

for i in range(2):
    if i != 2 - 1:
        print(i)

        



driver.get_screenshot_as_file('Before_2.png')


hint = driver.find_element_by_partial_link_text('Take Hint')  
hint.click() 
answer = driver.find_element_by_partial_link_text('Show Answer') 
answer.click() 
#answer.location  
driver.get_screenshot_as_file('After_2.png') 
submit = driver.find_elements_by_class_name('dc-btn__content')  

for sub in submit:
    if 'solution' in sub.text.lower():
        run = sub

run.click() 

help(webdriver.Chrome.get_sc)   

from PIL import Image
Image.open(pic) 

#driver.find_elements_by_tag_name('html')   

p#age = bs(driver.page_source, 'lxml') 

print(page.prettify()) 

len(page.find_all('html'))
frame = page.find('iframe') 
dir(frame) 

for k, v in frame.attrs.items():
    print(k)
    print(v, end='\n\n')  


for i in div:
    print(i, end='\n\n')   

###############################################
###############################################
m1 = 'https://s3.amazonaws.com/videos.datacamp.com/mp3/7356_working_with_geospatial_data_in_python/v1/7356_ch1_1.mp3'
 
address =  m1.split('/')
address 
base_address =  '/'.join(address[:5])  
base_address
ch = address[-1].split('.')[0][-5:] 
ch 

Geo.name.lower().replace(' ', '_')


def get_ch(link):
    return link.split('/')[-1].split('.')[0][-5:]  

video_links[4]
driver.get(video_links[4][4])        

m2 = 'https://s3.amazonaws.com/videos.datacamp.com/mp3/7356_working_with_geospatial_data_in_python/v1/7356_ch4_5.mp3' 

#m = {}
#m[4] = [] 
m[4].append(get_ch(m2))  

for k, v in m.items():
    print(k, v)

check = m[2] 

for i in range(len(check)):
    print(check[i])

slides = 'https://s3.amazonaws.com/assets.datacamp.com/production/course_7356/slides/chapter1.pdf' 




pdf = requests.get(slides, stream=True) 

slide_down = open('test_slides.pdf', 'wb') 


for chunk in pdf.iter_content(chunk_size=1024*1024):
    if chunk:
        slide_down.write(chunk) 

slide_down.close()
###############################################################
###############################################################













###########################################################
#ol = soup.find('ol', class_='chapters chapters--single-column')
ch_headers = []
ch_desc = []
for i in ol.children:
    if isinstance(i, bs4.element.Tag):
        header = i.h4.get_text().strip() # Chapters
        print(header)             
        desc = i.p.get_text().strip() #Description
        print(desc)
        print('-'*20)
        ch_headers.append(header)
        ch_desc.append(desc)
ch_headers

ul = ol.find_all('ul', class_='chapter__exercises hidden dc-u-ta-center')  
ul
h5 = ul[0].find_all('h5') #chapter headers 
links = ul[0].find_all('a') #chapter links



course = {}
for i, lesson in enumerate(ul):
    h5 = lesson.find_all('h5')
    links = lesson.find_all('a')
    chapters = {(b.img['alt'].split()[2], a.get_text()):b['href'] for a, b in zip(h5, links)}
    course['chapter {}'.format(i+1)] = chapters 

course 

amazon = 'https://s3.amazonaws.com/videos.datacamp.com/transcoded/6554_advanced_deep_learning_with_keras/v1/hls-6554_ch1_1-1000k00012.ts'
base = '/'.join(amazon.split('/')[:-1]) 
start = amazon.split('/')[-1] 

start 

amazon2 = 'https://s3.amazonaws.com/videos.datacamp.com/transcoded/6554_advanced_deep_learning_with_keras/v1/hls-6554_ch1_2-1000k00001.ts'
base2 = '/'.join(amazon2.split('/')[:-1])  
start2 = amazon2.split('/')[-1]  

amazon3 = 'https://s3.amazonaws.com/videos.datacamp.com/transcoded/6554_advanced_deep_learning_with_keras/v1/hls-6554_ch1_3-1000k00001.ts'
base3 = '/'.join(amazon3.split('/')[:-1])  
start3 = amazon3.split('/')[-1]  

amazon4 = 'https://s3.amazonaws.com/videos.datacamp.com/transcoded/6554_advanced_deep_learning_with_keras/v1/hls-6554_ch2_1-1000k00001.ts'

amazon2[-30:]
amazon4[-30:]



base == base2 == base3

print(start.replace('12', '01'))
print(start2)   
print(start3) 

for i in range(150):
    print(str(i).rjust(5, '0'))
start
v
v = start2[:-8]
sess = Advance_keras.session 
i = 1
page = base + '/' + v + str(i).rjust(5, '0') + '.ts'
result = sess.get(page, stream= True)  
video = open('test2.ts', 'wb')
video.close()
print(result.status_code)
while str(result.status_code)[0] == '2':
    print(page.split('/')[-1]) 
    video = open('test2.ts', 'ab')
    for chunk in result.iter_content(chunk_size=1024*1024):
        if chunk:
            video.write(chunk)
    video.close() 
    i += 1
    page = base + '/' + v + str(i).rjust(5, '0') + '.ts'
    result = sess.get(page, stream=True)  


