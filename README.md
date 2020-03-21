# Covid-19
Applicazione per l'estrazione automatica delle informazioni sul covid-19 come il numero totale di contagiati, di morti di ricoverati.
## Requisiti
**python3**

Installare le seguenti librerie con **pip** https://pip.pypa.io/en/stable/quickstart/

- `selenium` https://selenium-python.readthedocs.io/
- `mysql connector` https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html
- `re` https://docs.python.org/3/library/re.html
- `configparser` https://docs.python.org/3/library/configparser.html
- `argparse` https://docs.python.org/3/library/argparse.html

Scaricare il driver per la vostra versione di Google Chrome da questo link https://chromedriver.chromium.org/downloads.

## Struttura progetto
- `DBstruttura.sql`: file in formato sql che contiene la struttura del database utilizzato.
- `config.ini`: file di configurazione per l'accesso al database.
- `InfoCovid.py`: file python che esegue l'estrazione delle informazioni

## Procedimento
- Importare la struttura del database utilizzando il file `DBstruttura.sql`, creando così il DB (verificare che non sia presente un omonimo DB).
- Modificare il file `config.ini` secondo le proprie credenziali.
- Eseguire il file `InfoCovid.py` inserendo in input: **-n** seguito dalla nazione(in lingua inglese) desiderata.
**Esempio: python InfoCovid.py -n italy**
![InfoCovid](https://user-images.githubusercontent.com/51764993/77183963-6005f880-6acf-11ea-903e-143ff04ad559.png)
oppure eseguirlo senza valori in input per estrarre le informazioni da tutte le nazioni.
![InfoCovidGen](https://user-images.githubusercontent.com/51764993/77183833-3b118580-6acf-11ea-8cab-750ff8475896.png)
Nel caso decidiate di estrarre per una specifica nazione verrà mostrati dei grafici riassuntivi per la nazione scelta.
- Eseguire il file `plot.py` inserendo in input: **-n** seguito dalla nazione(in lingua inglese) desiderata, verrano cosi mostrati dei grafici riassuntivi.
**Esempio: python plot.py -n italy**
![plot](https://user-images.githubusercontent.com/51764993/77228953-1c70c480-6b8b-11ea-8222-aed96b0a3776.png)
