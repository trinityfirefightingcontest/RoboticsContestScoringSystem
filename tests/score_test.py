import sys
sys.path.append('..') # until I can find a better method

from initialize_registry import load_registry
import registry as r

from libraries.repositories.runs import Runs
import unittest

class TestScoringMethods(unittest.TestCase):
    
    def 

def run():
	load_registry()
	robots = [
				{
					'division': 'junior',
					'id': 'test-1',
					'volume': 365,
					'school': 'Test',
					'name': 'Jazz',
					'is_unique': True,
					'used_versa_valve': False,
					'level': 1,
					'is_disqualified': False,
					'passed_inspection': False
				},
				{
					'division': 'high_school',
					'id': 'test-2',
					'volume': 345,
					'school': 'Test',
					'name': 'Hanley',
					'is_unique': True,
					'used_versa_valve': False,
					'level': 1,
					'is_disqualified': False,
					'passed_inspection': False
				},
				{
					'division': 'senior',
					'id': 'test-3',
					'volume': 345,
					'school': 'Test',
					'name': 'Spazz',
					'is_unique': True,
					'used_versa_valve': False,
					'level': 1,
					'is_disqualified': False,
					'passed_inspection': False
				}
			]

	for data in robots:
		r.get_registry()['ROBOTS'].record_robot(
			division= data['division'],
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

	#Values of param for record_run is robot_div, level,
	# failed_trial, actual_time, reached_time_limit, 
	# non_air, furniture, arbitrary_start, return_trip,
	# candle_location_mode, stopped_within_circle,
	# signled_detection, num_rooms_detected, kicked_dog,
	# touched_candle, cont_wall_contact, ramp_hallway,
	# alt_target, all_candles, used_versa_valve, score, robot_id

	#Just using dictionary for clarification
	jazz_runs = [
		{
			'level': 1,
			'failed_trial': False,
			'actual_time': 155.742,
			'reached_time_limit': False,
			'non_air': False,
			'furniture': False,
			'arbitrary_start': False,
			'return_trip': False,
			'candle_location_mode': False,
			'stopped_within_circle': False,
			'signaled_detection': False,
			'num_rooms_detected': 2,
			'kicked_dog': False,
			'touched_candle': False,
			'cont_wall_contact': 0,
			'ramp_hallway': False,
			'alt_target': False,
			'all_candles': False,
			'used_versa_valve': False
		},
		{
			'level': 1,
			'failed_trial': False,
			'actual_time': 132.614,
			'reached_time_limit': False,
			'non_air': False,
			'furniture': False,
			'arbitrary_start': False,
			'return_trip': False,
			'candle_location_mode': True,
			'stopped_within_circle': False,
			'signaled_detection': False,
			'num_rooms_detected': 4,
			'kicked_dog': True,
			'touched_candle': False,
			'cont_wall_contact': 16,
			'ramp_hallway': False,
			'alt_target': False,
			'all_candles': False,
			'used_versa_valve': False
		},
		{
			'level': 1,
			'failed_trial': True,
			'actual_time': 340,  #Some random number over 3
			'reached_time_limit': True,
			'non_air': False,
			'furniture': False,
			'arbitrary_start': False,
			'return_trip': False,
			'candle_location_mode': False,
			'stopped_within_circle': False,
			'signaled_detection': False,
			'num_rooms_detected': 1,
			'kicked_dog': False,
			'touched_candle': False,
			'cont_wall_contact': 0,
			'ramp_hallway': False,
			'alt_target': False,
			'all_candles': False,
			'used_versa_valve': False
		},
		{
			'level': 2,
			'failed_trial': False,
			'actual_time': 150.304,
			'reached_time_limit': False,
			'non_air': False,
			'furniture': True,
			'arbitrary_start': False,
			'return_trip': False,
			'candle_location_mode': False,
			'stopped_within_circle': False,
			'signaled_detection': False,
			'num_rooms_detected': 4,
			'kicked_dog': False,
			'touched_candle': False,
			'cont_wall_contact': 3,
			'ramp_hallway': False,
			'alt_target': False,
			'all_candles': False,
			'used_versa_valve': False	
		},
		{
			'level': 3,
			'failed_trial': True,
			'actual_time': 190,
			'reached_time_limit': True,
			'non_air': False,
			'furniture': True,
			'arbitrary_start': False,
			'return_trip': False,
			'candle_location_mode': False,
			'stopped_within_circle': False,
			'signaled_detection': False,
			'num_rooms_detected': 2,
			'kicked_dog': False,
			'touched_candle': False,
			'cont_wall_contact': 3,
			'ramp_hallway': False,
			'alt_target': False,
			'all_candles': False,
			'used_versa_valve': False	
		}
	]

	hanley_runs = [
		{
			'level': 1,
			'failed_trial': False,
			'actual_time': 285.742,
			'reached_time_limit': False,
			'non_air': False,
			'furniture': False,
			'arbitrary_start': False,
			'return_trip': False,
			'candle_location_mode': False,
			'stopped_within_circle': False,
			'signaled_detection': False,
			'num_rooms_detected': 2,
			'kicked_dog': False,
			'touched_candle': False,
			'cont_wall_contact': 0,
			'ramp_hallway': False,
			'alt_target': False,
			'all_candles': False,
			'used_versa_valve': False	
		},
		{
			'level': 1,
			'failed_trial': False,
			'actual_time': 39.234,
			'reached_time_limit': False,
			'non_air': False,
			'furniture': False,
			'arbitrary_start': False,
			'return_trip': False,
			'candle_location_mode': True,
			'stopped_within_circle': False,
			'signaled_detection': False,
			'num_rooms_detected': 3,
			'kicked_dog': False,
			'touched_candle': False,
			'cont_wall_contact': 8,
			'ramp_hallway': False,
			'alt_target': False,
			'all_candles': False,
			'used_versa_valve': False	
		},
		{
			'level': 2,
			'failed_trial': False,
			'actual_time': 150.304,
			'reached_time_limit': False,
			'non_air': False,
			'furniture': True,
			'arbitrary_start': False,
			'return_trip': False,
			'candle_location_mode': False,
			'stopped_within_circle': False,
			'signaled_detection': False,
			'num_rooms_detected': 4,
			'kicked_dog': False,
			'touched_candle': False,
			'cont_wall_contact': 3,
			'ramp_hallway': False,
			'alt_target': False,
			'all_candles': False,
			'used_versa_valve': False	
		},
		{
			'level': 3,
			'failed_trial': True,
			'actual_time': 450,
			'reached_time_limit': False,
			'non_air': False,
			'furniture': False,
			'arbitrary_start': False,
			'return_trip': False,
			'candle_location_mode': False,
			'stopped_within_circle': False,
			'signaled_detection': False,
			'num_rooms_detected': 0,
			'kicked_dog': False,
			'touched_candle': False,
			'cont_wall_contact': 0,
			'ramp_hallway': False,
			'alt_target': False,
			'all_candles': False,
			'used_versa_valve': False	
		},
		{
			'level': 3,
			'failed_trial': False,
			'actual_time': 58.222,
			'reached_time_limit': False,
			'non_air': False,
			'furniture': False,
			'arbitrary_start': False,
			'return_trip': False,
			'candle_location_mode': False,
			'stopped_within_circle': False,
			'signaled_detection': False,
			'num_rooms_detected': 2,
			'kicked_dog': False,
			'touched_candle': False,
			'cont_wall_contact': 0,
			'ramp_hallway': False,
			'alt_target': False,
			'all_candles': True,
			'used_versa_valve': False	
		}
	]

	spazz_runs = [
		{
			'level': 1,
			'failed_trial': True,
			'actual_time': 285.742,
			'reached_time_limit': False,
			'non_air': False,
			'furniture': False,
			'arbitrary_start': False,
			'return_trip': False,
			'candle_location_mode': False,
			'stopped_within_circle': False,
			'signaled_detection': False,
			'num_rooms_detected': 2,
			'kicked_dog': False,
			'touched_candle': False,
			'cont_wall_contact': 3,
			'ramp_hallway': False,
			'alt_target': False,
			'all_candles': False,
			'used_versa_valve': False	
		},
		{
			'level': 1,
			'failed_trial': False,
			'actual_time': 85.641,
			'reached_time_limit': False,
			'non_air': False,
			'furniture': False,
			'arbitrary_start': False,
			'return_trip': False,
			'candle_location_mode': False,
			'stopped_within_circle': False,
			'signaled_detection': False,
			'num_rooms_detected': 2,
			'kicked_dog': False,
			'touched_candle': False,
			'cont_wall_contact': 0,
			'ramp_hallway': False,
			'alt_target': False,
			'all_candles': False,
			'used_versa_valve': False	
		},
		{
			'level': 1,
			'failed_trial': True,
			'actual_time': 285.742,
			'reached_time_limit': False,
			'non_air': False,
			'furniture': False,
			'arbitrary_start': False,
			'return_trip': False,
			'candle_location_mode': False,
			'stopped_within_circle': False,
			'signaled_detection': False,
			'num_rooms_detected': 2,
			'kicked_dog': False,
			'touched_candle': False,
			'cont_wall_contact': 0,
			'ramp_hallway': False,
			'alt_target': False,
			'all_candles': False,
			'used_versa_valve': False	
		},
		{
			'level': 2,
			'failed_trial': False,
			'actual_time': 187.638,
			'reached_time_limit': False,
			'non_air': True,
			'furniture': True,
			'arbitrary_start': True,
			'return_trip': True,
			'candle_location_mode': False,
			'stopped_within_circle': False,
			'signaled_detection': False,
			'num_rooms_detected': 4,
			'kicked_dog': True,
			'touched_candle': True,
			'cont_wall_contact': 0,
			'ramp_hallway': False,
			'alt_target': False,
			'all_candles': False,
			'used_versa_valve': False	
		},
		{
			'level': 3,
			'failed_trial': False,
			'actual_time': 117,
			'reached_time_limit': False,
			'non_air': False,
			'furniture': True,
			'arbitrary_start': False,
			'return_trip': False,
			'candle_location_mode': False,
			'stopped_within_circle': False,
			'signaled_detection': False,
			'num_rooms_detected': 2,
			'kicked_dog': False,
			'touched_candle': False,
			'cont_wall_contact': 0,
			'ramp_hallway': True,
			'alt_target': True,
			'all_candles': True,
			'used_versa_valve': False	
		}
	]

	for run in jazz_runs:
		jazz_robot = robots[0]
		robot_div = jazz_robot['division']
		robot_id = jazz_robot['id']

		score_components = (robot_div,
							run['level'],
							run['failed_trial'],
							run['actual_time'],
							run['non_air'],
							run['furniture'],
							run['arbitrary_start'],
							run['return_trip'],
							run['candle_location_mode'],
							run['stopped_within_circle'],
							run['signaled_detection'],
							run['num_rooms_detected'],
							run['kicked_dog'],
							run['touched_candle'],
							run['cont_wall_contact'],
							run['ramp_hallway'],
							run['alt_target'],
							run['all_candles'])

		r.get_registry()['RUNS'].record_run(run['level'],
											run['failed_trial'],
											run['actual_time'],
											run['non_air'],
											run['furniture'],
											run['arbitrary_start'],
											run['return_trip'],
											run['candle_location_mode'],
											run['stopped_within_circle'],
											run['signaled_detection'],
											run['num_rooms_detected'],
											run['kicked_dog'],
											run['touched_candle'],
											run['cont_wall_contact'],
											run['ramp_hallway'],
											run['alt_target'],
											run['all_candles'],
											run['used_versa_valve'],
											Runs.calculate_run_score(*score_components),
											robot_id)

	for run in hanley_runs:
		hanley_robot = robots[1]
		robot_div = hanley_robot['division']
		robot_id = hanley_robot['id']

		score_components = (robot_div,
							run['level'],
							run['failed_trial'],
							run['actual_time'],
							run['non_air'],
							run['furniture'],
							run['arbitrary_start'],
							run['return_trip'],
							run['candle_location_mode'],
							run['stopped_within_circle'],
							run['signaled_detection'],
							run['num_rooms_detected'],
							run['kicked_dog'],
							run['touched_candle'],
							run['cont_wall_contact'],
							run['ramp_hallway'],
							run['alt_target'],
							run['all_candles'])

		print "score components:"
		print(score_components)
		
		r.get_registry()['RUNS'].record_run(run['level'],
											run['failed_trial'],
											run['actual_time'],
											run['non_air'],
											run['furniture'],
											run['arbitrary_start'],
											run['return_trip'],
											run['candle_location_mode'],
											run['stopped_within_circle'],
											run['signaled_detection'],
											run['num_rooms_detected'],
											run['kicked_dog'],
											run['touched_candle'],
											run['cont_wall_contact'],
											run['ramp_hallway'],
											run['alt_target'],
											run['all_candles'],
											run['used_versa_valve'],
											Runs.calculate_run_score(*score_components),
											robot_id)
	
	for run in spazz_runs:
		spazz_robot = robots[2]
		robot_div = spazz_robot['division']
		robot_id = spazz_robot['id']

		score_components = (robot_div,
							run['level'],
							run['failed_trial'],
							run['actual_time'],
							run['non_air'],
							run['furniture'],
							run['arbitrary_start'],
							run['return_trip'],
							run['candle_location_mode'],
							run['stopped_within_circle'],
							run['signaled_detection'],
							run['num_rooms_detected'],
							run['kicked_dog'],
							run['touched_candle'],
							run['cont_wall_contact'],
							run['ramp_hallway'],
							run['alt_target'],
							run['all_candles'])
		
		r.get_registry()['RUNS'].record_run(run['level'],
											run['failed_trial'],
											run['actual_time'],
											run['non_air'],
											run['furniture'],
											run['arbitrary_start'],
											run['return_trip'],
											run['candle_location_mode'],
											run['stopped_within_circle'],
											run['signaled_detection'],
											run['num_rooms_detected'],
											run['kicked_dog'],
											run['touched_candle'],
											run['cont_wall_contact'],
											run['ramp_hallway'],
											run['alt_target'],
											run['all_candles'],
											run['used_versa_valve'],
											Runs.calculate_run_score(*score_components),
											robot_id)



if __name__ == "__main__":
	unittest.main()
