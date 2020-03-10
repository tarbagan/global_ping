from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
import requests

URL = 'https://www.instagram.com/irgit_valery/'
LOGIN = '***'
PASSWORD = '***'
FILE = 'out_data.txt' #json

#Подключаем драйвер Selenium
driver = webdriver.Firefox(executable_path=r"e:\PythonProgect\insta\geckodriver.exe" )
url_autch = f'https://www.instagram.com/accounts/login/?source=auth_switcher'
driver.get(url_autch)
time.sleep(5)

#Аутификация
log = driver.find_element_by_name( "username" )
psw = driver.find_element_by_name( "password" )
btn = driver.find_element_by_css_selector("[type='submit']")
log.send_keys( LOGIN )
psw.send_keys( PASSWORD )
btn.click()
time.sleep(5)

#Процесс
driver.get(URL)
time.sleep(5)

def get_count(driver):
    # получаем количество постов COUNT
    podtemp = driver.find_element_by_tag_name("html").text
    soup = bs(podtemp, 'lxml')
    pod = (str(soup).split('\n'))
    pod = [x for x in pod if "публикаций" in x]
    pod = [x for x in str(pod) if x.isdigit()]
    pod = int(''.join(pod))
    return pod

def dublicat(dic):
    return list(set(dic))

def get_json(url):
    r = requests.get(url)
    return r.json()

COUNT = get_count(driver)
if COUNT > 0:
    print (f'Начинаем парсинг {COUNT} публикаций аккаунта Инстаграмм')
    print ('*'*40)
    POST = []

    while driver.find_element_by_tag_name('html'):
        soup = bs(driver.page_source, 'lxml')

        for i in soup.findAll('a'):
            url_temp = i.get('href')
            if str(url_temp)[0:3] == '/p/':
                id_post = url_temp.split('/')[2]
                POST.append(id_post)

        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        print (f'Parsing: {len(POST)} / Total: {len(dublicat(POST))} | {id_post}')
        if len(dublicat(POST)) == COUNT:
            break
    print('*' * 40)
    print (f'Идентификаторы {len(dublicat(POST))} публикаций получены. \nНачинаем парсинг публикаций...')
    driver.quit()

    IDENT = dublicat(POST)
    URL_ALL = [f'https://www.instagram.com/p/{x}/?__a=1' for x in IDENT]
    with open(FILE, 'a', encoding='utf8') as file:
        count_temp = []
        try:
            for num, url in enumerate(URL_ALL):
                data = get_json(url)
                count_temp.append(1)
                print (f'№{num} | Пост {len(count_temp)} /Всего{len(URL_ALL)} - записан')
                file.write(str(data) + '\n')
        except Exception as e:
            print (e)

        print('*' * 40)
        print (f'Запись в файл успешна завершена \nВсего постов {len(count_temp)}')
        
else:
    driver.quit()
    print ('У пользователя нет публикаций!')
