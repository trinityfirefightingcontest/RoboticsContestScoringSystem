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
                level INT,
                failed_trial BOOLEAN,
                actual_time INT,
                reached_time_limit BOOLEAN,
                non_air BOOLEAN,
                furniture BOOLEAN,
                arbitrary_start BOOLEAN,
                return_trip BOOLEAN,
                candle_location_mode BOOLEAN,
                stopped_within_circle BOOLEAN,
                signaled_detection BOOLEAN,
                num_rooms_searched INT,
                kicked_dog BOOLEAN,
                touched_candle BOOLEAN,
                cont_wall_contact INT,
                ramp_hallway BOOLEAN,
                alt_target BOOLEAN,
                all_candles BOOLEAN,
                used_versa_valve BOOLEAN,
                FOREIGN KEY (id) REFERENCES robots(id))
            ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;"""
        )
        r.get_registry()['MY_SQL'].query(query)

    @staticmethod
    def get_runs(robot_id):
        query = """ SELECT * FROM runs where id = %(robot_id)s;"""
        data = {
            'robot_id': robot_id       
        }
        return r.get_registry()['MY_SQL'].get(query, data)

    @staticmethod
    def record_run(id,
                level,
                failed_trial,
                actual_time,
                reached_time_limit,
                non_air,
                furniture,
                arbitrary_start,
                return_trip,
                candle_location_mode,
                stopped_within_circle,
                signaled_detection,
                num_rooms_searched,
                kicked_dog,
                touched_candle,
                cont_wall_contact,
                ramp_hallway,
                alt_target,
                all_candles,
                used_versa_valve):
        query = """INSERT INTO runs(
            id,
            level,
            failed_trial,
            actual_time,
            reached_time_limit,
            non_air,
            furniture,
            arbitrary_start,
            return_trip,
            candle_location_mode,
            stopped_within_circle,
            signaled_detection,
            num_rooms_searched,
            kicked_dog,
            touched_candle,
            cont_wall_contact,
            ramp_hallway,
            alt_target,
            all_candles,
            used_versa_valve
        ) VALUES (
            %(id)s,
            %(level)s,
            %(failed_trial)s,
            %(actual_time)s,
            %(reached_time_limit)s,
            %(non_air)s,
            %(furniture)s,
            %(arbitrary_start)s,
            %(return_trip)s,
            %(candle_location_mode)s,
            %(stopped_within_circle)s,
            %(signaled_detection)s,
            %(num_rooms_searched)s,
            %(kicked_dog)s,
            %(touched_candle)s,
            %(cont_wall_contact)s,
            %(ramp_hallway)s,
            %(alt_target)s,
            %(all_candles)s,
            %(used_versa_valve)s
        );"""
        data = {
            'id': id,
            'level': int(level),
            'failed_trial': failed_trial,
            'actual_time': int(actual_time),
            'reached_time_limit': reached_time_limit,
            'non_air': non_air,
            'furniture': furniture,
            'arbitrary_start': arbitrary_start,
            'return_trip': return_trip,
            'candle_location_mode': candle_location_mode,
            'stopped_within_circle': stopped_within_circle,
            'signaled_detection': signaled_detection,
            'num_rooms_searched': int(num_rooms_searched),
            'kicked_dog': kicked_dog,
            'touched_candle': touched_candle,
            'cont_wall_contact': int(cont_wall_contact),
            'ramp_hallway': ramp_hallway,
            'alt_target': alt_target,
            'all_candles': all_candles,
            'used_versa_valve': used_versa_valve
        }
        r.get_registry()['MY_SQL'].insert(query, data)
