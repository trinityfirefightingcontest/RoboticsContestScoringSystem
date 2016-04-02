# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
import registry as r
from libraries.utilities.scoreboard import ScoreBoard

api = Blueprint('api', __name__)


@api.route('/scoreboard/gpmp', methods=['GET', 'POST'])
def scoreboard_gpmp():
    robots = r.get_registry()['ROBOTS'].get_all_robots()

    # add additional parameters to be displayed on scoreboard
    robots = ScoreBoard.add_scoreboard_params(robots)

    # sort based on name then total score
    sorted_robots = sorted(list(robots), key=lambda k: k['name'])
    sorted_robots = sorted(list(sorted_robots), key=lambda k: k['TFS'])
    for robot in sorted_robots:
        robot['completed'] = list(robot['completed'])
    return jsonify({
        'robots': sorted_robots
    })
