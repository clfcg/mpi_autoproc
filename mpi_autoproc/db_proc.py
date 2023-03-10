import urllib
from configparser import ConfigParser

from sqlalchemy import Table, MetaData, create_engine, exc
from sqlalchemy.orm import Session

from log_collector import *


def get_engine():
    try:
        config_path = "mpi_autoproc/config.ini"
        conf = ConfigParser()
        conf.read(config_path)

        params = urllib.parse.quote_plus(
            f"DRIVER={conf['db_options']['driver']};"
            f"SERVER={conf['db_options']['host']};"
            f"DATABASE={conf['db_options']['dbname']};"
            f"UID={conf['db_options']['user']};"
            f"PWD={conf['db_options']['password']}"
            )
        engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
        conn = engine.connect()
        get_log("Соединение установлено.")
        conn.close()
        return engine
    except exc.SQLAlchemyError as err:
        get_log(err)
        exit()