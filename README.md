QGIS_import_catasto
===================

Basato sul plugin per QGIS CXF_In di Fabio Saccon, un progetto per importare e gestire tutti i dati catastali in QGIS


Ho apprezzato tantissimo il plugin CXF_in che consente di importare le geometrie dei file cxf in un layer in memoria

http://plugins.qgis.org/plugins/Cxf_in/

Quel che sto cercando di fare è espandere questo plugin in modo da gestire sia le geometrie in CXF che i dati alfanumerici del catasto in un unico database postgis. 
I dati catastali censuari sono distribuiti in file di testo .FAB, .SOG, .TIT e sono collegabili alla cartografia tramite foglio e mappale.

le specifiche dei dati censuari sono qui: 
http://wwwt.agenziaentrate.gov.it/mt/ServiziComuniIstituzioni/ES-23-IS-05_100909.pdf


Molti hanno lavorato con il software Catsto_2000 che consentiva di importare i dati censuari in un database MS access, io ho preferito fare una struttura del DB ex-novo, che ricalca la struttura record presente nei file di testo creando una tabella per ciascun tipo record e sotto-record. (questo anceh perché non ho mai usato catasto 2000)

Uno script python crea un file di testo con i campi separati da "|"  per ogni tipo record, poi lo posso importare con COPY nella tabella corrispondente del database.


Lo scopo di tutto e' calcolare agevolmente l'ICI/IMU dovuta sulle aree fabbricabili.





