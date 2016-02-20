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
            division VARCHAR(16),
            id VARCHAR(10) UNIQUE,
            volume INT,
            school VARCHAR(50),
            name VARCHAR(50),
            teammates INT,
            is_unique BOOLEAN,
            used_versa_valve BOOLEAN,
            level INT,
            is_disqualified BOOLEAN,
            passed_inspection BOOLEAN,
            PRIMARY KEY (id))
            ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;"""
        )
        r.get_registry()['MY_SQL'].query(query)
        r.get_registry()['MY_SQL'].query(
            ('ALTER TABLE robots ADD INDEX (name), ADD '
             'UNIQUE INDEX (name)')
        )

    @staticmethod
    def record_robot(division,
                     id,
                     volume,
                     school,
                     name,
                     teammates,
                     is_unique,
                     used_versa_valve,
                     level,
                     is_disqualified,
                     passed_inspection):
        query = """INSERT INTO robots(
            division,
            id,
            volume,
            school,
            name,
            teammates,
            is_unique,
            used_versa_valve,
            level,
            is_disqualified,
            passed_inspection
        ) VALUES (
            %(division)s,
            %(id)s,
            %(volume)s,
            %(school)s,
            %(name)s,
            %(teammates)s,
            %(is_unique)s,
            %(used_versa_valve)s,
            %(level)s,
            %(is_disqualified)s,
            %(passed_inspection)s
        );"""
        data = {
            'division': division,
            'id': id,
            'volume': volume,
            'school': school,
            'name': name,
            'teammates': teammates,
            'is_unique': is_unique,
            'used_versa_valve': used_versa_valve,
            'level': level,
            'is_disqualified': is_disqualified,
            'passed_inspection': passed_inspection
        }
        r.get_registry()['MY_SQL'].insert(query, data)

    @staticmethod
    def get_robot(robot_id):
        query = """SELECT * FROM robots where id = %(robot_id)s;"""
        data = {
            'robot_id': robot_id
        }
        return r.get_registry()['MY_SQL'].get(query, data)

    @staticmethod
    def get_all_robots():
        query = """SELECT * FROM robots;"""
        return r.get_registry()['MY_SQL'].get_all(query)
