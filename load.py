# -*- coding: utf-8 -*-
from initialize_registry import load_registry
import registry as r


def run():
    load_registry()
    r.get_registry()['MY_SQL'].query(
        'CREATE DATABASE IF NOT EXISTS scoring_system;'
    )
    r.get_registry()['MY_SQL'].query(
        'ALTER DATABASE scoring_system CHARACTER SET '
        'utf8 COLLATE utf8_general_ci;'
    )
    r.get_registry()['ROBOTS'].create_table()
    r.get_registry()['RUNS'].create_table()


if __name__ == "__main__":
    run()
