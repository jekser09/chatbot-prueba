from core.ctrl_firebird import fb_sql

class sql_usuarios(fb_sql):

    def login(self,usuario:str,clave:str)->dict:
        '''Esta funcion valida la existencia de un usuario segun su nombre de usuario y contraseña y devuelve los datos'''
        query='''
            SELECT 
                c.USUARIO, c.CLAVE, c.INI_CL,
                c.NOM_CL, c.CLV_VENDE, c.CLV_RECNO
            FROM CLAVES c
            RIGHT JOIN MENUS m ON c.CLAVE = m.MEN_CLAVE
            WHERE USUARIO=? AND CLAVE=? AND m.ID_MENU=996
            '''
        consulta = self.buscar_uno(query=query,params=(usuario,clave))

        if consulta['estado']:
            consulta['data']={
                "usuario":consulta['data'][0].strip(),
                "iniciales":consulta['data'][2],
                "nombre":consulta['data'][3],
                "cod_vende":consulta['data'][4],
                "id_user":consulta['data'][5],
                "lista_menus": dict(self.lista_menus(consulta['data'][1]))
            }
        else: consulta['error'] = "Usuario o contraseña incorrectos" if consulta['error'] == "" else consulta['error']
        return consulta

    def lista_menus(self,clave:str)->list:
        '''Esta funcion devuelve la lista de menus disponibles para un usuario en concreto'''
        query="""
        SELECT um.URL_TEXT, um.DESCRIPCION
        FROM URL_MENUS um
        INNER JOIN MENUS m ON m.ID_MENU=um.URL_ID
        INNER JOIN CLAVES c ON m.MEN_CLAVE=c.CLAVE
        WHERE m.MEN_CLAVE=? AND m.ACCESO_MENU='T'
        """
        respuesta=self.buscar_todos(query=query,params=(clave,))
        if respuesta['estado']:
            urls=[]
            for url in respuesta['data']:
                urls.append((url[0].strip(),url[1]))
            return urls
        else: return []

