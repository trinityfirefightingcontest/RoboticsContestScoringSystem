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
                actual_time INT,
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
                score FLOAT(10,2),
                robot_id VARCHAR(10),
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
    def record_run(level,
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
                robot_id):

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
            robot_id
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
            %(robot_id)s
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
            'robot_id': robot_id 
        }
        r.get_registry()['MY_SQL'].insert(query, data)

    @staticmethod
    def get_runs_robot_level(robot_id, level):
        query = """SELECT * FROM runs where (robot_id = %(robot_id)s) AND (level = level);"""
        data = {
            'robot_id': robot_id,
            'level': level
        }
        return r.get_registry()['MY_SQL'].get_all(query, data)

    @staticmethod
    def calculate_run_score(robot_div,
                        level,
                        failed_trial,
                        actual_time,
                        non_air ,
                        furniture,
                        arbitrary_start,
                        return_trip,
                        candle_location_mode,
                        stopped_within_circle,
                        signaled_detection,
                        num_rooms_detected,
                        kicked_dog,
                        touched_candle,
                        cont_wall_contact,
                        ramp_hallway,
                        alt_target,
                        all_candles,
                        used_versa_valve):

        task_search = num_rooms_detected * (-30)
        task_detect = -30 if signaled_detection else 0
        task_position = -30 if stopped_within_circle else 0

        om_candle = 0.75 if candle_location_mode else 1

        om_start = 0.8 if arbitrary_start else 1
        om_return = 0.8 if return_trip else 1
        om_extinguisher = 0.75 if non_air else 1
        om_furniture = 0.75 if furniture else 1

        if num_rooms_detected == 0 or num_rooms_detected == 1:
            room_factor = 1
        elif num_rooms_detected == 2:
            room_factor = 0.85
        elif num_rooms_detected == 3:
            room_factor = 0.5
        elif num_rooms_detected == 4:
            room_factor = 0.35

        pp_candle = 50 if touched_candle else 0
        pp_slide = cont_wall_contact / 2
        pp_dog = 50 if kicked_dog else 0

        om_alt_target = 0.6 if alt_target else 1
        om_ramp_hallway = 0.9 if ramp_hallway else 1
        om_all_candles = 0.6 if all_candles else 1

        #Scores
        if failed_trial:
            if robot_div in ['junior', 'walking'] and level == 1:
                return 600 + task_detect + task_position + task_search;
            else:
                return 600
        
        if level == 1:
            return ((actual_time + pp_candle + pp_dog + pp_slide) *
                    (om_candle * om_start * om_return * om_extinguisher * om_furniture) * room_factor)
        
        if level == 2:
            return ((actual_time + pp_candle + pp_dog + pp_slide) * 
                    (om_start * om_return * om_extinguisher * om_furniture) * room_factor)

        if level == 3:
            return ((actual_time + pp_candle + pp_dog + pp_slide) * 
                    om_alt_target * om_ramp_hallway * om_all_candles) 
            
