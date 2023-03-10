import urllib
from configparser import ConfigParser
from datetime import datetime, timedelta

from sqlalchemy import create_engine, exc, text
from sqlalchemy.orm import Session

from mpi_autoproc.log_collector import *


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
        conn.close()
        return engine
    except exc.SQLAlchemyError as err:
        get_log(err)
        exit()


def mpi_get_insurance_status_changes(dbeg: str, dend: str):
    engine = get_engine()
    session = Session(bind=engine)
    stored_proc = session.execute(text(
        "exec mpi_getInsuranceStatusChanges :dbeg :dend"
    ), {"dbeg": dbeg, "dend": dend})
    get_log(f"Процедура mpi_getInsuranceStatusChanges с параметрами {dbeg}, {dend} выполнена")


def main():
    date_begin = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
    date_end = datetime.now().strftime("%Y%m%d")
    mpi_get_insurance_status_changes(date_begin, date_end)
    input("Обработка завершена...")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        get_log(traceback.format_exc())