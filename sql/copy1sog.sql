TRUNCATE TABLE sogp;
COPY sogp 
(
   nriga,
   c_codiceamministrativo , 
   c_sezione , 
   s_identificativosoggetto , 
   s_tiposoggetto ,
   a_cognome ,
   a_nome ,
   a_sesso ,
   a_datadinascita ,
   a_luogodinascita ,
   a_codicefiscale ,
   indicazionisupplementari 
)
from 'C:/vilcatasto/fabsP.SOG' WITH CSV DELIMITER '|' ESCAPE E'\\' QUOTE '#';

COPY sogp 
(
   nriga,		
   c_codiceamministrativo , 
   c_sezione , 
   s_identificativosoggetto , 
   s_tiposoggetto ,
   a_cognome ,
   a_nome ,
   a_sesso ,
   a_datadinascita ,
   a_luogodinascita ,
   a_codicefiscale ,
   indicazionisupplementari 
)
from 'C:/vilcatasto/tersP.SOG' WITH CSV DELIMITER '|' ESCAPE E'\\'  QUOTE '#';
TRUNCATE TABLE sogg;
COPY sogg
(
  
   nriga,
   c_codiceamministrativo , 
   c_sezione , 
   s_identificativosoggetto , 
   s_tiposoggetto ,
   i_denominazione ,
   i_sede ,
   i_codicefiscale 
)

from 'C:/vilcatasto/fabsG.SOG' WITH CSV DELIMITER '|' ESCAPE E'\\'  QUOTE '#';

COPY sogg
(
   nriga,
   c_codiceamministrativo , 
   c_sezione , 
   s_identificativosoggetto , 
   s_tiposoggetto ,
   i_denominazione ,
   i_sede ,
   i_codicefiscale 
)

from 'C:/vilcatasto/tersG.SOG' WITH CSV DELIMITER '|' ESCAPE E'\\'  QUOTE '#';