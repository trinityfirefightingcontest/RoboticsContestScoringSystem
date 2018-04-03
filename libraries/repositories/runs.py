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
                id INT AUTO_INCREMENT,
                level INT,
                failed_trial BOOLEAN,
                actual_time FLOAT(10,2),
                non_air BOOLEAN,
                furniture BOOLEAN,
                arbitrary_start BOOLEAN,
                return_trip BOOLEAN,
                candle_location_mode BOOLEAN,
                stopped_within_circle BOOLEAN,
                signaled_detection BOOLEAN,
                num_rooms_searched INT,
                kicked_dog BOOLEAN,
                touched_candle INT,
                cont_wall_contact INT,
                ramp_hallway BOOLEAN,
                alt_target BOOLEAN,
                all_candles BOOLEAN,
                used_versa_valve BOOLEAN,
                score FLOAT(10,2),
                robot_id VARCHAR(10),
                l3_traversed_hallway BOOLEAN,
                l3_found_baby BOOLEAN,
                l3_rescued_baby BOOLEAN,
                l3_all_candles BOOLEAN,
                l3_one_candle BOOLEAN,
                l3_none BOOLEAN,
                PRIMARY KEY (id))
                ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;""")
        r.get_registry()['MY_SQL'].query(query)

    @staticmethod
    def get_runs(robot_id):
        query = """ SELECT * FROM runs where robot_id = %(robot_id)s;"""
        data = {
            'robot_id': robot_id       
        }
        return r.get_registry()['MY_SQL'].get_all(query, data)

    @staticmethod
    def record_run(
        level,
        failed_trial,
        actual_time,
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
        used_versa_valve,
        score,
        robot_id,
        l3_traversed_hallway,
        l3_found_baby,
        l3_rescued_baby,
        l3_all_candles,
        l3_one_candle,
        l3_none
    ):

        query = """INSERT INTO runs(
            level,
            failed_trial,
            actual_time,
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
            used_versa_valve,
            score,
            robot_id,
            l3_traversed_hallway,
            l3_found_baby,
            l3_rescued_baby,
            l3_all_candles,
            l3_one_candle,
            l3_none
        ) VALUES (
            %(level)s,
            %(failed_trial)s,
            %(actual_time)s,
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
            %(used_versa_valve)s,
            %(score)s,
            %(robot_id)s,
            %(l3_traversed_hallway)s,
            %(l3_found_baby)s,
            %(l3_rescued_baby)s,
            %(l3_all_candles)s,
            %(l3_one_candle)s,
            %(l3_none)s
        );"""
        data = {
            'level': level,
            'failed_trial': failed_trial,
            'actual_time': actual_time,
            'non_air': non_air,
            'furniture': furniture,
            'arbitrary_start': arbitrary_start,
            'return_trip': return_trip,
            'candle_location_mode': candle_location_mode,
            'stopped_within_circle': stopped_within_circle,
            'signaled_detection': signaled_detection,
            'num_rooms_searched': num_rooms_searched,
            'kicked_dog': kicked_dog,
            'touched_candle': touched_candle,
            'cont_wall_contact': cont_wall_contact,
            'ramp_hallway': ramp_hallway,
            'alt_target': alt_target,
            'all_candles': all_candles,
            'used_versa_valve': used_versa_valve,
            'score': score,
            'robot_id': robot_id,
            'l3_traversed_hallway': l3_traversed_hallway,
            'l3_found_baby': l3_found_baby,
            'l3_rescued_baby': l3_rescued_baby,
            'l3_all_candles': l3_all_candles,
            'l3_one_candle': l3_one_candle,
            'l3_none': l3_none
        }
        return r.get_registry()['MY_SQL'].insert(query, data)

    @staticmethod
    def get_runs_robot_level(robot_id, level):
        query = """SELECT * FROM runs where (robot_id = %(robot_id)s) AND (level = level);"""
        data = {
            'robot_id': robot_id,
            'level': level
        }
        return r.get_registry()['MY_SQL'].get_all(query, data)
