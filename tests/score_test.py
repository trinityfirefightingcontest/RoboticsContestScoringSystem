import sys
sys.path.append('..')  # until I can find a better method

from initialize_registry import load_registry
import registry as r
import json

from libraries.utilities.runs import Runs

def run():
    load_registry()
    test_data = json.load(open('score_test.json'))

    

    for data in test_data['robots']:
        delete_query = "DELETE FROM robots WHERE id = %(id)s"
        query_data = { 'id': data['id'] }
        r.get_registry()['MY_SQL'].insert(delete_query, query_data)

        r.get_registry()['ROBOTS'].record_robot(
            division=data['division'],
            id=data['id'],
            volume=data['volume'],
            school=data['school'],
            name=data['name'],
            is_unique=data['is_unique'],
            used_versa_valve=data['used_versa_valve'],
            level=data['level'],
            is_disqualified=data['is_disqualified'],
            passed_inspection=data['passed_inspection']
        )

        # Values of param for record_run is robot_div, level,
        # failed_trial, actual_time, reached_time_limit,
        # non_air, furniture, arbitrary_start, return_trip,
        # candle_location_mode, stopped_within_circle,
        # signled_detection, num_rooms_detected, kicked_dog,
        # touched_candle, cont_wall_contact, ramp_hallway,
        # alt_target, all_candles, used_versa_valve, score, robot_id

        # Just using dictionary for clarification

    for robot in test_data['robots']:
        robot_name = robot['name']
        robot_div = robot['division']
        robot_id = robot['id']
        
        robot_runs = test_data["{0}_runs".format(robot_name.lower())]

        for run in robot_runs:

            run_param_names = ['level', 'failed_trial', 'actual_time',
                               'non_air', 'furniture', 'arbitrary_start',
                               'return_trip', 'candle_location_mode', 
                               'stopped_within_circle', 'signaled_detection',
                               'num_rooms_detected', 'kicked_dog', 'touched_candle',
                               'cont_wall_contact', 'ramp_hallway', 'alt_target',
                               'all_candles', 'used_versa_valve']

            record_params = [run[x] for x in run_param_names] 

            score_params = [run[x] for x in run_param_names[:-1]] # No versa
            score_params.insert(0, robot_div) 
            
            run_score = Runs.calculate_run_score(*score_params)
            print run_score
        
            r.get_registry()['RUNS'].record_run(*record_params,
                                                score=run_score,
                                                robot_id=robot_id)


if __name__ == "__main__":
    run()
