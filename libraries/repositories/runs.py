# -*- coding: utf-8; -*-

import registry as r


class Runs(object):
    @staticmethod
    def create_table():
        result = r.get_registry()['MY_SQL'].query(
            (
                "select * from information_schema.tables where "
                "TABLE_SCHEMA='scoring_system' and table_name='runs';"
            )
        )
        if result != 0:
            return
        query = (
            """CREATE TABLE IF NOT EXISTS runs(
            id VARCHAR(50),
            division VARCHAR(10),
            diqualified BOOLEAN,
            PRIMARY KEY (id))
             ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;"""
        )
        r.get_registry()['MY_SQL'].query(query)
