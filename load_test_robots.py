# -*- coding: utf-8 -*-
from initialize_registry import load_registry
import registry as r


def run():
    load_registry()
    robots = [
        ('junior', 'a'),
        ('high_school', 'b'),
        ('senior', 'c'),
        ('walking', 'd'),
        ('junior', 'e'),
        ('high_school', 'f'),
        ('senior', 'g'),
        ('walking', 'h'),
        ('junior', 'i'),
        ('high_school', 'j'),
        ('senior', 'k'),
        ('walking', 'l'),
        ('junior', 'm'),
        ('high_school', 'n'),
        ('junior', 'o'),
        ('high_school', 'p'),
    ]
    for division, name in robots:
        r.get_registry()['ROBOTS'].record_robot(
            name=name, division=division
        )

if __name__ == "__main__":
    run()
