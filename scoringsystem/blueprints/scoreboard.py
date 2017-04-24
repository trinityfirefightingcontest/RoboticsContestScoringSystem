# -*- coding: utf-8 -*-

import requests
from flask import (
    Blueprint, current_app, session, request,
    redirect, url_for, flash, render_template,
    make_response
)
import StringIO
import csv
import registry as r
from constants import settings
from libraries.utilities.scoreboard import ScoreBoard
from libraries.utilities.score_calculator import ScoreCalculator


scoreboard = Blueprint('scoreboard', __name__)


@scoreboard.route('/scoreboard', methods=['GET', 'POST'])
def scoreboard_home():
    return render_template("scoreboard_home.html")


@scoreboard.route('/scoreboard/brd/<division>', methods=['GET', 'POST'])
def scoreboard_brd(division):
    robots = r.get_registry()['ROBOTS'].get_all_robots_division(
        division
    )

    if not robots:
        return render_template("not_found.html")

    # add additional parameters to be displayed on scoreboard
    robots = ScoreBoard.add_scoreboard_params(robots)

    # sort based on name then total score
    sorted_robots = sorted(
        list(robots),
        key=lambda k: k['name']
    )
    sorted_robots = sorted(
        list(sorted_robots),
        key=lambda k: k['TFS']
    )

    return render_template(
        "scoreboard_brd_gpmp.html",
        robots=sorted_robots,
        scoreboard_name=get_division_label(division)
    )


@scoreboard.route('/scoreboard/gpmp', methods=['GET', 'POST'])
def scoreboard_gpmp():
    robots = r.get_registry()['ROBOTS'].get_all_robots()

    if not robots:
        return render_template("not_found.html")

    # add additional parameters to be displayed on scoreboard
    robots = ScoreBoard.add_scoreboard_params(robots)

    # sort based on name then total score
    sorted_robots = sorted(
        list(robots),
        key=lambda k: k['name']
    )
    sorted_robots = sorted(
        list(sorted_robots),
        key=lambda k: k['TFS']
    )

    return render_template(
        "scoreboard_brd_gpmp.html",
        robots=sorted_robots,
        scoreboard_name="Grand Performance"
    )


@scoreboard.route('/scoreboard/lisp/<level>', methods=['GET', 'POST'])
def scoreboard_lisp(level):
    if not level.isdigit():
        return render_template("not_found.html")
    if int(level) not in [1, 2, 3]:
        return render_template("not_found.html")

    robots = r.get_registry()['ROBOTS'].get_all_robots()

    if not robots:
        return render_template("not_found.html")

    # add additional parameters to be displayed on scoreboard
    robots = ScoreBoard.add_scoreboard_params(robots)

    # filter robots
    filtered_robots = ScoreBoard.filter_robots_level(
        robots,
        int(level)
    )

    # key used for sorting
    score_name = "LS" + level

    # sort based on name then this level's lowest score
    sorted_robots = sorted(
        list(filtered_robots),
        key=lambda k: k['name']
    )
    sorted_robots = sorted(
        list(sorted_robots),
        key=lambda k: k[score_name]
    )

    return render_template(
        "scoreboard_lisp.html",
        robots=sorted_robots,
        level=level,
        score_name=score_name
    )

@scoreboard.route('/prizes', methods=['GET', 'POST'])
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

    return render_template(
        "prizes.html",
        gpmp_winners=gpmp_winners,
        lisp_winners=lisp_winners,
        brd_winners=brd_winners
    )


@scoreboard.route('/scoreboardcsv', methods=['GET', 'POST'])
def export_to_csv():
    divisions = ['junior', 'walking', 'high_school', 'senior']

    all_robots = {}

    for division in divisions:
        all_robots[division] = r.get_registry()['ROBOTS'].get_all_robots_division(division)

    si = StringIO.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Rank', 'Division', 'Name', '# of Successful Runs',
                 'Current Level', 'LS1', 'LS2', 'LS3', 'TFS'])

    for div in all_robots:
        for robot in all_robots[div]:
            runs = r.get_registry()['RUNS'].get_runs(robot['id'])
            # get current best scores
            best_scores, attempted_levels, total_score, num_successful = (
                ScoreCalculator.get_best_scores(runs)
            )
            robot.update(best_scores)
            robot['TFS'] = total_score
            robot['num_successful'] = num_successful
            # calculate lowes scores for each level and TFS, returns tuple
            robot['completed'] = attempted_levels

        # sort based on name then total score
        sorted_robots = sorted(
            list(all_robots[div]),
            key=lambda k: k['name']
        )
        sorted_robots = sorted(
            list(sorted_robots),
            key=lambda k: k['TFS']
        )


        for index, sorted_r in enumerate(sorted_robots, start=1):
            cw.writerow([
                index,
                sorted_r['division'],
                sorted_r['name'],
                sorted_r['num_successful'],
                sorted_r['level'],
                sorted_r['LS1'],
                sorted_r['LS2'],
                sorted_r['LS3'],
                sorted_r['TFS']
            ])

        cw.writerow('\n')

    output = make_response(si.getvalue())
    si.close()
    output.headers["Content-Disposition"] = "attachment; filename=scoreboard.csv"
    output.headers["Content-type"] = "text/csv"
    return output


def get_division_label(division):
    # page header label
    if division == 'junior':
        return "Junior Division"
    elif division == 'walking':
        return "Walking Division"
    elif division == 'high_school':
        return "High School Division"
    else:
        return "Senior Division"