# -*- coding: utf-8; -*-

import registry as r


class Robots(object):
    @staticmethod
    def create_table():
        result = r.get_registry()['MY_SQL'].query(
            (
                "select * from information_schema.tables where "
                "TABLE_SCHEMA='scoring_system' and table_name='robots';"
            )
        )
        if result != 0:
            return
        query = (
            """CREATE TABLE IF NOT EXISTS robots(
            id INT AUTO_INCREMENT,
            name VARCHAR(50),
            division VARCHAR(24),
            PRIMARY KEY (id))
             ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;"""
        )
        r.get_registry()['MY_SQL'].query(query)
        r.get_registry()['MY_SQL'].query(
            ('ALTER TABLE robots ADD INDEX (name), ADD '
             'UNIQUE INDEX (name)')
        )

    @staticmethod
    def record_robot(name, division):
        query = """INSERT INTO robots(
            name, division
        ) VALUES (
            %(name)s,
            %(division)s
        );"""
        data = {
            'name': name,
            'division': division
        }
        r.get_registry()['MY_SQL'].insert(query, data)
