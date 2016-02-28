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
        return r.get_registry()['MY_SQL'].get_all(query, data)

    @staticmethod
    def record_run(id,
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
                used_versa_valve):
        query = """INSERT INTO runs(
            id,
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
            used_versa_valve
        ) VALUES (
            %(id)s,
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
            %(used_versa_valve)s
        );"""
        data = {
            'id': id,
            'level': int(level),
            'failed_trial': failed_trial,
            'actual_time': int(actual_time),
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

    @staticmethod
    def calculate_run_score(run_id, robot_id):
        query = ("""SELECT * FROM runs where id = %(run_id)s;""")
        data = {
            'run_id': run_id
        } 
        run_data = r.get_registry()['MY_SQL'].get(query, data)
       
        query = ("""SELECT division FROM robots where id = %(robot_id)s;""")
        data = {
            'robot_id': robot_id
        }
        robot_div = r.get_registry()['MY_SQL'].get(query, data)
        
        actual_time = run_data['actual_time']
        run_level = run_data['level'];
        
        if run_level == 1 and robot_div in ['junior','walking']:
            task_search = run_data.get('num_rooms_searched', 0) * (-30)
            task_detect = -30 if run_data.get('signaled_detection', false) else 0
            task_position = -30 if run_data.get('stopped_within_circle', false) else 0
        
        if run_level in [1,2,3]:
            if run_level == 1:
                om_candle = 0.75 if run_data.get('candle_location_mode', false) else 1

            if run_level in [1,2]:
                om_start = 0.8 if run_data.get('arbitrary_start', false) else 1
                om_return = 0.8 if run_data.get('return_trip', false) else 1
                om_extinguisher = 0.75 if run_data.get('non_air', false) else 1
                om_furniture = 0.75 if run_data.get('furniture', false) else 1

                if run_data.get('num_rooms_searched') == 1:
                    room_factor = 1
                elif run_data.get('num_rooms_searched') == 2:
                    room_factor = 0.85
                elif run_data.get('num_rooms_searched') == 3:
                    room_factor = 0.5
                elif run_data.get('num_rooms_searched') == 4:
                    room_factor = 0.35

            pp_candle = 50 if run_data.get('touched_candle', false) else 0
            pp_slide = run_data.get('cont_wall_contact', 0) / 2
            pp_dog = 50 if run_data.get('kicked_dog', false) else 0

            if run_level == 3:
                om_alt_target = 0.6 if run_data.get('alt_target', false) else 1
                om_ramp_hallway = 0.9 if run_data.get('ramp_hallway', false) else 1
                om_all_candles = 0.6 if run_data.get('all_candles', false) else 1

        #Scores
        if run_data['disqualified']:
            if robot_div in ['junior', 'walking']:
                return 600 + task_detect + task_position + task_search;
            else:
                return 600

        elif run_level == 1 and robot_div in ['junior','walking']:
            return ((actual_time + task_detect + task_position + task_search) *
                    (om_candle * om_start * om_return * om_extinguisher * om_furniture))
        
        elif run_level == 1 and robot_div in ['high_school','senior']:
            return ((actual_time + task_search) * (om_start * om_return * om_extinguisher * om_furniture))

        elif run_level == 2 and robot_div in ['junior', 'walking']:
            return ((actual_time) * (om_start * om_return * om_extinguisher * om_furniture) * room_factor)

        elif run_level == 2 and robot_div in ['high_school', 'senior']:
            return ((actual_time) * (om_start * om_return * om_extinguisher * om_furniture))

        #?? 
        elif run_level == 3 and robot_div == 'junior':
            return actual_time

        elif run_level == 3 and robot_div in ['walking', 'high_school', 'senior']:
            return actual_time * (om_alt_target * om_ramp_hallway * om_all_candles)


            
