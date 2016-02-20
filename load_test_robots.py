# -*- coding: utf-8 -*-
from initialize_registry import load_registry
import registry as r


def run():
    load_registry()
    robots = [
        {
            'division': 'junior',
            'id': 'j-42',
            'volume': 345,
            'school': 'Taft',
            'name': 'astrid',
            'teammates': 3,
            'is_unique': True,
            'used_versa_valve': False,
            'level': 1,
            'is_disqualified': False,
            'passed_inspection': False
        },
        {
            'division': 'junior',
            'id': 'j-43',
            'volume': 1000,
            'school': 'NorthHampton',
            'name': 'robowaiter',
            'teammates': 4,
            'is_unique': False,
            'used_versa_valve': False,
            'level': 1,
            'is_disqualified': False,
            'passed_inspection': False
        },
        {
            'division': 'junior',
            'id': 'j-44',
            'volume': 98,
            'school': 'Riverside',
            'name': 'walter',
            'teammates': 4,
            'is_unique': True,
            'used_versa_valve': False,
            'level': 1,
            'is_disqualified': False,
            'passed_inspection': False
        },
        {
            'division': 'junior',
            'id': 'j-45',
            'volume': 231,
            'school': 'Springfield',
            'name': 'APS-23',
            'teammates': 1,
            'is_unique': True,
            'used_versa_valve': False,
            'level': 1,
            'is_disqualified': False,
            'passed_inspection': False
        },
        {
            'division': 'walking',
            'id': 'w-42',
            'volume': 340,
            'school': 'Waterbury',
            'name': 'W24',
            'teammates': 2,
            'is_unique': False,
            'used_versa_valve': False,
            'level': 1,
            'is_disqualified': False,
            'passed_inspection': False
        },
        {
            'division': 'junior',
            'id': 'j-47',
            'volume': 230,
            'school': 'Revere',
            'name': 'April',
            'teammates': 5,
            'is_unique': True,
            'used_versa_valve': False,
            'level': 1,
            'is_disqualified': False,
            'passed_inspection': False
        },
        {
            'division': 'senior',
            'id': 's-42',
            'volume': 220,
            'school': 'Quincy',
            'name': 'iRobot',
            'teammates': 1,
            'is_unique': True,
            'used_versa_valve': False,
            'level': 1,
            'is_disqualified': False,
            'passed_inspection': False
        },
        {
            'division': 'high_school',
            'id': 'h-42',
            'volume': 423,
            'school': 'Taft School',
            'name': 'SomeName',
            'teammates': 3,
            'is_unique': False,
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
            teammates=data['teammates'],
            is_unique=data['is_unique'],
            used_versa_valve=data['used_versa_valve'],
            level=data['level'],
            is_disqualified=data['is_disqualified'],
            passed_inspection=data['passed_inspection']
        )

if __name__ == "__main__":
    run()
