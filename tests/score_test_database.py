import sys
sys.path.append('..')  # until I can find a better method

from initialize_registry import load_registry
import registry as r
import json

from libraries.repositories.runs import Runs


def run():
    load_registry()
    test_data = json.load('score_test.json')

    for data in test_data['robots']:
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
        robit_id = robot['id']

        robot_runs = test_data["{0}_runs".format(robot_name)]

        for run in robot_runs:
            
            run_data = run.values()
            score_components = (robot_div, run_data)

            r.get_registry()['RUNS'].record_run(run_data,
                                                Runs.calculate_run_score(
                                                    *score_components),
                                                robot_id)


if __name__ == "__main__":
    run()
