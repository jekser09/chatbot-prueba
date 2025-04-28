from ctrl_firebird import fb_sql

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
                AND (GRUPO=2 OR (GRUPO=99 AND LINEA=3))
                AND p.PRE_CLIENTE=48
            ORDER BY CODPRO
        '''
        return self.buscar_todos(query=query,params=None)
        