from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from Cloud_keywords import keywords
import re
from time import sleep
import csv

num_jobs = 200
page = 1
S_no = 1
role = 'Cybersecurity Analyst'
base_url = 'https://www.naukri.com/'+str(role)+'-jobs-'+str(page)
driver = webdriver.Firefox()
driver.get(base_url)
sleep(5)
i = 0
job = dict()

with open('Cybersecurity.csv', 'a', newline='') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(role)
    while i<num_jobs:
            #get details
        if (i+1) % 20 == 0:
            page = page + 1
            url = 'https://www.naukri.com/'+str(role)+'-jobs-'+str(page)
            driver.get(url)
            print('~~~~~~~~~~~~~~~~~~~~   Page '+str(page)+'   ~~~~~~~~~~~~~~~~~~~~~~~')
            sleep(2)
            act = ActionChains(driver)
            act.send_keys(Keys.PAGE_UP).perform()
            sleep(2)
        try:
            src = driver.page_source
            src = BeautifulSoup(src, "lxml")
            jobs = src.find("div", {'class': 'list'})
            job_details = jobs.find_all('article')[i % 20]
            job['name'] = (job_details.find('a',{'class':'title fw500 ellipsis'}).get_text().strip())
            job['company'] = (job_details.find('a',{'class':'subTitle ellipsis fleft'}).get_text().strip())

            experience = job_details.find('li',{'class':'fleft grey-text br2 placeHolderLi experience'}).find('span').get_text().strip()
            experience = experience.split('-')
            job['experience_min'] = (int("".join(re.findall(r'\d+', experience[0]))))
            job['experience_max'] = (int("".join(re.findall(r'\d+', experience[1]))))

            salary = job_details.find('li',{'class':'fleft grey-text br2 placeHolderLi salary'}).find('span').get_text().strip()
            if '-' in salary:
                salary = salary.replace(',','')
                salary = salary.split('-')
                job['salary_min'] = (int("".join(re.findall(r'\d+', salary[0])))/100000)
                job['salary_max'] = (int("".join(re.findall(r'\d+', salary[1])))/100000)
            else:
                job['salary_min'] = 'NA'
                job['salary_max'] = 'NA'

            try:
                job['skills'] = (job_details.find('ul',{'class':'tags has-description'}).get_text(",").strip())
            except:
                job['skills'] = 'NA'

            try:
                try:
                    driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[2]/section[2]/div[2]/article['+str((i)%20+1)+']').click()
                except:
                    driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[2]/section[2]/div[2]/article['+str((i)%20+1)+']').click()
            except:
                try:
                    driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[2]/section[2]/div[5]/article['+str((i)%20+1)+']').click()
                except:
                    driver.find_element_by_xpath(
                        '/html/body/div[2]/div[3]/div[2]/section[2]/div[5]/article[' + str((i)%20+1) + ']').click()



            sleep(2)
            driver.switch_to.window(driver.window_handles[1])
            src = driver.page_source
            src = BeautifulSoup(src,"lxml")
            try:
                desc = src.find('div',{'class':'dang-inner-html'}).get_text().strip()
            except:
                desc = 'no desc'
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            count_keywords = []
            for r in range(len(keywords)):
                if r < 6:
                    for words in keywords[r]:
                        if words.lower() + ' ' in desc.lower():
                            count_keywords.append(1)
                        elif words.lower() + '.' in desc.lower():
                            count_keywords.append(1)
                        elif words.lower() + ',' in desc.lower():
                            count_keywords.append(1)
                        elif words.lower() + '/' in desc.lower():
                            count_keywords.append(1)
                        elif words.lower() + ')' in desc.lower():
                            count_keywords.append(1)
                        else:
                            count_keywords.append(0)
                else:
                    for words in keywords[r]:
                        if words.lower() + ' ' in desc.lower():
                            count_keywords.append(1)
                            break
                        elif words.lower() + '.' in desc.lower():
                            count_keywords.append(1)
                            break
                        elif words.lower() + ',' in desc.lower():
                            count_keywords.append(1)
                            break
                        elif words.lower() + '/' in desc.lower():
                            count_keywords.append(1)
                            break
                        elif words.lower() + ')' in desc.lower():
                            count_keywords.append(1)
                            break
                        else:
                            count_keywords.append(0)
                            break
            if sum(count_keywords) ==0:
                print('fail')
                print(i+1)
            else:
                count_keywords = ','.join(str(count) for count in count_keywords)
                job['keyword_count'] = count_keywords
                row = []
                row.append(S_no)
                S_no = S_no+1
                for keys in job:
                    row.append(job[keys])
                print(count_keywords)
                print(i + 1)
                thewriter.writerow(row)
            i=i+1

        except:
            act = ActionChains(driver)
            act.send_keys(Keys.PAGE_DOWN).perform()
