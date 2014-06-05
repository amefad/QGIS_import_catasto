#!/usr/bin/env python
# -*- coding: utf-8 -*-

#File query.py Amedeo Fadini - (Rolando & Amedeo) 16/10/2012
#utilizzato per effettuare delle query da un layer di qgis tramite il comando "azioni"
#questo file va salvato in un percorso facilmente raggiungibile e richiamato da una azione di Qgis
#
#l'azione va inserita tra la proprietà del layer e rimane salvata nel progetto di qgis
#	Tipo di azione: Windows
#	Cattura dell'output: si
#	Testo dell'azione: python [percorso]/query.py [stringa di connessione] [query] [intestazioni_colonne]

#[percorso]
#sostituire con il percorso del file
#[stringadi connessione]
#la stringa di connessione contiene nome del server, database, utente, password separati da spazi esempio:
#"host=v-gpe dbname=villorba user=postgres password=postgres"
#[query] la query sql da eseguire (tra virgolette doppie). esempio:
#"select a_cognome, a_nome, a_codicefiscale, i_denominazione, i_codicefiscale, t_quotanumeratore, t_quotadenominatore, to_char(datainizio, 'DD/MM/YYYY') as atto_gen, to_char(datafine, 'DD/MM/YYYY') as atto_conc  from proprietari where i_identificativoimmobile='[% "i_identificativoimmobile" %]' order by datafine" 
#[intestazioni_colonne]
#lista delleintestazioni delle colonne da usare (tra virgolette doppie, separate da virgole) esempio:
#"a_cognome, a_nome, a_codicefiscale, i_denominazione, i_codicefiscale, quota_num, quota_den, datainizio, datafine"




import psycopg2
import sys
from PyQt4 import QtCore, QtGui



#queste righe leggono il contenuto dei primi tre argomenti della riga di comando
connection=sys.argv[1] 
q=sys.argv[2]
str= sys.argv[3]
col=str.split(',',)

#query di test togliere i commenti per il debug
#col="['a_cognome', 'a_nome', 'a_codicefiscale', 'i_denominazione', 'i_codicefiscale', 't_quotanumeratore',  't_quotadenominatore', 'datainizio', 'datafine' ]"
#q='select a_cognome, a_nome, a_codicefiscale, i_denominazione, i_codicefiscale, t_quotanumeratore, t_quotadenominatore, to_char(datainizio, \'DD/MM/YYYY\') as datainizio, to_char(datafine, \'DD/MM/YYYY\') as datafine   from proprietari where i_identificativoimmobile=\'1007551\' order by id'
#connection="host=v-gpe dbname=villorba user=postgres password=postgres"

#crea la finestra per la tabella
app = QtGui.QApplication(sys.argv)
wnd = QtGui.QWidget()
table_widget = QtGui.QTableWidget()
layout = QtGui.QVBoxLayout()
layout.addWidget(table_widget)
wnd.setLayout(layout) 
#connessione al db e query
con = psycopg2.connect(connection)
cur = con.cursor()
cur.execute(q)
data = cur.fetchall()

lines = len(data)
if lines == 0:
	columns= 0
else:
	columns =  len(data[0])
i = 1
j = 0
table_widget.setSortingEnabled(True)
table_widget.setRowCount(lines)
table_widget.setColumnCount(columns)
table_widget.setHorizontalHeaderLabels(col)
for i in range(lines):#parse lines
   for j in range(columns):#parse  columns
	   #print  i + j
	   if data[i][j] is None:
			item=QtGui.QTableWidgetItem('na')
	   else:
			item = QtGui.QTableWidgetItem(data[i][j])
	   table_widget.setItem(i, j, item)
# now sort
table_widget.sortByColumn(0, QtCore.Qt.DescendingOrder)
#dimensione della finestra
wnd.resize(640, 300)
wnd.show()
sys.exit(app.exec_())
