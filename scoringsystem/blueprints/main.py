# -*- coding: utf-8 -*-
from flask import (
    Blueprint, render_template, url_for, request,
    redirect, session, make_response)
import registry as r
import StringIO
import csv
from libraries.utilities.authentication import AuthenticationUtilities
from libraries.utilities.level_progress_handler import LevelProgressHandler
from libraries.utilities.score_calculator import ScoreCalculator
from libraries.utilities.scoreboard import ScoreBoard
from libraries.utilities.runs import Runs
from libraries.utilities.robot_inspection_table_handler import (
    RobotInspectionTableHandler
)
main = Blueprint('main', __name__)


@main.before_request
def require_login():
    if not AuthenticationUtilities.user_is_logged_in(session):
        return redirect(url_for('auth.signin'))


@main.route('/', methods=['GET', 'POST'])
def home():
    robots = r.get_registry()['ROBOTS'].get_all_robots()
    for rb in robots:
        rb['endpoint'] = url_for('main.robot_detail', robot_id=rb['id'])
    return render_template(
        "home.html",
        robots=robots
    )


@main.route('/schedule', methods=['GET', 'POST'])
def schedule():
    return render_template("schedule.html")


@main.route('/rit_inspection_approval/<robot_id>', methods=['POST'])
def rit_inspection_approval(robot_id):
    valid, inputs = RobotInspectionTableHandler.validate_inputs(request.form)
    if valid:
        RobotInspectionTableHandler.approve_and_store_volume(
            inputs[RobotInspectionTableHandler.HEIGHT],
            inputs[RobotInspectionTableHandler.WIDTH],
            inputs[RobotInspectionTableHandler.BREADTH],
            robot_id
        )
    return robot_detail(robot_id=robot_id, inputs=inputs)


@main.route('/not_found', methods=['GET', 'POST'])
def not_found():
    return render_template("not_found.html")


@main.route('/robot/<robot_id>', methods=['POST'])
def advance_level(robot_id):
    robot = r.get_registry()['ROBOTS'].get_robot(robot_id)

    if not robot:
        return render_template("not_found.html")

    runs = r.get_registry()['RUNS'].get_runs(robot_id)

    eligible = LevelProgressHandler.get_eligibility_for_next_run(runs, robot['level'])

    if eligible.get('can_level_up') and not eligible['disqualified']:
        r.get_registry()['ROBOTS'].advance_level(robot_id, robot['level'])
        return redirect(url_for('main.robot_add_run', robot_id=robot_id))

    return "Robot not eligible to advance to next level.\n"


@main.route('/robot/<robot_id>', methods=['GET', 'POST'])
def robot_detail(robot_id, inputs=None):
    robot = r.get_registry()['ROBOTS'].get_robot(robot_id)
    if not robot:
        return render_template("not_found.html")

    runs = r.get_registry()['RUNS'].get_runs(robot_id)
    run_levels = [run['id'] for run in runs]

    # check if disqualifited and eligibility to advnace to next level
    eligibility = LevelProgressHandler.get_eligibility_for_next_run(
        runs, robot['level']
    )
    # get current best scores
    best_scores, attempted_levels, total_score, num_successful = (
        ScoreCalculator.get_best_scores(runs)
    )
    return render_template(
        "robot.html",
        attempted_levels=attempted_levels,
        total_score=total_score,
        robot_id=robot_id,
        robot=robot,
        disqualified=eligibility['disqualified'],
        eligible=eligibility['can_level_up'],
        best_scores=best_scores,
        robot_runs=runs,
        applied_factors=[applied_factors(id, robot_id) for id in run_levels],
        inputs=inputs
    )


@main.route('/robot/<robot_id>/addrun', methods=['GET', 'POST'])
def robot_add_run(robot_id):
    # get current robot object
    robot = r.get_registry()['ROBOTS'].get_robot(robot_id)
    if not robot:  # if invalid robot_id
        return render_template("not_found.html")
    # get all previous runs
    all_runs = r.get_registry()['RUNS'].get_runs(robot_id)

    # if GET request
    if request.method == 'GET':
        # get all previous runs
        return render_template(
            "run.html",
            robot=robot,
            division=get_division_label(robot['division']),
            input=request.args,
            error={},
            all_runs=all_runs
        )
    # request is POST
    # validate input data
    form = Runs.convert_to_dict(request.form)
    error = Runs.validate_form(
        form,
        robot['level'],
        robot['division'],
        robot['name']
    )

    if error:
        print error
        return render_template(
            "run.html",
            robot=robot,
            division=get_division_label(robot['division']),
            input=form,
            error=error,
            all_runs=all_runs
        )


    # calculate score
    actual_time, score = Runs.get_score(robot, form)

    # insert into databse
    r.get_registry()['RUNS'].record_run(
        level=robot['level'],
        failed_trial=form[Runs.RUN_DISQ],
        actual_time=actual_time,
        non_air=form[Runs.NON_AIR],
        furniture=form[Runs.FURNITURE],
        arbitrary_start=form[Runs.ARBITRARY_START],
        return_trip=form[Runs.RETURN_TRIP],
        candle_location_mode=form[Runs.NO_CANDLE_CIRCLE],
        stopped_within_circle=form[Runs.STOPPED_WITHIN_30],
        signaled_detection=form[Runs.CANDLE_DETECTED],
        num_rooms_searched=form[Runs.NUM_ROOMS],
        kicked_dog=form[Runs.KICKED_DOG],
        touched_candle=form[Runs.TOUCHED_CANDLE],
        cont_wall_contact=form[Runs.WALL_CONTACT],
        ramp_hallway=form[Runs.RAMP_USED],
        alt_target=form[Runs.BABY_RELOCATED],
        all_candles=form[Runs.ALL_CANDLES],
        used_versa_valve=form[Runs.VERSA_VALVE_USED],
        score=score,
        robot_id=robot_id
    )
    return redirect(url_for('main.robot_detail', robot_id=robot_id))



@main.route('/scoreboard', methods=['GET', 'POST'])
def scoreboard_home():
    return render_template("scoreboard_home.html")


@main.route('/scoreboardcsv', methods=['GET', 'POST']) 
def export_to_csv():
    divisions = ['junior', 'walking', 'high_school', 'senior']

    all_robots = {}

    for division in divisions:
        all_robots[division] = r.get_registry()['ROBOTS'].get_all_robots_division(division);

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
        sorted_robots = sorted(list(all_robots[div]), key=lambda k: k['name'])
        sorted_robots = sorted(list(sorted_robots), key=lambda k: k['TFS'])


        for index, sorted_r in enumerate(sorted_robots, start=1):
            cw.writerow([index, sorted_r['division'], sorted_r['name'], sorted_r['num_successful'],
                        sorted_r['level'], sorted_r['LS1'], sorted_r['LS2'], sorted_r['LS3'],
                         sorted_r['TFS']])

        cw.writerow('\n')

    output = make_response(si.getvalue())
    si.close()
    output.headers["Content-Disposition"] = "attachment; filename=scoreboard.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@main.route('/scoreboard/brd/<division>', methods=['GET', 'POST'])
def scoreboard_brd(division):
    robots = r.get_registry()['ROBOTS'].get_all_robots_division(division)

    if not robots:
        return render_template("not_found.html")

    # add additional parameters to be displayed on scoreboard
    robots = ScoreBoard.add_scoreboard_params(robots)

    # sort based on name then total score
    sorted_robots = sorted(list(robots), key=lambda k: k['name'])
    sorted_robots = sorted(list(sorted_robots), key=lambda k: k['TFS'])

    return render_template(
        "scoreboard_brd_gpmp.html",
        robots=sorted_robots,
        scoreboard_name=get_division_label(division)
    )

@main.route('/scoreboard/gpmp', methods=['GET', 'POST'])
def scoreboard_gpmp():
    robots = r.get_registry()['ROBOTS'].get_all_robots()

    if not robots:
        return render_template("not_found.html")

    # add additional parameters to be displayed on scoreboard
    robots = ScoreBoard.add_scoreboard_params(robots)

    # sort based on name then total score
    sorted_robots = sorted(list(robots), key=lambda k: k['name'])
    sorted_robots = sorted(list(sorted_robots), key=lambda k: k['TFS'])

    return render_template(
        "scoreboard_brd_gpmp.html",
        robots=sorted_robots,
        scoreboard_name="Grand Performance"
    )


@main.route('/scoreboard/lisp/<level>', methods=['GET', 'POST'])
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
    filtered_robots = ScoreBoard.filter_robots_level(robots, int(level))

    # key used for sorting
    score_name = "LS" + level

    # sort based on name then this level's lowest score
    sorted_robots = sorted(list(filtered_robots), key=lambda k: k['name'])
    sorted_robots = sorted(list(sorted_robots), key=lambda k: k[score_name])

    return render_template(
        "scoreboard_lisp.html",
        robots=sorted_robots,
        level=level,
        score_name=score_name
    )

@main.route('/prizes', methods=['GET', 'POST'])
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


def applied_factors(run_id, robot_id):
    query = ("""SELECT * FROM runs where id = %(run_id)s;""")
    data = {
        'run_id': run_id
    }
    run_data = r.get_registry()['MY_SQL'].get(query, data)

    query = ("""SELECT division FROM robots where id = %(robot_id)s;""")
    data = {
        'robot_id': robot_id
    }
    robot_div = r.get_registry()['MY_SQL'].get(query, data).get('division')

    run_level = run_data['level']

    applied_oms = ""
    applied_rf = ""
    applied_pp = ""

    if run_data.get('failed_trial') == 1:
        if run_level == 1 and robot_div in ['junior', 'walking']:
            if (run_data.get('num_rooms_searched', 0) > 0):
                applied_oms += 'Task.search:-30x%d rooms\n' % (run_data.get('num_rooms_searched', 0))
            applied_oms += 'Task.detect:-30\n' if run_data.get('signaled_detection', 0) == 1 else ''
            applied_oms += 'Task.position:-30\n' if run_data.get('stopped_within_circle', 0) == 1 else ''
    else:
        if run_data.get('touched_candle', 0) > 0:
            applied_pp += 'PP.candle=%d\n' % (run_data.get('touched_candle', 0) * 50)
        if run_data.get('cont_wall_contact', 0) > 0:
            applied_pp += 'PP.slide=%dcm/2\n' % (run_data.get('cont_wall_contact', 0))
        applied_pp += 'PP.dog=50\n' if run_data.get('kicked_dog', 0) == 1 else ''

        if run_level == 1:
            applied_oms += 'OM.candle=0.75\n' if run_data.get('candle_location_mode', 0) == 1 else ''

        if run_level in [1,2]:
            applied_oms += 'OM.start=0.8\n' if run_data.get('arbitrary_start', 0) == 1 else ''
            applied_oms += 'OM.return=0.8\n' if run_data.get('return_trip', 0) == 1 else ''
            applied_oms += 'OM.extinguisher=0.75\n' if run_data.get('non_air', 0) == 1 else ''
            applied_oms += 'OM.furniture=0.75\n' if run_data.get('furniture', 0) == 1 else ''

            if run_data.get('num_rooms_searched') == 1:
                applied_rf += 'Room Factor:1\n'
            elif run_data.get('num_rooms_searched') == 2:
                applied_rf += 'Room Factor:0.85\n'
            elif run_data.get('num_rooms_searched') == 3:
                applied_rf += 'Room Factor:0.5\n'
            elif run_data.get('num_rooms_searched') == 4:
                applied_rf += 'Room Factor:0.35\n'

        elif run_level == 3:
            applied_oms += 'OM.Alt_Target=0.6\n' if run_data.get('alt_target', 0) == 1 else ''
            applied_oms += 'OM.Ramp_Hallway=0.9\n' if run_data.get('ramp_hallway', 0) == 1 else ''
            applied_oms += 'OM.All_Candles=0.6\n' if run_data.get('all_candles', 0) == 1 else '' 

    return {'applied_oms': applied_oms, 'applied_rf': applied_rf, 'applied_pp': applied_pp}
