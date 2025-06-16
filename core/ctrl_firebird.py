from firebird.driver import connect, DatabaseError
from decouple import config
from decouple import UndefinedValueError

class fb_sql:
    # Esta clase se encarga de la gestión de la base de datos y es heredada en las aplicaciones que lo requieran
    def __init__(self) -> None:
        # Inicializa la conexión con Firebird y maneja el estado de la base de datos.
        self._cursor = None
        self._conn = None
        try:
            self._conn = connect(
                database=f'{config('FIREBIRD_HOST')}:{config('FIREBIRD_DB')}',
                user=config('FIREBIRD_USER'),
                password=config('FIREBIRD_PASSWORD'),
                charset=config('FIREBIRD_CHARSET', default='UTF8'))
            self.estado_db_bool = True
            self.estado_db_str = '✅ Conexión a la DB establecida.'
            self._cursor = self._conn.cursor()
        except UndefinedValueError:
            self.estado_db_bool = False
            self.estado_db_str = '🚫 Error: no se encontró una EV'
        except ValueError:
            self.estado_db_bool = False
            self.estado_db_str = '🚫 Error: no se pudo convertir el valor de una EV'
        except DatabaseError as db_err:
            self.estado_db_bool = False
            self.estado_db_str = f'🚫 Error de conexión: {db_err}'
        except Exception as e:
            self.estado_db_bool = False
            self.estado_db_str = f'⚠️ Error inesperado: {e}'

    # Permite usar la clase con 'with' para asegurar el cierre de la conexión.
    def __enter__(self):
        return self

    # Cierra la conexión automáticamente al salir de 'with'.
    def __exit__(self, exc_type, exc_value, traceback):
        self.cerrar_db()

    def buscar_uno(self, query: str, params=None) -> dict:
        # Ejecuta una consulta que devuelve una única fila.
        result = {"estado": False, "error": ""}
        if not self.estado_db_bool:
            return result
        try:
            self._cursor.execute(query, params or ())
            data = self._cursor.fetchone()
            if data:
                result['estado'] = True
                result['data'] = data
            else:
                result['error'] = ""
        except Exception as e:
            result['error'] = f'Error al obtener datos de la DB: {e}'
        return result

    def buscar_todos(self, query: str, params=None) -> dict:
        # Ejecuta una consulta que devuelve múltiples filas
        result = {"estado": False, "error": ""}
        if not self.estado_db_bool:
            result['error'] = self.estado_db_str
            return result
        try:
            self._cursor.execute(query, params or ())
            data = self._cursor.fetchall()
            if data:
                result['estado'] = True
                result['data'] = data
            else:
                result['error'] = ""
        except Exception as e:
            result['error'] = f'Error al obtener datos de la DB: {e}'
        return result

    def ejecutar_query(self, query: str, params=None) -> dict:
        # Ejecuta un query SQL de INSERT, UPDATE o DELETE y hace commit.
        result = {"estado": False, "error": ""}
        if not self.estado_db_bool:
            result['error'] = self.estado_db_str
            return result
        try:
            self._cursor.execute(query, params or ())
            self._conn.commit()
            result['estado'] = True
        except Exception as e:
            result['error'] = f'Error al ejecutar el query: {e}'
        return result

    def ejecutar_querys(self, query: str, params=None) -> dict:
        # Ejecuta un query múltiples veces dependiendo de la cantidad de datos y hace commit
        result = {"estado": False, "error": ""}
        if not self.estado_db_bool:
            result['error'] = self.estado_db_str
            return result
        try:
            self._cursor.executemany(query, params or [])
            self._conn.commit()
            result['estado'] = True
        except Exception as e:
            result['error'] = f'Error al ejecutar query: {e}'
        return result

    def cerrar_db(self) -> None:
        # Libera los recursos de la DB
        if self._cursor:
            self._cursor.close()
        if self._conn:
            self._conn.close()

    def estado_db(self) -> dict:
        return {"estado": self.estado_db_bool, "msg": self.estado_db_str}