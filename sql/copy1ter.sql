TRUNCATE TABLE ter1;
COPY ter1 from 'C:/vilcatasto/t1.TER' WITH CSV DELIMITER '|';
TRUNCATE TABLE ter2;
COPY ter2 from 'C:/vilcatasto/t2.TER' WITH CSV DELIMITER '|';
TRUNCATE TABLE ter2ext;
COPY ter2ext (
   id_ter2 ,
   --identificativo in poi vengono 
   simbolodeduzione ,
   extra )
from 'C:/vilcatasto/t2ext.ter' WITH CSV DELIMITER '|';

TRUNCATE TABLE ter3;
COPY ter3 from 'C:/vilcatasto/t3.ter' WITH CSV DELIMITER '|';
TRUNCATE TABLE ter3ext;
COPY ter3ext 
(  id_ter3 ,
   r_codiceriserva,
   r_partitaiscrizioneriserva,
   extra 
)
from 'C:/vilcatasto/t3ext.ter' WITH CSV DELIMITER '|';



TRUNCATE TABLE ter4;
COPY ter4 from 'C:/vilcatasto/t4.ter' WITH CSV DELIMITER '|';
TRUNCATE TABLE ter4ext;
COPY ter4ext 
   (id_ter4,
   po_idporzione ,
   po_qualita ,
   po_classe ,
   po_ettari ,
   po_are ,
   po_centiare,
   --campi solo se si usa il sistema di interscambio
   --po_redditodomincaleeuro ,
   --po_redditoagrarioeuro ,
   extra )

from 'C:/vilcatasto/t4ext.ter' WITH CSV DELIMITER '|';

