import mysql.connector
from mysql.connector import Error
import datetime
import configparser
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n", type=str, help="seleziona la nazione per la quale estrarre i dati es: italy")
args = parser.parse_args()

config = configparser.ConfigParser()
configurazione = config.read('config.ini')
if not configurazione:
    exit('file config.ini non trovato')
else:
    hostDB = config['mysqlDB']['host']
    userDB = config['mysqlDB']['user']
    passwdDB = config['mysqlDB']['pass']
    dbDB = config['mysqlDB']['db']
if not hostDB or not userDB or not passwdDB or not dbDB:
    exit('parametri file config.ini non definiti')

try:
    mydb = mysql.connector.connect(host = hostDB,
           user = userDB,
           passwd = passwdDB,
           db = dbDB)
    print('stabilita connessione al DB')
except:
    exit('impossibile stabilire connessione al DB')
nation = args.n
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM casinazione where Nazione = %s", (nation,))
res = mycursor.fetchall()
mycursor.close()
for i in res:
    plt.suptitle(args.n +', '+str(i[10]))
    plt.bar(['Casi Totali', 'Morti', 'Ricoverati', 'Casi Attivi', 'Critici'],[i[2], i[4], i[6], i[7],i[8]])
    plt.show()
