import requests
from bs4 import BeautifulSoup
import json
import time
import random
import MySQLdb

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.132 Safari/537.36'}

keyword = '資料庫'
work_dict_head = 'https://www.104.com.tw/job/ajax/content/'

# Connect the database
db = MySQLdb.connect(host='localhost', user='root', passwd='root', db='py104', port=3306, charset='utf8')
cursor = db.cursor()
db.autocommit(True)

ss = requests.session()

# The variable of work-context dictionary
work_dict_urls = []

# The variable of 104 link
link = ''

for page in range(1, 101):
    url = 'https://www.104.com.tw/jobs/search/?ro=0&keyword=' \
          + keyword + '&order=15&asc=0&page=' + str(page) + '&mode=s'

    res = ss.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    # To get the vacancy blocks
    vacancies = soup.select('div.b-block__left')

    # To get the title and url for each vacancy
    for vacancy in vacancies:

        tmp_a = vacancy.select('a.js-job-link')
        for a in tmp_a:
            link = 'https:' + a['href']
            work_dict_urls.append(work_dict_head + a['href'][21:26])

    # get into each work_dict
    for work_dict_url in work_dict_urls:
        res = ss.get(work_dict_url, headers=headers)
        job_content = json.loads(res.text)

        skills_str = ''

        # A dictionary about information of the vacancy
        vacancy_dict = {'job_name': '', 'company_name': '', 'salary': '', 'job_description': '',
                        'company_page': '', 'address': '', 'link': '', 'MS SQL': '0', 'MySQL': '0',
                        'JavaScript': '0', 'C#': '0', 'HTML': '0', 'ASP.NET': '0', 'Java': '0', 'jQuery': '0',
                        'Oracle': '0', 'Linux': '0'}

        try:
            skill_list = job_content['data']['condition']['specialty']

            # from skill dict get skills
            for skill in skill_list:
                skills_str += skill['description'] + ','

            for skills in skills_str.split(','):
                if skills in vacancy_dict:
                    vacancy_dict[skills] = '1'

            vacancy_dict['job_name'] = job_content['data']['header']['jobName']
            vacancy_dict['company_name'] = job_content['data']['header']['custName']
            vacancy_dict['salary'] = job_content['data']['jobDetail']['salary']
            vacancy_dict['job_description'] = job_content['data']['jobDetail']['jobDescription']
            vacancy_dict['company_page'] = job_content['data']['header']['custUrl']
            vacancy_dict['address'] = job_content['data']['jobDetail']['addressRegion'] + \
                                      job_content['data']['jobDetail']['addressDetail']
            vacancy_dict['link'] = link

        except Exception as err:
            print(err.args)
            continue

        try:
            sql_str = "INSERT INTO `job` (`job_name`, `company_name`, `salary`," \
                      " `job_description`, `company_page`, `address`, `link`, `MS_SQL`, `MySQL`," \
                      " `JavaScript`, `C_sharp`, `HTML`, `ASPNET`, `Java`, `jQuery`, `Oracle`, `Linux`)" \
                      " VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', " \
                      "\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\'); " \
                .format(vacancy_dict['job_name'], vacancy_dict['company_name'], vacancy_dict['salary'],
                        vacancy_dict['job_description'], vacancy_dict['company_page'], vacancy_dict['address'],
                        vacancy_dict['link'], vacancy_dict['MS SQL'], vacancy_dict['MySQL'], vacancy_dict['JavaScript'],
                        vacancy_dict['C#'], vacancy_dict['HTML'], vacancy_dict['ASP.NET'], vacancy_dict['Java'],
                        vacancy_dict['jQuery'], vacancy_dict['Oracle'], vacancy_dict['Linux'])
            cursor.execute(sql_str)
            print('Done')
        except Exception as err:
            print(err.args)

    time.sleep(random.randint(0, 5))

    print('換頁換頁換頁換頁換頁換頁換頁換頁換頁換頁換頁換頁換頁換頁換頁換頁')
