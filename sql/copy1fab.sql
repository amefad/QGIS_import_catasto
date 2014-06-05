TRUNCATE TABLE fab1;
COPY fab1 from 'C:/vilcatasto/f1.FAB' WITH CSV DELIMITER '|';
TRUNCATE TABLE fab2;
COPY fab2 from 'C:/vilcatasto/f2.FAB' WITH CSV DELIMITER '|';
TRUNCATE TABLE fab2ext;
COPY fab2ext (
   id_fab2 ,
   --identificativo in poi vengono 
   id_sezioneurbana ,
   id_foglio ,
   id_numero ,
   id_denominatore ,
   id_subalterno ,
   id_edificialita ,
   extra )
from 'C:/vilcatasto/f2ext.FAB' WITH CSV DELIMITER '|';

TRUNCATE TABLE fab3;
COPY fab3 from 'C:/vilcatasto/f3.FAB' WITH CSV DELIMITER '|';
TRUNCATE TABLE fab3ext;
COPY fab3ext 
(   id_fab3 ,
   --tabella indirizzi max 4 (0-3)
   in_toponimo  ,
   in_indirizzo ,
   in_civico1 ,
   in_civico2 ,
   in_civico3 ,
   in_codicestrada ,
   extra 
)
from 'C:/vilcatasto/f3ext.FAB' WITH CSV DELIMITER '|';



TRUNCATE TABLE fab4;
COPY fab4 from 'C:/vilcatasto/f4.FAB' WITH CSV DELIMITER '|';
TRUNCATE TABLE fab4ext;
COPY fab4ext 
   (id_fab4,
   u_sezioneurbana ,
   u_foglio ,
   u_numero ,
   u_denominatore ,
   u_subalterno ,
   extra )

from 'C:/vilcatasto/f4ext.FAB' WITH CSV DELIMITER '|';

TRUNCATE TABLE fab5;
COPY fab5 from 'C:/vilcatasto/f5.FAB' WITH CSV DELIMITER '|';
TRUNCATE TABLE fab5ext;
COPY fab5ext 
   (

   id_fab5 ,
   r_codiceriserva ,
   r_partitaiscrizioneriserva ,
   extra )

from 'C:/vilcatasto/f5ext.FAB' WITH CSV DELIMITER '|';