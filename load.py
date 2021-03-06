# -*- coding: utf-8 -*-
from initialize_registry import load_registry
import registry as r
import MySQLdb
from constants import settings


def run():
    db = MySQLdb.connect(
        host=settings.mysql_host,
        port=settings.mysql_port,
        user=settings.mysql_user,
        passwd=settings.mysql_password)
    db.query('CREATE DATABASE IF NOT EXISTS scoring_system;')
    load_registry()

    r.get_registry()['MY_SQL'].query(
        'ALTER DATABASE scoring_system CHARACTER SET '
        'utf8 COLLATE utf8_general_ci;'
    )
    r.get_registry()['ROBOTS'].create_table()
    r.get_registry()['RUNS'].create_table()


if __name__ == "__main__":
    run()
