# -*- coding: utf-8 -*-
from initialize_registry import load_registry
import registry as r
import csv


def get_id(id_counter, robot_data):
    division = robot_data['division']
    index = id_counter[division]
    id_counter[division] += 1
    return division[0] + '_' + str(index)


def run():
    load_registry()
    division_map = {
        'fire fighting high school division': 'high_school',
        'fire fighting junior division': 'junior',
        'fire fighting senior division': 'senior',
        'fire fighting walking division': 'walking'
    }
    unique_map = {
        'no, it is unique': True,
        'yes, we customized a kit': False
    }
    versa_valve_map = {
        'yes, please ship one to me.': True,
        'no, not at this time.  we will contact you if we change our mind.': (
            False
        )
    }
    fields_index = {
        'email': 3,
        'division': 5,
        'name': 6,
        'unique': 7,
        'versa_valve': 8,
        'school': 10
    }
    with open('robot_list.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        i = 0
        id_counter = {
            'high_school': 1,
            'senior': 1,
            'walking': 1,
            'junior': 1
        }
        for row in spamreader:
            if i == 0:
                i += 1
                continue
            i += 1
            d = {}
            if row[fields_index['unique']].strip().lower() == (
                    'i am not sure, please contact me to discuss'):
                continue
            for field, index in fields_index.iteritems():
                if field == 'division':
                    d[field] = division_map[row[index].strip().lower()]
                elif field == 'unique':
                    d[field] = unique_map[row[index].strip().lower()]
                elif field == 'versa_valve':
                    d[field] = versa_valve_map[row[index].strip().lower()]
                else:
                    d[field] = row[index]
            d['id'] = get_id(id_counter, d)
            r.get_registry()['ROBOTS'].record_robot(
                division=d['division'],
                id=d['id'],
                volume=0,
                school=d['school'],
                name=d['name'],
                is_unique=d['unique'],
                used_versa_valve=d['versa_valve'],
                level=1,
                is_disqualified=False,
                passed_inspection=False
            )

if __name__ == "__main__":
    run()
