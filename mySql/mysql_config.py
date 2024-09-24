import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="job_offer_analysis"
)

cursor = connection.cursor()
