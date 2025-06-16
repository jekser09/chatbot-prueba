from core.ctrl_firebird import fb_sql

class Bot_db(fb_sql):
    
    def get_productos(self)->dict:
        query='''
            SELECT
                i.CODPRO,
                i.NOMPRO,
                p.PRE_PRVTA
            FROM PRECIOS p
                LEFT JOIN INVENTARIO i ON p.PRE_PRODUCTO = i.CODPRO
            WHERE
                CATEGORIA!='Z'
                AND GRUPO=2
                AND p.PRE_CLIENTE=10001
            ORDER BY CODPRO
        '''
        return self.buscar_todos(query=query,params=None)

    def get_frases(self):
        query='''
            SELECT
                d.ID_DATA,
                d.ID_INTENCION,
                i.NOMBRE,
                d.FRASE
            FROM DATASET_CHAT d
            JOIN INTENCIONES_CHAT i ON i.ID_INTENCION=d.ID_INTENCION
        '''
        return self.buscar_todos(query=query)