# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, make_response
import registry as r
import StringIO
import csv
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

@api.route('/prizes', methods=['GET', 'POST'])
def prize_winners():
    robots = r.get_registry()['ROBOTS'].get_all_robots()

    # calculate additional score parameters
    robots = ScoreBoard.add_scoreboard_params(robots)

    # gpmp_winner[place] dict
    gpmp_winners = ScoreBoard.get_gpmp_winners(robots)

    # lisp_winners[level][category][place] dict
    lisp_winners = ScoreBoard.get_lisp_winners(robots)

    # brd_winners[division][category][place] dict
    brd_winners = ScoreBoard.get_brd_winners(robots)

    divisions = ['junior', 'walking', 'high_school', 'senior']
    levels = [1,2,3]
    categories = ['unique','custom']

    # initialize csv file writer
    si = StringIO.StringIO()
    cw = csv.writer(si)

    # write GPMP winner to file
    entry = ''
    first_place = 1
    if gpmp_winners.get(first_place):
        entry += gpmp_winners.get(first_place).get('name')
    else:
        entry += 'N/A'
    cw.writerow(['Grand Performance Mastery Prize Winner (GPMP)',entry])

    cw.writerow('\n')
    cw.writerow('\n')

    # write BRD winners to file
    cw.writerow(['Best Robots in Division Prize Winners (BRD)'])
    cw.writerow(['Division', 'Unique', 'Customized'])

    for division in divisions:
        row = []
        row.append(division)
        for category in categories:
            entry = ''
            for place in [1,2,3]:
                entry += str(place) + ': '
                if brd_winners.get(division).get(category).get(place):
                    entry += brd_winners.get(division).get(category).get(place).get('name')
                else:
                    entry += 'N\A'
                entry += '      '

            row.append(entry)
        cw.writerow(row)

    cw.writerow('\n')
    cw.writerow('\n')

    # write LISP winners to file
    cw.writerow(['Lowest Individual Score Prize Winners (LISP)'])
    cw.writerow(['Level', 'Unique', 'Customized'])

    for level in levels:
        row = []
        row.append('L' + str(level))
        for category in categories:
            entry = ''
            for place in [1]:
                entry += str(place) + ': '
                if lisp_winners.get(level).get(category).get(place):
                    entry += lisp_winners.get(level).get(category).get(place).get('name')
                else:
                    entry += 'N\A'
                entry += '      '

            row.append(entry)
        cw.writerow(row)

    output = make_response(si.getvalue())
    si.close()
    output.headers['Content-Disposition'] = 'attachment; filename=prizes.csv'
    output.headers['Content-type'] = 'text/csv'
    return output
