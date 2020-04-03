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

ss = requests.session()

# The variable of work-context dictionary
work_dict_urls = []

for page in range(1, 51):
    url = 'https://www.104.com.tw/jobs/search/?ro=0&keyword=' \
          + keyword + '&order=15&asc=0&page=' + str(page) + '&mode=s'

    res = ss.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    # A dictionary about information of the vacancy
    vacancy_dict = {'job_name': '', 'company_name': '', 'salary': '', 'job_description': '',
                    'company_page': '', 'address': '', 'link': '', 'MS SQL': '0', 'MySQL': '0',
                    'JavaScript': '0', 'C#': '0', 'HTML': '0', 'ASP.NET': '0', 'Java': '0', 'jQuery': '0',
                    'Oracle': '0', 'Linux': '0'}

    # most_mentioned_skills = {'MS SQL': '0', 'MySQL': '0', 'JavaScript': '0', 'C#': '0', 'HTML': '0', 'ASP.NET': '0',
    #                          'Java': '0', 'jQuery': '0', 'Oracle': '0', 'Linux': '0'}

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
            skill_list = job_content['data']['condition']['specialty']

            # There are problems with skills

            # from skill dict get skills

            # if len(skill_list) > 1:
            #     for skill in skill_list:
            #         if skill in vacancy_dict:
            #             vacancy_dict[skill] = '1'
            # else:
            #     print('fuck you')

            vacancy_dict['job_name'] = job_content['data']['header']['jobName']
            vacancy_dict['company_name'] = job_content['data']['header']['custName']
            vacancy_dict['salary'] = job_content['data']['jobDetail']['salary']
            vacancy_dict['job_description'] = job_content['data']['jobDetail']['jobDescription']
            vacancy_dict['company_page'] = job_content['data']['header']['custUrl']
            vacancy_dict['address'] = job_content['data']['jobDetail']['addressRegion'] + \
                                      job_content['data']['jobDetail']['addressDetail']
            # vacancy_dict['skills'] = skills_str

        except Exception as err:
            print(err.args)
            continue

        # Connect the database
        db = MySQLdb.connect(host='localhost', user='root', passwd='root', db='py104', port=3306, charset='utf8')
        cursor = db.cursor()
        db.autocommit(True)

        try:
            sql_str = "INSERT INTO `job` (`job_name`, `company_name`, `salary`," \
                      " `job_description`, `company_page`, `address`, `link`)" \
                      " VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\'); " \
                .format(vacancy_dict['job_name'], vacancy_dict['company_name'], vacancy_dict['salary'],
                        vacancy_dict['job_description'], vacancy_dict['company_page'], vacancy_dict['address'],
                        vacancy_dict['link'])
            cursor.execute(sql_str)
            print('Done')
        except Exception as err:
            print(err.args)

    time.sleep(random.randint(0, 5))

    print('換頁換頁換頁換頁換頁換頁換頁換頁換頁換頁換頁換頁換頁換頁換頁換頁')