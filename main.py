import requests
from bs4 import BeautifulSoup
import json
import time
import random
import os

path = './jobs/'
if not os.path.exists(path):
    os.mkdir(path)

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.132 Safari/537.36'}

keyword = '資料庫'
work_dict_head = 'https://www.104.com.tw/job/ajax/content/'

ss = requests.session()

# The variable of work-context dictionary
work_dict_urls = []

for page in range(1, 101):
    url = 'https://www.104.com.tw/jobs/search/?ro=0&keyword=' \
          + keyword + '&order=15&asc=0&page=' + str(page) + '&mode=s'

    res = ss.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    # A dictionary about information of the vacancy
    vacancy_dict = {'job_name': '', 'company_name': '', 'salary': '', 'job_description': '',
                    'company_page': '', 'address': '', 'link': '', 'skills': ''}

    # To get the vacancy blocks
    vacancys = soup.select('div.b-block__left')

    # To get the title and url for each vacancy
    for vacancy in vacancys:

        tmp_a = vacancy.select('a.js-job-link')
        for a in tmp_a:
            vacancy_dict['link'] = 'https:' + a['href']
            work_dict_urls.append(work_dict_head + a['href'][21:26])

    # get into each work_dict
    for work_dict_url in work_dict_urls:
        res = ss.get(work_dict_url, headers=headers)
        job_content = json.loads(res.text)

        skills_str = ''

        try:
            skill_dict = job_content['data']['condition']['specialty']

            # from skill dict get skills
            for skill in skill_dict:
                skills_str += skill['description'] + ','

            vacancy_dict['job_name'] = job_content['data']['header']['jobName']
            vacancy_dict['salary'] = job_content['data']['jobDetail']['salary']
            vacancy_dict['job_description'] = job_content['data']['jobDetail']['jobDescription']
            vacancy_dict['company_name'] = job_content['data']['header']['custName']
            vacancy_dict['company_page'] = job_content['data']['header']['custUrl']
            vacancy_dict['address'] = job_content['data']['jobDetail']['addressRegion'] +\
                                      job_content['data']['jobDetail']['addressDetail']
            vacancy_dict['skills'] = skills_str

        except Exception as err:
            print(err.args)
            continue

        print('Done')

        try:
            with open(path + vacancy_dict['company_name'] + '-' + vacancy_dict['job_name'] + '.txt', 'w',
                      encoding='utf-8') as f:
                for key in vacancy_dict:
                    f.writelines(vacancy_dict[key] + '\n')

        except Exception as err:
            print(err.args)

    time.sleep(random.randint(0, 5))

    print('換頁換頁換頁換頁換頁換頁換頁換頁換頁換頁換頁換頁換頁換頁換頁換頁')
