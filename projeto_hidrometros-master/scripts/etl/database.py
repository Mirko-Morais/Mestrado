import etl.variables as var
from sqlalchemy import create_engine

class Vertica():
    def __init__(self):
        self._vrt_connection_string = 'vertica+vertica_python://{username}:{password}@{hostname}:{port}/{database}'
        self._vrt_engine = create_engine(
            self._vrt_connection_string.format(
                username='{}'.format(var.vertica_credentials['USR']),
                password='{}'.format(var.vertica_credentials['PWD']),
                hostname='{}'.format(var.vertica_credentials['IP']),
                port=var.vertica_credentials['PORT'],
                database='{}'.format(var.vertica_credentials['DB'])            
            )
        )

    def get_engine(self):
        return self._vrt_engine

class Prax():
    def __init__(self):
        self._oracle_connection_string = 'oracle+cx_oracle://{username}:{password}@{hostname}:{port}/{database}'
        self._oracle_engine = create_engine(
            self._oracle_connection_string.format(
                username='{}'.format(var.prax_credentials['USR']),
                password='{}'.format(var.prax_credentials['PWD']),
                hostname='{}'.format(var.prax_credentials['IP']),
                port=var.prax_credentials['PORT'],
                database='{}'.format(var.prax_credentials['DB'])  
            )
            ,convert_unicode=True
        )

    def get_engine(self):
        return self._oracle_engine


class Datawarehouse():
    def __init__(self):
        self._pg_connection_string = 'postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database}'
        self._pg_engine = create_engine(
            self._pg_connection_string.format(
                username='{}'.format(var.datawarehouse_credentials['USR']),
                password='{}'.format(var.datawarehouse_credentials['PWD']),
                hostname='{}'.format(var.datawarehouse_credentials['IP']),
                port=var.datawarehouse_credentials['PORT'],
                database='{}'.format(var.datawarehouse_credentials['DB'])  
            )
        )

    def get_engine(self):
        return self._pg_engine