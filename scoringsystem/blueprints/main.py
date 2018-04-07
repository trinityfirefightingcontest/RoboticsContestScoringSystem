# -*- coding: utf-8 -*-
from flask import (
    Blueprint, render_template, url_for, request,
    redirect, session)
import registry as r
from libraries.utilities.authentication import AuthenticationUtilities
from libraries.utilities.level_progress_handler import LevelProgressHandler
from libraries.utilities.score_calculator import ScoreCalculator
from libraries.utilities.runs import Runs
from libraries.utilities.robot_inspection_table_handler import (
    RobotInspectionTableHandler
)


main = Blueprint('main', __name__)

# runs before all https requests to make sure user is logged in
@main.before_request
def require_login():
    if not AuthenticationUtilities.user_is_logged_in(session):
        return redirect(url_for('auth.signin'))


# get request handler for home page
@main.route('/', methods=['GET'])
def home():
    robots = r.get_registry()['ROBOTS'].get_all_robots()
    for rb in robots:
        rb['endpoint'] = url_for(
            'main.robot_detail',
            robot_id=rb['id']
        )
    return render_template(
        "home.html",
        robots=robots
    )


# get request handler for scoreboard page
@main.route('/scoreboard', methods=['GET'])
def scoreboard_home():
    return render_template("scoreboard_home.html")


# not found page
@main.route('/not_found', methods=['GET'])
def not_found():
    return render_template("not_found.html")


# post request handler for robot insepection form
@main.route('/rit_inspection_approval/<robot_id>', methods=['POST'])
def rit_inspection_approval(robot_id):
    # validate form
    valid, inputs = RobotInspectionTableHandler.validate_inputs(
        request.form
    )
    # if valid, check volume and store in db
    if valid:
        RobotInspectionTableHandler.approve_and_store_volume(
            inputs[RobotInspectionTableHandler.HEIGHT],
            inputs[RobotInspectionTableHandler.WIDTH],
            inputs[RobotInspectionTableHandler.BREADTH],
            robot_id
        )
    return robot_detail(robot_id=robot_id, inputs=inputs)


# post request handler for "advance to next level" button on robot detail page
@main.route('/robot/<robot_id>', methods=['POST'])
def advance_level(robot_id):
    # validate robot id
    robot = r.get_registry()['ROBOTS'].get_robot(robot_id)
    if not robot:
        return render_template("not_found.html")

    # get existing runs of robot
    runs = r.get_registry()['RUNS'].get_runs(robot_id)

    # check if robot is eligible to be advanced to next level
    eligible = LevelProgressHandler.get_eligibility_for_next_run(
        runs,
        robot['level']
    )
    # if eligible and has not be disqualified, advance robot to next level
    if eligible.get('can_level_up') and not eligible['disqualified']:
        # advance to next level by updating 'level' column in db
        r.get_registry()['ROBOTS'].advance_level(
            robot_id,
            robot['level']
        )
        # redirect to add run page
        return redirect(
            url_for('main.robot_add_run', robot_id=robot_id)
        )

    return "Robot not eligible to advance to next level.\n"


# get request handler for robot detail page
@main.route('/robot/<robot_id>', methods=['GET'])
def robot_detail(robot_id, inputs=None):
    # validate robot id
    robot = r.get_registry()['ROBOTS'].get_robot(robot_id)
    if not robot:
        return render_template("not_found.html")

    # get existing runs of robot
    runs = r.get_registry()['RUNS'].get_runs(robot_id)

    # check if disqualifited and eligibility to advnace to next level
    eligibility = LevelProgressHandler.get_eligibility_for_next_run(
        runs, robot['level']
    )
    # get current best scores
    best_scores, attempted_levels, total_score, num_successful = (
        ScoreCalculator.get_best_scores(runs)
    )

    # get all factors applied to the scores of previous runs
    run_levels = [run['id'] for run in runs]
    applied_factors = [
        get_applied_factors(id, robot_id) for id in run_levels
    ]
    # render template
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
        applied_factors=applied_factors,
        inputs=inputs
    )

# get and post request handler for add run page
@main.route('/robot/<robot_id>/addrun', methods=['GET', 'POST'])
def robot_add_run(robot_id):
    # validate robot it
    robot = r.get_registry()['ROBOTS'].get_robot(robot_id)
    if not robot:
        return render_template("not_found.html")

    # get all previous runs of robot
    all_runs = r.get_registry()['RUNS'].get_runs(robot_id)

    # if GET request
    if request.method == 'GET':
        return render_template(
            "run.html",
            robot=robot,
            division=get_division_label(robot['division']),
            input=request.args,
            error={},
            all_runs=all_runs
        )

    # make sure not more than 5 runs can be submitted
    if all_runs and len(all_runs) == 5:
        error = {'error': 'Cannot submit more than five runs'}
        return render_template(
            "run.html",
            robot=robot,
            division=get_division_label(robot['division']),
            input=request.form,
            error=error,
            all_runs=all_runs
        )

    # request is POST
    # validate input data
    form = Runs.convert_to_dict(request.form)  # convert to dict
    error = Runs.validate_form(
        form,
        robot['level'],
        robot['division'],
        robot['name']
    )

    # if error, re-render page with errors
    if error:
        error['error'] = '*Please fix all errors highlighted in red'
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

    # insert into database
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
        touched_candle=form[Runs.TOUCHED_CANDLE] or 0,
        cont_wall_contact=form[Runs.WALL_CONTACT],
        ramp_hallway=form[Runs.RAMP_USED],
        alt_target=form[Runs.SECONDARY_SAFE_ZONE],
        all_candles=form[Runs.ALL_CANDLES],
        used_versa_valve=form[Runs.VERSA_VALVE_USED],
        l3_traversed_hallway=form[Runs.L3_TRAVERSED_HALLWAY],
        l3_found_baby=form[Runs.L3_FOUND_BABY],
        l3_rescued_baby=form[Runs.L3_RESCUED_BABY],
        l3_all_candles=form[Runs.L3_ALL_CANDLES],
        l3_one_candle=form[Runs.L3_ONE_CANDLE],
        l3_none=form[Runs.L3_NONE],
        score=score,
        robot_id=robot_id,
    )

    # redirect to robot detail page
    return redirect(url_for('main.robot_detail', robot_id=robot_id))

# get probperly formatted string from division id
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


# calculate applied factors based on rules, needs more documentation
def get_applied_factors(run_id, robot_id):
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
