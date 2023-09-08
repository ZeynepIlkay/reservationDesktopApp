import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

user = os.environ['PYTHON_GUI_USER']
password = os.environ['PYTHON_GUI_PASSWORD'] 
host = os.environ['PYTHON_GUI_HOST']
database = os.environ['PYTHON_GUI_NAME']


config = {
    'user': user,
    'password': password,
    'host': host,  # Docker Compose ağı içindeki MariaDB servisinin ip
    'database': database, 
    'port': 3306,
}

mysqldb = mysql.connector.connect(**config)



'''

# MySQL sunucusuyla etkileşim
cursor = mysqldb.cursor()


# Sonuçları al
#result = cursor.fetchall()

# Bağlantıyı kapat
#mysqldb.close()
config = {
    'user' : 'root',
    'password' : 'database',
    'host' : 'localhost',
    'database' : 'reservation'
}'''

