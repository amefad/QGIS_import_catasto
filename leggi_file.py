"""
/***************************************************************************
CARICA CXF 
                                 A QGIS plugin

                             -------------------
        begin                : 2013-05-03
        copyright            : (C) 2013 by Amedeo Fadini
        email                : fame@libero.it
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""


      
true = 1
false = 0
from qgis.core import *
from qgis.gui import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_importa_imu import Ui_importa_imu
from insert_file import INSERT
import os
import sys
import string
import codecs
import csv
import ntpath
import glob
from datetime import datetime
import xml.etree.ElementTree as etree
#Should find a better way to do this rather then using regex
#Needs to be refactored into different lists.
# Need to add these with correct regex
# Spatial Data Transfer Standard (*catd.ddf *CATD.DDF) :  "^.*\.(shp)$"
# X-Plane/Flightgear (apt.dat nav.dat fix.dat awy.dat APT.DAT NAV.DAT FIX.DAT AWY.DAT)" :  "^.*\.(shp)$"
filters = {
   # 'File Terreni Agenzia del Territorio (*.ter *.TER)' : '^.*\.(ter)$',
   # 'File Fabbricati Agenzia  del Territorio (*.fab *.FAB)' : '^.*\.(fab)$',
   # 'File Soggetti Agenzia  del Territorio (*.sog *.SOG)' : '^.*\.(sog)$',
   # 'File Titolarita\' Agenzia  del Territorio (*.tit *.TIT)' : '^.*\.(tit)$'
   'File fornitura Agenzia  del Territorio (*.prm *.PRM)' : '^.*\.(prm)$',
   '[Vettore] File Agenzia del Territorio (*.cxf *.CXF)' : '^.*\.(cxf)$'
   
  }
class foglio(object):
    pass
class eAF(object):
    pass

"""This provides a lineno() function to make it easy to grab the line
number that we're on.

Danny Yoo (dyoo@hkn.eecs.berkeley.edu)
"""

import inspect

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

#########################
#variabili globali
#########################
#imposta la  directory temporanea
profile = os.path.expanduser('~')
tdir = ''
#variabile per valutare se è aggiornamento
deletefile = ''
aggiornamento = None
tipo= None
prmdata={}

def deltmp(self):
    list = os.listdir(tdir)
    for fileName in list:
        os.remove(tdir+"/"+fileName)
    global deletefile
    deletefile = true
    

class SELFILE(QDockWidget):
    #Signal notify when a file needs to be opened
    fileOpenRequest = pyqtSignal()



    def __init__(self):
        QDockWidget.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_importa_imu()
        self.ui.setupUi(self)



        #Load the filter list
        for key in sorted(filters.iterkeys()):
            self.ui.filtercombobox.addItem(key)

    def LoadFiles(self):
        self.model = QFileSystemModel(self.ui.Listafile)
        self.model.setRootPath(QDir.homePath())
        self.proxy = MyFilter()
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterKeyColumn(0)

        self.proxy.setFilterRegExp(QRegExp(filters[unicode(self.ui.filtercombobox.currentText())],Qt.CaseInsensitive,QRegExp.RegExp))

        self.ui.Listafile.setModel(self.proxy)
        self.ui.Listafile.setSortingEnabled(True)
        self.ui.Listafile.sortByColumn(0, Qt.AscendingOrder)  
        self.ui.Listafile.hideColumn(1)
        self.ui.Listafile.hideColumn(2)
        self.ui.Listafile.hideColumn(3)
        #Hack to make sure the horizontal scroll bar shows up
        self.ui.Listafile.header().setStretchLastSection(False)
        self.ui.Listafile.header().setResizeMode(QHeaderView.ResizeToContents)
        self.ui.Listafile.setColumnWidth(0,280)

        #Just hide the header because we don't need to see it.
        self.ui.Listafile.header().hide()
        self.ui.Listafile
        self.ui.filtercombobox.currentIndexChanged[QString].connect(self.filterChanged)
        self.ui.Listafile
        self.ui.Listafile.doubleClicked.connect(self.itemClicked)
		
        #TODO set linedit text with selected item
        #index = item.model().mapToSource(item)
		#self.ui.selPath.setText(unicode(self.model.filePath(index).toUtf8(),"utf-8"))
        self.ui.selButton.clicked.connect(self.buttonPressed)
    def filterChanged(self, text):
        self.proxy.setFilterRegExp(QRegExp(filters[str(text)],Qt.CaseInsensitive,QRegExp.RegExp))

    def itemClicked(self, item):
		
        index = item.model().mapToSource(item)
        filepath = unicode(self.model.filePath(index).toUtf8(),"utf-8")
        #We don't need to do anything if filepath is a directory.
        if os.path.isdir(filepath):
            return
		
        iterfile(self,filepath)
    def buttonPressed(self):
        filepath = unicode(self.ui.selPath.text().toUtf8(),"utf-8")
        QMessageBox.information(self, QCoreApplication.translate('rolando', "Primo testo"), QCoreApplication.translate('rolando', filepath))
        #We don't need to do anything if filepath is a directory.
        if os.path.isdir(filepath):
            return
        iterfile(self,filepath)

    def updateFilter(self, text):
        self.proxy.setFilterRegExp(QRegExp(text,Qt.CaseInsensitive,QRegExp.RegExp))
 
 
def load_cxf(filename):
  try:
      in_file = open(filename,"r")
  except IOError:
      print 'Impossibile aprire il file', filename
      sys.exit()
  #else:
  #print filename, 'ha', len(in_file.readlines()), 'linee'
  #in_file = open(filename,"r")
  
  
  def disarea(livello,codice ):
        geometria=[]
        area=[]
        lt_testo  = in_file.readline().strip()
        angolo  = in_file.readline().strip()
        #in_line  = in_file.readline().strip()
        x=float(in_file.readline().strip())
        y=float(in_file.readline().strip())
        orig1=[x,y]
        x=float(in_file.readline().strip())
        y=float(in_file.readline().strip())
        orig2=[x,y]
        #print orig1
        nrisole=int(in_file.readline().strip())
        nrverttot=int(in_file.readline().strip())
        #if nrisole > 0 :
        nrvertisola=[]

        for x in range(1,nrisole+1):
            nrvertisola.append(int(in_file.readline()))
        #print nrvertisola
        nrvertisola.insert(0,nrverttot-sum(nrvertisola))
        nrvertisola.insert(0,nrverttot-sum(nrvertisola))

        sgeometria="POLYGON"
        for isola,vert in enumerate(nrvertisola):
              sgeometria=sgeometria+"("
              for n in range (0,vert):
                  x=float(in_file.readline().strip())
                  y=float(in_file.readline().strip()) 
                 
                  geom= coord=[x,y]
                  if n == vert-1:
                    if isola==nrisole+1:
                        sgeom=str(x)+" "+str(y)+")"
                    else:
                        sgeom=str(x)+" "+str(y)+"),"
                  else:
                    sgeom=str(x)+" "+str(y)+","
                  sgeometria=sgeometria+sgeom
                  geometria.append(coord)
              area.append(geometria)
        sgeometria=sgeometria+")"
        #print sgeometria
        fet = QgsFeature()
        fet.setGeometry(QgsGeometry.fromWkt(sgeometria))
        fet.setAttributeMap( {0 : QVariant(mappa[0:4]),
                             1 : QVariant(mappa[4:5]),
                             2 : QVariant(mappa[5:9].lstrip('0')),
                             3 : QVariant(mappa[9:10]),
                             4 : QVariant(mappa[10:11]),
                             5 : QVariant(codice), 
                             6 : QVariant(livello), 
                             7 : QVariant(float(lt_testo)),
                             8 : QVariant(float(angolo)),
                             9 : QVariant(float(orig1[0])),
                             10 : QVariant(float(orig1[1]))} )  
        part.addFeatures( [ fet ] )
        vl_part.updateExtents()



  vl_part = QgsVectorLayer('Polygon', 'catasto_import', 'memory')
  part = vl_part.dataProvider()   
  part.addAttributes( [ QgsField("COMUNE", QVariant.String),
                      QgsField("SEZIONE", QVariant.String), 
                      QgsField("FOGLIO", QVariant.String), 
                      QgsField("ALLEGATO", QVariant.String),
                      QgsField("SVILUPPO", QVariant.String),
                      QgsField("NUMERO", QVariant.String),
                      QgsField("LIVELLO", QVariant.String),
                      QgsField("Htxt", QVariant.Double),
                      QgsField("Rtxt", QVariant.Double),
                      QgsField("Xtxt", QVariant.Double),
                      QgsField("Ytxt", QVariant.Double)]
                      )

  QgsMapLayerRegistry.instance().addMapLayer(vl_part)    
    
  file =ntpath.split(filename)[1]
 

  while true:
    in_line= in_file.readline().strip()
    if in_line == "":
        break
    #in_line = in_line[:-1]
    if in_line in ['MAPPA', 'QUADRO D\'UNIONE']:
       mappa = in_file.readline().strip()
       scala=in_file.readline().strip()
    elif in_line == 'BORDO':
        in_line  = in_file.readline().strip()
        if in_line[len(in_line)-1] == '+':
            disarea('FABBRICATI',in_line)
        elif in_line  == 'STRADA':
            disarea('STRADE',in_line)
        elif in_line  == 'ACQUA':
            disarea('ACQUE',in_line)
        elif in_line  == mappa:
            pass
			#disarea('Confine',in_line)
        elif len(in_line) == 11 :
            disarea('Sezioni',in_line)
        else:
            disarea('PARTICELLE',in_line)
  in_file.close()
  vl_part.startEditing()
  vl_part.commitChanges()

def load_prm(self,filename):
  try:
      in_file = open(filename,"r")
  except IOError:
      print 'Impossibile aprire il file', filename
      sys.exit()
  global prmdata
  
  while true:
    in_line= in_file.readline().strip()
    if in_line == "":
        break
    field = in_line.split(" :",1)
    prmdata[field[0].strip()]=field[1].strip()
    #QMessageBox.information(self,"Ok", field[0])
  dataelab = datetime.strptime(prmdata['Data elaborazione'], '%d/%m/%Y')
  QMessageBox.information(self,"Ok", prmdata['Tipologia di estrazione'].lower()+'\nElaborato il '+dataelab.strftime('%Y%m%d'))
  global aggiornamento
  if ('aggiornamento') in prmdata['Tipologia di estrazione'].lower():
    aggiornamento=1
  elif ('completa') in prmdata['Tipologia di estrazione'].lower():
    aggiornamento=0
  else:
    raise ErrorePRM('Impossibile stabilire il tipo di estrazione (completa o aggiornamento)')
  QMessageBox.information(self,"Ok","aggiornamento: "+str(aggiornamento))
  return prmdata
def iterfile(self,f):
	
	global deletefile, tdir
	ext = f[-3:]
	global tipo, tdir
	if (ext=='CXF'):
		load_cxf(f)
	elif (ext=='PRM'):
		load_prm(self,f)
		if aggiornamento==1:
			tdir = profile+"/.qgis/python/plugins/imu_import/tmp/"+'agg'+datetime.strptime(prmdata['Data elaborazione'], '%d/%m/%Y').strftime('%Y%m%d')+'/'
			if not os.path.exists(tdir):
				os.makedirs(tdir)
		elif aggiornamento==0:
			tdir = profile+"/.qgis/python/plugins/imu_import/tmp/"
		estrazione = prmdata['Tipologia di estrazione'].lower()
		if ('fabbricati') in estrazione:
			tipo="fabbricati"
		elif ('terreni') in estrazione:
			tipo="terreni"
		else:
			raise ErrorePRM('Impossibile stabilire se terreni o fabbricati')
		deletefile = false
		#ans = QMessageBox.information(self, 'Conversione file', 'Cancellare i file in tmp?', buttons= QMessageBox.No | QMessageBox.Yes )
		#if (ans == QMessageBox.Yes):
		#	deltmp(self)
		QMessageBox.information(self,"Ok", str(deletefile))
		dir = os.path.dirname(f)
		files = os.listdir(dir)
		#QMessageBox.information(self,"Ok", ' ,'.join(files))
		#TODO
		#prendere i nomi dei file dal file di fornitura
		msg=''
		for elem in files:
			insertlist = ["SOG", "TIT", "FAB", "TER", "SOG"]
			#insertlist = [ "TER" ]
			ext = elem[-3:]
			if ext in insertlist:
				#QMessageBox.information(self,"Ok", dir+'/'+elem+' da processare')
				msg = msg+elem+', '
				parse_file(self,dir+'/'+elem)
		QMessageBox.information(self,"Ok", msg+' importati correttamente')

def parse_file(self,f):
	
	#apre l'input e decodifica da latin-1
	fd = codecs.open(f, encoding='latin-1')
			# for line in fd:
			   # print repr(line)
			   # print repr(line.encode('utf-8'))
			# raise ValueError("uscita")
	#prepara i file di ouput in base all'input e assegna il numero corretto al campo tipo record e il numero di colonne della tabella principale
	ext = f[-3:]

	if ext == "FAB":
		 #questa lista definisce i fle di output
		 out = ["f1.FAB", "f2.FAB", "f2ext.FAB", "f3.FAB", "f3ext.FAB", "f4.FAB", "f4ext.FAB", "f5.FAB", "f5ext.FAB",]
		#definisce il campo chiave (tipo record)
		 key = 5
		 #quest'altra lista definisce i parametri in base al campo chiave 1-2-3-4-5 e per ciascun timpo x-subx-subr
		 param = [[45,0,0],[6,6,10],[6,6,4],[6,5,4],[6,2,10]]
	elif ext == "TER":
		 out = ["t1.TER", "t2.TER", "t2ext.TER", "t3.TER", "t3ext.TER", "t4.TER", "t4ext.TER"]
		 key = 5
		 #quest'altra lista definisce i parametri in base al campo chiave 1-2-3-4 e per ciascun timpo x-subx-subr
		 param = [[43,0,0],[6,1,7],[6,2,30],[6,6,20]]
		 #se il file è ottenuto tramite il sistema di interscambio (?) i campi del tr 4 sono due in più redddito agrario e domincale
		 #param = [[43,0,0],[6,1,7],[6,2,30],[6,8,20]]
	elif ext == "SOG":
		 #input dell'utente per capire se si riferiesce ai terreni o ai febbricati
		 #print "Stai importando i soggetti relativi ai fabbricati o ai terreni?"
		 QMessageBox.information(self,"Ok", 'Tipo import: '+tipo)
		 #tipo = raw_input("Inserisci f o t: ")
		 if tipo=="fabbricati":
			out = ["fabsP.SOG", "fabsG.SOG"]
		 elif tipo =="terreni":
			out = ["tersP.SOG", "tersG.SOG"]
		 key = 3
		 #quest'altra lista definisce i parametri in base al campo chiave 1-2-3-4 e per ciascun timpo x-subx-subr
		 param = [[11,0,0],[7,0,0]]
	elif ext == "TIT":
		 #input dell'utente per capire se si riferiesce ai terreni o ai febbricati
		 #print "Stai importando le titolarita' relative ai fabbricati o ai terreni?"
		 #tipo = raw_input("Inserisci f o t: ")
		 if tipo == "fabbricati":
			 out = ["fabi.TIT"]
		 elif tipo== "terreni":
			 out = ["teri.TIT"]
		 
		 key = 5
		 #quest'altra lista definisce i parametri in base al campo chiave P G e per ciascun timpo x-subx-subr
		 param = [[32,0,0]]
	#deletefile 1: true, 0: false
	if deletefile == 1:
		openmod = 'w+'
	else:
		openmod = 'a+'
	er = open(tdir+"error.txt", openmod)
		 
	#lista con i file di output
	ffo = []	 
	#apre file di ouput in utf-8 riempie una lista con i nomi 
	for file in out:
		i = codecs.open(tdir+file, encoding='utf-8', mode=openmod)
		
		ffo.append(i)
		#print ffo

	#imposta un id per il tipo record 2
	id1=id2=id3=id4=id5=id6=idp=idg=idt=0
	#ciclo legge le linee del file di input
	for  i,line in enumerate(fd,1):
		 campi = string.split(line, '|')
		
		 #test tipo record (
		 
		 n = len(campi)
		 #print "num campi: " + str(n)
		 tr = campi[key]
		 #print "tipo record: " + tr
		 #raise ValueError("uscita")

		 

		 ##azione in base al tipo record apre file corrispondente 
		 if    tr == '1':
			 id1 += 1
			 idr = id1
			 of = ffo[0]
			 p = param[0]
			 
		 elif  tr == '2':
			#tipo record 2 identificativi catastali
			#incrementa id per questo tipo record
			id2 += 1
			#imposta id per file di output
			idr = id2
			#file di ouptut tab principale
			of = ffo[1]
			#file di outpu tab secondaria

			off = ffo[2]
			#imposta i parametri per questo tipo record
			p = param[1]

		 elif  tr == '3':
			#tipo record 3
			id3 += 1
			idr = id3
			of = ffo[3]
			off = ffo[4]
			#imposta i parametri per questo tipo record
			p = param[2]
		 elif  tr == '4':
			id4 += 1
			idr = id4
			of = ffo[5]
			off = ffo[6]
			#imposta i parametri per questo tipo record
			p = param[3]
		 elif  tr == '5':
			id5 += 1
			idr = id5
			x=6

			of = ffo[7]
			off = ffo[8]
			#imposta i parametri per questo tipo record
			p = param[4]
		 elif  tr == 'P':
			idp += 1
			idr = str(idp)
			x=6
			of = ffo[0]
			#imposta i parametri per questo tipo record
			p = param[0]
		 elif  tr == 'G':
			idg += 1
			idr = str(idg) 
			of = ffo[1]
			x=6
			#imposta i parametri per questo tipo record
			p = param[1]
		 elif  tr  == "F":
			idt += 1
			idr = idt 
			of = ffo[0]
			x=6
			#imposta i parametri per questo tipo record
			p = param[0]
		 elif  tr  == "T":
			idt += 1
			idr = idt 
			of = ffo[0]
			x=6
			#imposta i parametri per questo tipo record
			p = param[0]
		 else:
			 of = er
			 line = 'impossibile trovare l\'output per il tipo di record "'+n+'" nel file '+f+' linea '+str(i)+'\n' 
		
		 #numero di campi di interesse per la tabella principale
		 x=p[0]
		 #numero di campi di interesse per la tabella secondaria
		 subx=p[1]
		 #numero max record  tabella secondaria
		 subr=p[2]




		 div = "|"
		 #crea una stringa concatenando i campi necessari
		 record=div.join(campi[0:(x)])
		 #aggiunge id e a capo riga
		 record = str(idr) + div + record + campi[-1]
		 #codifica la linea in utf8 com tipo byte
		 utfline = line.encode('utf-8')
		 #print utfline
		 #scrive la linea (non serve codificarla) 
		 of.write(record) 

		 
		 if n > x+1:
			 #calcola il numero di record secondari (è una divisione)
			 subr = (n-(x+1))/subx


			 
			 #imposta l'offset per i campi della tabella secondaria (inizia da uno e poi nel ciclo aumenta di subx
			 j = 0
			 for i in range(subr):


					 #print str(i) + "   " +str(subr)
					 #concatena i campi delal tab asecondaria e aggiunge un delimiter alla fine
					 subrecord=div.join(campi[(j+x):(j+x+subx)])+div
					 #aggiunge idrecord iniziale e a capo
					 subrecord = str(idr) + div + subrecord + campi[-1]
					 off.write(subrecord)
					 #incrementa j del numero di campi tabella scondaria
					 j = j + subx
					 

	#chiude lista con i file di output
	for file in ffo:
		 file.close()
	msg = "import file " + ext + " completato."
	#QMessageBox.information(self,"Ok", msg)
def insert_file(self):
	pass
class MyFilter(QSortFilterProxyModel):
    def __init__(self,parent=None):
        super(MyFilter, self).__init__(parent)

    def filterAcceptsRow (self, source_row, source_parent ):
        if self.filterRegExp() =="":
            return True #Shortcut for common case

        source_index = self.sourceModel().index(source_row, 0, source_parent)

        if self.sourceModel().isDir(source_index):
            return True

        return self.sourceModel().data(source_index).toString().contains(self.filterRegExp())

      

















