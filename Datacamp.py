import requests
from bs4 import BeautifulSoup as bs 

bio = 'https://www.datacamp.com/courses/biomedical-image-analysis-in-python'
sign_in = 'https://www.datacamp.com/users/sign_in'

session = requests.session()

def save_html(url=None, file_name=None, sess=None, bs_object=None, soup=None):
        '''Save Html files'''
        if url:
            page = sess.get(url)
        if bs_object:
            page = bs_object
        html = open('{}.html'.format(file_name), 'wb')
        print('Writing File')
        html.write(page.content)
        print('Write Completed\nClosing File')
        html.close()
        print(html.closed)
        if soup:
            return bs(page.content, 'lxml')

soup = save_html(sign_in, 'Signin', session, soup=True) 

inputs = soup.find_all('input')
for i, inp in enumerate(inputs):
    print(i, end='  ')
    print(inp['name'], end='\n\n')

for i in inputs:
    if i['name'] == 'authenticity_token':
        token = i['value']
print(token)

payload = {'user[email]': None,
'user[password]': None,
'authenticity_token': token}

result = session.post(sign_in, data=payload)

soup = bs(result.content, 'lxml') 

bio_soup = save_html(bio, 'Biomedical', session, soup=True)  

ol = bio_soup.find('ol', class_='chapters chapters--single-column')

import bs4

## Chapters and Their Descriptions
a = 1
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

ul = ol.find_all('ul', class_='chapter__exercises hidden') 
h5 = ul[0].find_all('h5') #chapter headers 
links = ul[0].find_all('a') #chapter links

a[0].img['alt']
a[0]['href']

for a, b in zip(h5, links):
    print(a.get_text(), end='  ') # Get the text from headers tag
    print(b.img['alt'].split()[2]) # link description(Video, exer, MC)
    print('Links -->  ', b['href']) 
    
b['href'][35:]


course = {}
for i, lesson in enumerate(ul):
    h5 = lesson.find_all('h5')
    links = lesson.find_all('a')
    chapters = {(b.img['alt'].split()[2], a.get_text()):b['href'] for a, b in zip(h5, links)}
    course['chapter {}'.format(i+1)] = chapters 

course

def print_course(course_dict):
    for i, chapter in enumerate(course_dict.keys()):
        print('--'*25, end='\n\n')
        ch = chapter + ' {}'.format(ch_headers[i])
        print(ch.center(50, '*'), end='\n\n')
        print(ch_desc[i], end = '\n\n\n')
        k = 0
        for lesson, links in course_dict[chapter].items():
            string = str(k+1) + ' ' + lesson[1] +  '({})'.format(lesson[0]) +\
                  ' --> ' + links[35:]
            print(string)
            print('-'*len(string))
            k += 1

print_course(course) 

c = 'This is at center'
new_c = c.rjust(4, '*')
print(new_c)
print(len(c), len(new_c))

video = 'https://campus.datacamp.com/courses/biomedical-image-analysis-in-python/exploration?ex=1'

video_soup = save_html(video, 'video', session, soup=True)

r = video_soup.prettify() 
print(r)

error = 'https://s3.amazonaws.com/videos.datacamp.com/transcoded/7032_biomedical_image_analysis/v1/hls-7032_ch1_1-600k000100.ts'

v = requests.get(error)
v.status_code

data = {'CR7':'Juve', 'Messi':'Barcelona', 'Neymar':'PSG', 'Ramos':'Real Madrid'}  

for i, (k, v) in enumerate(data.items()):
    print(i+1, end='  ')
    print(k, v)

data.keys() 

data.values() 

try:
    exer = no_of_exer.text.split()[1]
    no = exer[1].split('/')[1]
    for i in range(int(no)):
        driver.get_screenshot_as_file('{} {} {}'\
            .format(num, 'Exer_{}'.format(i+1), name))
        try:
            hint = driver.find_element_by_partial_link_text('Take Hint')
            hint.click()
        except:
            pass
        answer = driver.find_element_by_partial_link_text('Show Answer')
        answer.click()
        driver.get_screenshot_as_file('{} {} {}'\
            .format(num, 'Sol_{}'.format(i+1), name))
        submit = driver.find_elements_by_class_name('dc-btn__content')
        for sub in submit:
            if 'solution' in sub.text.lower():
                run = sub
        
        if i != int(no) - 1:
            time.sleep(10) 
            run.click()
except:
    print('Only one exercise')
    print('Normal process')
        