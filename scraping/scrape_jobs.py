import sys
import os
import emploi_scrape
import rekrute_scrape
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mySql.mysql_config import connection, cursor


def scrape_jobs():
    jobs1 = emploi_scrape.scrap_jobs()
    jobs2 = rekrute_scrape.scrap_jobs()
    jobs = jobs1 + jobs2
    return jobs
  
def save_job_offer(job_offer):
    query = """
    INSERT IGNORE INTO job_offers (title, company, location, description, competences, posted_date, image, link)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        job_offer['title'],
        job_offer['company'],
        job_offer['location'],
        job_offer['desc'],
        job_offer['competences'],
        job_offer['posted_date'],
        job_offer['image'],
        job_offer['link']
    ))
    connection.commit()

    if cursor.rowcount == 0:
        print("Duplicated")
    else:
        print("Saved")


def save_to_mysql(jobs):
    for j in jobs:
        save_job_offer(j)


if __name__ == '__main__':
    offers = scrape_jobs()
    save_to_mysql(offers)
