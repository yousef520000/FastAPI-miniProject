import mysql.connector as ms
def get_connection():
    return ms.connect(
        host="localhost",
        user="yousef5200",
        password="yousef123aA@",
        database="phpmyadmin"
    )

