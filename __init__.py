"""
/***************************************************************************
CARICA SOG E TIT 
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

 This script initializes the plugin, making it known to QGIS.
"""
def name():
    return "Importa_IMU"
def description():
    return "Importatore file censuario"
def version():
    return "Version 0.1b"
def icon():
    return "icon.png"
def icon2():
    return "import_icon.png"
def qgisMinimumVersion():
    return "1.7.3"
def classFactory(iface):
    # load cxf_in class from file pippo
    from impcatasto import importa
    return importa(iface)
