import mysql.connector
from mysql.connector import Error
import datetime
import configparser
import matplotlib.pyplot as plt
import argparse
import numpy as np
parser = argparse.ArgumentParser()
parser.add_argument("-n", type=str, required= True, help="seleziona la nazione per la quale estrarre i dati es: italy")
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
NazioneScelta = args.n
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM casinazione where Nazione = %s order by ID desc LIMIT 3", (NazioneScelta,))
res = mycursor.fetchall()
mycursor.close()
colors = ['b','g','r']
z=0
c=0
barWidth = 0.25
r1 = np.arange(5)
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]

r=[r1,r2,r3]
for i in res:
    bars1 = [i[2], i[4], i[6], i[7],i[8]]
    plt.suptitle(args.n)
    plt.bar(r[z], bars1, color=colors[z], width=barWidth, edgecolor='white', label=str(i[10]))
    if z==2:
        z = 0
    else:
        z = z + 1


plt.xticks([r + barWidth for r in range(len(bars1))], ['Casi Totali', 'Morti', 'Ricoverati', 'Casi Attivi', 'Critici'])

plt.legend()
plt.show()

exit('estrazione finita')
