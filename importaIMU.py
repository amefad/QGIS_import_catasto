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
from qgis.utils import iface
from qgis.gui import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_importa_imu import Ui_importa_imu
import os
import sys
import string
import ntpath
import math
explorer = None


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
   'File fornitura Agenzia  del Territorio (*.prm *.TIT)' : '^.*\.(prm)$'
   
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

class SELFILE(QDockWidget):
    #Signal notify when a file needs to be opened
    fileOpenRequest = pyqtSignal()
    #imposta una directory temporanea
    profile = os.path.expanduser('~')
    tdir = profile+"/.qgis/python/plugins/imu_import/tmp/"


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
 
 
def load_cxf(filename,liv,vl_part,vl_ed,vl_st,vl_aq):
  try:
      in_file = open(filename,"r")
  except IOError:
      print 'Impossibile aprire il file', filename
      sys.exit()
  #else:
  #print filename, 'ha', len(in_file.readlines()), 'linee'
  #in_file = open(filename,"r")
  
  def dispoint(livello,codice ):
        geometria=[]
        simbolo= in_file.readline().strip()
        angolo= in_file.readline().strip()
        x=float(in_file.readline().strip())
        y=float(in_file.readline().strip()) 
        sgeometria="point ("+str(x)+" "+str(y)+")"
         
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromWkt(sgeometria))
        values = [(liv[0:4]),
                     (liv[5:9]),
                     (codice),                     
                     (liv[9:10]),
                     (liv[10:11]), 
                     (simbolo),            
                     (360-math.degrees(float(angolo)))
                     
                ]
        #QMessageBox.information(None, "DEBUG:",str(math.degrees(float(angolo))))  
       # QMessageBox.information(None, "DEBUG:",angolo)               
        feature.setAttributes(values)        
        vl_point.addFeature(feature,True)
        vl_point.updateExtents()       
        
        
        
  def dislinee(livello,codice ):

        geometria=[]
        lt_testo  = in_file.readline().strip()      
        vert=int(in_file.readline().strip())
        sgeometria="Linestring ("
        for n in range (0,vert):
                 
                  x=float(in_file.readline().strip())
                  y=float(in_file.readline().strip()) 
                 
                  geom= coord=[x,y]
                  if n == vert-1:
                    sgeometria=sgeometria+str(x)+" "+str(y)+")"
                  else:
                    sgeometria=sgeometria+str(x)+" "+str(y)+","
                
        #QMessageBox.information(None, "DEBUG:", sgeometria) 

        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromWkt(sgeometria))
        values = [(liv[0:4]),
                     (liv[5:9]),
                     (codice),                      
                     (liv[9:10]),
                     (liv[10:11]),
                     (float(lt_testo)),
]
        feature.setAttributes(values)        
        vl_linee.addFeature(feature,True)
        vl_linee.updateExtents()        
        
        
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
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromWkt(sgeometria))

        
        values = [(liv[0:4]),
                     (liv[5:9]),
                     (codice),                      
                     (liv[9:10]),
                     (liv[10:11]),
                     (float(lt_testo)),
                     (float(angolo)),
                     (float(orig1[0])),
                     (float(orig1[1]))]
        if livello=="Acque":
           
           feature.setAttributes(values)

           vl_aq.addFeature(feature,True)
           vl_aq.updateExtents()   
        if livello=="Confine":
















           

           feature.setAttributes(values)


           vl_conf.addFeature(feature,True)
           vl_conf.updateExtents()     
        if livello=="Strade":

           feature.setAttributes(values)

           vl_st.addFeature(feature,True)
           vl_st.updateExtents()
           
        if livello=="FABBRICATI":
              
            feature.setAttributes(values)       
            vl_ed.addFeature(feature,True)
            vl_ed.updateExtents()   
           
           
           
             
        if livello=="Particelle":

           feature.setAttributes(values)
           vl_part.addFeature(feature,True)
           vl_part.updateExtents()            
           if (orig1[0] <>  orig2[0]) and (orig1[1] <>  orig2[1]):
              sgeometria="Linestring ("+str(orig1[0])+" "+str(orig1[1])+","+str(orig2[0])+" "+str(orig2[1])+")"      
              feature = QgsFeature()
              feature.setGeometry(QgsGeometry.fromWkt(sgeometria))
              values = [(liv[0:4]),
                           (liv[5:9]),
                           (codice),                      
                           (liv[9:10]),
                           (liv[10:11]),
                           (float(lt_testo)),
      ]
              feature.setAttributes(values)        
              #vl_linee.addFeature(feature,True)
              #vl_linee.updateExtents()         
            


    
  file =ntpath.split(filename)[1]
 
  vl_part.startEditing()
  vl_ed.startEditing()
  vl_st.startEditing()
  vl_aq.startEditing()
  #vl_conf.startEditing()
  #vl_linee.startEditing()
  #vl_point.startEditing()
  while True:
    in_line= in_file.readline().strip()
    if in_line == "":
        break
    #in_line = in_line[:-1]
    if in_line in  ("MAPPA","QUADRO D\'UNIONE"):
       mappa = in_file.readline().strip()
       
       if in_line == 'QUADRO D\'UNIONE':
        mappa = "QU"
       scala=in_file.readline().strip()

    elif in_line == 'BORDO':
        in_line  = in_file.readline().strip()
        if in_line[len(in_line)-1] == '+':
            disarea('FABBRICATI',in_line)
        elif in_line  == 'STRADA':
            disarea('Strade',in_line)
        elif in_line  == 'ACQUA':
            disarea('Acque',in_line)
        # elif in_line  == mappa:

            # disarea('Confine',in_line)
        # elif mappa=="QU":
            # disarea('Confine',in_line)            
        elif len(in_line) == 11 :
            disarea('Sezioni',in_line)
        else:

            disarea('Particelle',in_line)
    # if in_line == "LINEA" :
            # dislinee("Linee",in_line) 
    # if in_line == "SIMBOLO" :
            # dispoint("Simboli",in_line)            
  in_file.close()

#amedeo
def iterfile(self,f):
	dir = os.path.dirname(f)
	files = os.listdir(dir)
	#QMessageBox.information(self,"Ok", ' ,'.join(files))
	#TODO
	#prendere i nomi dei file dal file di fornitura
	msg=''
	for elem in files:
		insertlist = ["SOG", "TIT", "FAB", "TER", "SOG"]
		#insertlist = [ "TER" ]
		
		if elem[-3:] in insertlist:
			#QMessageBox.information(self,"Ok", dir+'/'+elem+' da processare')
			msg = msg+elem+', '
			parse_file(self,dir+'/'+elem)
	QMessageBox.information(self,"Ok", msg+' importati correttamente')

def parse_file(self,f):
			

		# if sys.argv[1]==None:
			 # #chiede all'utente di indicare il file
			 # f = raw_input("scrivi il percorso del file: \n")
		# else:
			 # f = sys.argv[1]

		#apre l'input
		try:
			fd = open(f,"r")
		except IOError:
			er.writelines('Impossibile aprire il file'+ f)
			sys.exit()
			

		#prepara i file di ouput
		ext = f[-3:]
		if ext == "FAB":
			 out = ["f1.FAB", "f2.FAB", "f3.FAB", "f4.FAB", "f5.FAB"]
			 key = 5
		elif ext == "TER":
			 out = ["f1.TER", "f2.TER", "f3.TER", "f4.TER"]
			 key = 5
		elif ext == "SOG":
			 out = ["fP.SOG", "fG.SOG"]
			 key = 3
		elif ext == "TIT":
			 out = ["fP.TIT", "fG.TIT"]
			 key = 3
		er = open(tdir+"error.txt", "w")
			 
		#lista con i file di output
		ffo = []	 
		#apre file di ouput
		for file in out:
			 i = open( tdir+file,"w")
			 ffo.append(i)
			 

		for  i,line in enumerate(fd,1):
			 campi = string.split(line, '|')
			 #test tipo record
			 
			 n = campi[key]
			 #apre file corrispondente
			 if    n == '1':
				 of = ffo[0]
			 elif  n == '2':
				 of = ffo[1]
			 elif  n == '3':
				 of = ffo[2]
			 elif  n == '4':
				 of = ffo[3]
			 elif  n == '5':
				 of = ffo[4]
			 elif  n == 'P':
				 of = ffo[0]
			 elif  n == 'G':
				 of = ffo[1]
			 else:
				 of = er
				 line = 'impossibile trovare l\'output per il tipo di record "'+n+'" nel file '+f+' linea '+str(i)+'\n' 
			 #print line,
			 of.writelines(line)
		#chiude file errore
		er.close()
		#chiude lista con i file di output
		for file in ffo:
			 file.close()
		msg = "import file " + ext + " completato."
		#QMessageBox.information(self,"Ok", msg)

# def insert_file(self, file)

# class MyFilter(QSortFilterProxyModel):
    # def __init__(self,parent=None):
        # super(MyFilter, self).__init__(parent)

    # def filterAcceptsRow (self, source_row, source_parent ):
        # if self.filterRegExp() =="":
            # return True #Shortcut for common case

        # source_index = self.sourceModel().index(source_row, 0, source_parent)

        # if self.sourceModel().isDir(source_index):
            # return True

        # return self.sourceModel().data(source_index).toString().contains(self.filterRegExp())

      





