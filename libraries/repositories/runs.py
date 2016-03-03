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
                score FLOAT(10,2),
                robot_id VARCHAR(10))
                ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;"""
        )
        r.get_registry()['MY_SQL'].query(query)

    @staticmethod
    def get_runs(robot_id):
        query = """ SELECT * FROM runs where robot_id = %(robot_id)s;"""
        data = {
            'robot_id': robot_id       
        }
        return r.get_registry()['MY_SQL'].get_all(query, data)

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
                used_versa_valve,
                robot_id):
        #Getting robot division for scoring later in the function
        #robot_div = get_robot(robot_id).get('division') 
        robot_div_query = """ SELECT division FROM robots where id = %(robot_id)s;"""
        robot_div_data = {
            'robot_id' : robot_id
        }
        robot_div = r.get_registry()['MY_SQL'].get_all(robot_div_query, robot_div_data)

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
            used_versa_valve,
            score,
            robot_id
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
            %(used_versa_valve)s,
            %(score)s,
            %(robot_id)s
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
            'used_versa_valve': used_versa_valve,
            'score': calculate_run_score(robot_div,
                                         id, 
                                         int(level),
                                         failed_trial,
                                         int(actual_time),
                                         reached_time_limit,
                                         non_air,
                                         furniture,
                                         arbitrary_start,
                                         return_trip,
                                         candle_location_mode,
                                         stopped_within_circle,
                                         signaled_detection,
                                         int(num_rooms_searched),
                                         kicked_dog,
                                         touched_candle,
                                         int(cont_wall_contact),
                                         ramp_hallway,
                                         alt_target,
                                         all_candles),
            'robot_id': robot_id 
        }
        r.get_registry()['MY_SQL'].insert(query, data)

def calculate_run_score(robot_div,
                        level,
                        failed_trial = False,
                        actual_time = 0,
                        reached_time_limit = False,
                        non_air = False,
                        furniture = False,
                        arbitrary_start = False,
                        return_trip = False,
                        candle_location_mode = False,
                        stopped_within_circle = False,
                        signaled_detection = False,
                        num_rooms_searched = 0,
                        kicked_dog = False,
                        touched_candle = False,
                        cont_wall_contact = 0,
                        ramp_hallway = False,
                        alt_target = False,
                        all_candles = False,
                        used_versa_valve = False):

    if level == 1 and robot_div in ['junior','walking']:
        task_search = num_rooms_searched * (-30)
        task_detect = -30 if signaled_detection else 0
        task_position = -30 if stopped_within_circle else 0
    
    if level in [1,2,3]:
        if level == 1:
            om_candle = 0.75 if candle_location_mode else 1

        if level in [1,2]:
            om_start = 0.8 if arbitrary_start else 1
            om_return = 0.8 if return_trip else 1
            om_extinguisher = 0.75 if non_air else 1
            om_furniture = 0.75 if furniture else 1

            if num_rooms_searched == 1:
                room_factor = 1
            elif num_rooms_searched == 2:
                room_factor = 0.85
            elif num_rooms_searched == 3:
                room_factor = 0.5
            elif num_rooms_searched == 4:
                room_factor = 0.35

        pp_candle = 50 if not touched_candle else 0
        pp_slide = cont_wall_contact / 2
        pp_dog = 50 if not kicked_dog else 0

        if level == 3:
            om_alt_target = 0.6 if alt_target else 1
            om_ramp_hallway = 0.9 if ramp_hallway else 1
            om_all_candles = 0.6 if all_candles else 1

    #Scores
    if failed_trial:
        if robot_div in ['junior', 'walking']:
            return 600 + task_detect + task_position + task_search;
        else:
            return 600

    elif level == 1 and robot_div in ['junior','walking']:
        return ((actual_time + task_detect + task_position + task_search) *
                (om_candle * om_start * om_return * om_extinguisher * om_furniture))
    
    elif level == 1 and robot_div in ['high_school','senior']:
        return ((actual_time + task_search) * (om_start * om_return * om_extinguisher * om_furniture))

    elif level == 2 and robot_div in ['junior', 'walking']:
        return ((actual_time) * (om_start * om_return * om_extinguisher * om_furniture) * room_factor)

    elif level == 2 and robot_div in ['high_school', 'senior']:
        return ((actual_time) * (om_start * om_return * om_extinguisher * om_furniture))

    #?? 
    elif level == 3 and robot_div == 'junior':
        return actual_time

    elif level == 3 and robot_div in ['walking', 'high_school', 'senior']:
        return actual_time * (om_alt_target * om_ramp_hallway * om_all_candles) 
            
