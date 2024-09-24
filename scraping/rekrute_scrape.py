from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.chrome.options import Options
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
    for i in range(1,3):
        driver.get(f'https://www.rekrute.com/fr/offres.html?s=3&p={i}&o=1')   
        for _ in range(1,51):
            job = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[1]/div[2]/div/div/div/div[3]/div/div[3]/ul/li[{_}]')
            job_link = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[1]/div[2]/div/div/div/div[3]/div/div[3]/ul/li[{_}]/div/div[2]/div/h2/a') 
            if job_link[0].text == "ExeKutive":
                job_link = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[1]/div[2]/div/div/div/div[3]/div/div[3]/ul/li[{_}]/div/div[2]/div/h2/a[2]') 
            job_link = job_link[0].get_attribute('href')

            job_img = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[1]/div[2]/div/div/div/div[3]/div/div[3]/ul/li[{_}]/div/div[1]/a/img')
            if len(job_img) == 0 :
                job_img = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[1]/div[2]/div/div/div/div[3]/div/div[3]/ul/li[{_}]/div/div[1]/img')
            job_img = job_img[0].get_attribute('src')
            job_text = job[0].text
            job_text = job_text + f"\n{job_img}" + f"\n{job_link}"
            jobs.append(job_text)
    driver.quit()    
    return data_organization(jobs)

def data_organization(arg):
    data = [jb.split("\n") for jb in arg]
    for j in data:
        try:
            if int(j[2]):
                    del(j[2])
        except:
            pass
    output = [{'image':j[-2],
            'title': j[1].split(" | ")[0],
            'company': "",
            'location': j[1].split(" | ")[1],
            'desc': j[3],
            'posted_date': datetime.strptime([y for y in j if y.split()[0] == "Publication"][0].split()[3], "%d/%m/%Y").strftime("%Y-%m-%d"),
            'competences': [y for y in j if y.split()[0] == "Fonction"][0].split(":")[1:][0] + " /" + [y for y in j if y.split()[0] == "Secteur"][0].split(":")[1:][0],
            'link': encode_link(j[-1])} for j in data]
    return output