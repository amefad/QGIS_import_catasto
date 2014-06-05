"""
/***************************************************************************
								CARICA IMU 
                                 A QGIS plugin

                             -------------------
        begin                : 2013-04-27
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

from ui_importa_imu import Ui_importa_imu

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.gui import *
from qgis.utils import iface
from qgis.core import *
import sys
import math
import os
import string
import ntpath
import resources




from leggi_file import SELFILE
from leggi_file import deltmp
from insert_file import INSERT
from importaIMU import *

explorer = None
class importa():
    __module__ = __name__

    def __init__(self, iface):
        self.iface = iface




    def initGui(self):
        self.pluginname = '&QGIS Importatore IMU'
        self.actionConvert = QAction(QIcon(':/plugins/imu_import/icon.png'), self.pluginname, self.iface.mainWindow())
        self.iface.registerMainWindowAction(self.actionConvert, "F7")
        #self.action.triggered.connect(self.run)
        QObject.connect(self.actionConvert, SIGNAL("triggered()"), self.run)
        self.iface.addToolBarIcon(self.actionConvert)
        self.iface.addPluginToMenu('&importaIMU', self.actionConvert)
        self.actionImport = QAction(QIcon(":/plugins/imu_import/import_icon.png"), u"importa censuario nel db", self.iface.mainWindow())
        self.iface.registerMainWindowAction(self.actionImport, "Shift +F7")
        QObject.connect(self.actionImport, SIGNAL("triggered()"), self.importdb)
        self.iface.addToolBarIcon(self.actionImport)
        self.iface.addPluginToMenu('&importaIMU', self.actionImport)
        for action in self.iface.pluginMenu().actions():
            if (action.text() == self.pluginname):
                action.setIcon(QIcon(':/plugins/imu_import/icon.png'))




    def unload(self):
        self.iface.removePluginMenu('&importaIMU', self.actionConvert)
        self.iface.removeToolBarIcon(self.actionConvert)
        self.iface.removePluginMenu('&importaIMU', self.actionImport)
        self.iface.removeToolBarIcon(self.actionImport)



    def run(self):
        if os.path.exists(os.getenv("HOME")+'/workpath'):
         fpath = open(os.getenv("HOME")+'/workpath', 'r') 
         read_path = fpath.read()
         fpath.close
        else:
         read_path ="."     
        (filename, filter) = QFileDialog.getOpenFileNamesAndFilter(self.iface.mainWindow(),
                    "Seleziona un file cxf da caricare...",read_path,
                    "CXF e catasto files (*.cxf )",
                    "Filtro per selezione file")
        if len(filename)==0:
            return
        
        
        ###### selettore unico sr by Salvatore Caligiore
        selcrs=QgsGenericProjectionSelector()
        result=selcrs.exec_() 
        


        stringacrs=''
       
        if  result==1 :     
            crs=QgsCoordinateReferenceSystem()
            crs.createFromSrsId(selcrs.selectedCrsId ())   
            stringacrs="crs="+crs.toWkt()
            
            
        else:
             selcrs=QgsProjectionSelector()
             result=selcrs.exec_() 
             if  result==1 :  
                 crs=QgsCoordinateReferenceSystem()
                 crs.createFromSrsId(selcrs.selectedCrsId ())   
                 stringacrs="crs="+crs.toWkt()
             else:
                 stringacrs=''
             








        
             
        del selcrs
        ##########################    
        QMessageBox.information(None, "DEBUG:",stringacrs)  
        #vl_conf= QgsVectorLayer("Polygon?"+stringacrs+"&field=Codice_comune:string(50)&field=Foglio:string(5)&field=Mappale:string(5)&field=Allegato:string(5)&field=Sviluppo:string(5)&field=Htxt:Double&field=Rtxt:Double&field=Xtxt:Double&field=Ytxt:Double",
        #                   "Confine", "memory")  
        #QgsMapLayerRegistry.instance().addMapLayer(vl_conf)     
        vl_part = QgsVectorLayer("Polygon?"+stringacrs+"&field=Codice_comune:string(50)&field=Foglio:string(5)&field=Mappale:string(5)&field=Allegato:string(5)&field=Sviluppo:string(5)&field=Htxt:Double&field=Rtxt:Double&field=Xtxt:Double&field=Ytxt:Double",
                           "Particelle", "memory")
        #QgsMapLayerRegistry.instance().addMapLayer(vl_part)   
        vl_ed= QgsVectorLayer("Polygon?"+stringacrs+"&field=Codice_comune:string(50)&field=Foglio:string(5)&field=Mappale:string(5)&field=Allegato:string(5)&field=Sviluppo:string(5)&field=Htxt:Double&field=Rtxt:Double&field=Xtxt:Double&field=Ytxt:Double",
                           "Fabbricati", "memory")  
        #QgsMapLayerRegistry.instance().addMapLayer(vl_ed)   
        vl_st= QgsVectorLayer("Polygon?"+stringacrs+"&field=Codice_comune:string(50)&field=Foglio:string(5)&field=Mappale:string(5)&field=Allegato:string(5)&field=Sviluppo:string(5)&field=Htxt:Double&field=Rtxt:Double&field=Xtxt:Double&field=Ytxt:Double",
                           "Strade", "memory")  
        #QgsMapLayerRegistry.instance().addMapLayer(vl_st)
        vl_aq= QgsVectorLayer("Polygon?"+stringacrs+"&field=Codice_comune:string(50)&field=Foglio:string(5)&field=Mappale:string(5)&field=Allegato:string(5)&field=Sviluppo:string(5)&field=Htxt:Double&field=Rtxt:Double&field=Xtxt:Double&field=Ytxt:Double",
                           "Acque", "memory")  
        #QgsMapLayerRegistry.instance().addMapLayer(vl_aq)
        #vl_linee= QgsVectorLayer("Linestring?"+stringacrs+"&field=Codice_comune:string(50)&field=Fg:string(5)&field=Mappale:string(5)&field=All:string(5)&field=Sez:string(5)&field=Cod_linea:string(5)",
        #                   "Linee", "memory")
 
        #QgsMapLayerRegistry.instance().addMapLayer(vl_linee) 
        #vl_point= QgsVectorLayer("Point?"+stringacrs+"&field=Codice_comune:string(50)&field=Fg:string(5)&field=Mappale:string(5)&field=All:string(5)&field=Sez:string(5)&field=Simbolo:string(5)&field=Rot:Double",
        #                   "Simboli", "memory")  
        #QgsMapLayerRegistry.instance().addMapLayer(vl_point)
        
        #livelligruppofoglio=[vl_point,vl_linee,vl_aq,vl_st, vl_ed,vl_part,vl_conf]
        livelligruppofoglio=[vl_aq,vl_st, vl_ed,vl_part]		
        QgsMapLayerRegistry.instance().addMapLayers(livelligruppofoglio)
        
        
                        
        #QMessageBox.information(None, "DEBUG:",os.environ["PYTHONPATH"]+'/Cxf_in/part.qml') 
        vl_aq.loadNamedStyle(os.getenv("HOME")+'/.qgis2/python/plugins/Cxf_in/acque.qml')
        vl_part.loadNamedStyle(os.getenv("HOME")+'/.qgis2/python/plugins/Cxf_in/part.qml')
        vl_ed.loadNamedStyle(os.getenv("HOME")+'/.qgis2/python/plugins/Cxf_in/fab.qml')
        vl_st.loadNamedStyle(os.getenv("HOME")+'/.qgis2/python/plugins/Cxf_in/strade.qml')
        #vl_conf.loadNamedStyle(os.getenv("HOME")+'/.qgis2/python/plugins/Cxf_in/conf.qml')
        #vl_point.loadNamedStyle(os.getenv("HOME")+'/.qgis2/python/plugins/Cxf_in/simboli.qml')

        #vl_linee.loadNamedStyle(os.getenv("HOME")+'/.qgis2/python/plugins/Cxf_in/linee.qml')
        
        fpath = open(os.getenv("HOME")+'/workpath', 'w') 
        fpath.write(os.path.dirname(filename[0])) 
        fpath.close  
              
              
              
              
        for f in filename:
        

            liv=os.path.basename (os.path.splitext( str(f))[0])
            #load_cxf(str(f),liv,vl_part,vl_ed,vl_st,vl_aq,vl_conf,vl_linee,vl_point)
            load_cxf(str(f),liv,vl_part,vl_ed,vl_st,vl_aq)			

        vl_part.commitChanges()
        vl_ed.commitChanges()
        vl_st.commitChanges()
        vl_aq.commitChanges() 
        #vl_conf.commitChanges()
        #vl_linee.commitChanges()
        #vl_point.commitChanges()  
        
        li = iface.legendInterface()    
        index=li.addGroup(liv[0:10]) 
        
        for l in livelligruppofoglio:
            li.moveLayer(l, index)
 


    def importdb(self):
        INSERISCI

    def openFile(self, filePath):
        filename = unicode(filePath.toUtf8(), 'utf-8')





#if (__name__ == '__main__'):
   # app = QApplication(sys.argv)
   # win = QMainWindow(None)
   # explorer = fileDialog()
   # explorer.LoadFiles()
   # win.show()
   # retval = app.exec_()
   # sys.exit(retval)



