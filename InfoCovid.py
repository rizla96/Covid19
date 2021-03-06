import configparser
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException as WDE
import warnings
from selenium.webdriver.firefox.options import Options
import mysql.connector
from mysql.connector import Error
import datetime
import re
import csv
import argparse
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-n", type=str, help="seleziona la nazione per la quale estrarre i dati es: italy")
args = parser.parse_args()


options = webdriver.ChromeOptions()
options.add_argument('headless')
#windows
driver = webdriver.Chrome( options = options)


driver.get('https://www.worldometers.info/coronavirus/')
if args.n:
    nation = driver.find_element_by_xpath('//*[@id="main_table_countries_today_filter"]/label/input')
    nation.send_keys(args.n)
    time.sleep(2)
corpoTabella = driver.find_element_by_xpath('//*[@id="main_table_countries_today"]/tbody[1]')
tr = corpoTabella.find_elements_by_tag_name('tr')

with open('casiNazione.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for i in tr:
        td = i.find_elements_by_tag_name('td')
        filewriter.writerow([td[0].text,str(re.sub(',','',td[1].text)),str(re.sub(',','',td[2].text)),str(re.sub(',','',td[3].text)),str(re.sub(',','',td[4].text)),str(re.sub(',','',td[5].text)),str(re.sub(',','',td[6].text)),str(re.sub(',','',td[7].text)),str(re.sub(',','',td[8].text))])


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
    connection = mysql.connector.connect(host = hostDB,
           user = userDB,
           passwd = passwdDB,
           db = dbDB)
    print('stabilita connessione al DB')
except:
    exit('impossibile stabilire connessione al DB')
giorno = (datetime.date.today(), )

with open('casiNazione.csv', 'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if(line_count%2==0):
            campi = row
            print(campi)
            try:
                time.sleep(1)
                CasTot = campi[1]
                MortTot = campi[3]
                Ric = campi[5]
                CasAtt = campi[6]
                Cri = campi[7]
                if not CasTot:
                    CasTot = 0
                if not MortTot:
                    MortTot = 0
                if not Ric:
                    Ric = 0
                if not CasAtt:
                    CasAtt = 0
                if not Cri:
                    Cri = 0
                mySql_insert_query = """INSERT INTO casinazione (Nazione, CasiTotali, NuoviCasi, MortiTotali, NuoviMorti, RicoveratiTotali, CasiAttivi, Critici, CasiDivMilione,dataRicerca)
                       VALUES
                       (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """

                cursor = connection.cursor()
                result = cursor.execute(mySql_insert_query, (campi[0], CasTot, campi[2], MortTot, campi[4], Ric, CasAtt, Cri, campi[8],giorno[0]))
                connection.commit()
                print("Record inserted successfully into urlht table")
                cursor.close()

            except mysql.connector.Error as error:
                print("Failed to insert record into urlht table {}".format(error))
        line_count += 1
if args.n:
    NazioneScelta = args.n
    mycursor = connection.cursor()
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
