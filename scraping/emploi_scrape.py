from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import base64

chrome_options = Options()
#chrome_options.add_argument("--headless")

def encode_link(link):
    encoded_bytes = base64.urlsafe_b64encode(link.encode("utf-8"))
    encoded_str = str(encoded_bytes, "utf-8")
    return encoded_str

def scrap_jobs():
    driver = webdriver.Chrome(options=chrome_options)
    jobs = []
    res = "3"
    for i in range(2): 
        if i > 0:
            res = "2"
        driver.get(f"https://www.emploi.ma/recherche-jobs-maroc?page={i}")            
        for _ in range(1,26):
            job = driver.find_elements(By.XPATH, f'/html/body/main/div[2]/div/div[{res}]/div/div[2]/div[2]/div[{_}]')
            job_link = driver.find_elements(By.XPATH, f'/html/body/main/div[2]/div/div[{res}]/div/div[2]/div[2]/div[{_}]/div/h3/a') 
            job_link = job_link[0].get_attribute('href')

            job_img = driver.find_elements(By.XPATH, f'/html/body/main/div[2]/div/div[{res}]/div/div[2]/div[2]/div[{_}]/picture/a/img')
            if len(job_img) == 0 :
                job_img = driver.find_elements(By.XPATH, f'/html/body/main/div[2]/div/div[{res}]/div/div[2]/div[2]/div[{_}]/picture/img')
            job_img = job_img[0].get_attribute('src')

            job_text = job[0].text
            job_text = job_text + f"\n{job_img}" + f"\n{job_link}"
            jobs.append(job_text)
    driver.quit()
    return data_organization(jobs)


def data_organization(arg):
    data = [jb.split("\n") for jb in arg]
    output = [{'image':j[-2],
            'title': j[0],
            'company': j[1],
            'location': [l for l in j if l.split()[0] == "Région"][0].split(": ")[1],
            'desc': j[2],
            'posted_date': datetime.strptime(j[-3], "%d.%m.%Y").strftime("%Y-%m-%d"),
            'competences': [y for y in j if y.split()[0] == "Compétences"][0].split(":")[1:][0] if [y for y in j if y.split()[0] == "Compétences"] else '',
            'link': encode_link(j[-1])} for j in data]
    return output