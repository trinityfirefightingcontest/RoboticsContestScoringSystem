# -*- coding: utf-8 -*-
from flask import (
    Blueprint, render_template, url_for, request,
    redirect, session, make_response)
import registry as r
import StringIO
import csv
import logging
from libraries.utilities.authentication import AuthenticationUtilities
from libraries.utilities.level_progress_handler import LevelProgressHandler
from libraries.utilities.score_calculator import ScoreCalculator
from libraries.utilities.run_parameters import RunParameters
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
    robot = r.get_registry()['ROBOTS'].get_robot(robot_id)

    if not robot:
        return render_template("not_found.html")

    all_runs = r.get_registry()['RUNS'].get_runs(robot_id)
    if request.method == 'GET':
        # get all previous runs
        return render_template(
            "run.html",
            robot=robot,
            division=get_division_label(robot['division']),
            input=request.args,
            all_runs=all_runs
        )
    # For post request

    # Database query for showing past runs if the POST fails

    all_runs = r.get_registry()['RUNS'].get_runs(robot_id)

    # if invalidate input data
    params_d = bind_params(request.form, robot_id, robot['level'])

    err = validate_params(params_d,
                          robot['level'],
                          robot['division'],
                          robot['name'])

    if err:
        err['ERR'] = True
        params_and_errors = {}
        params_and_errors.update(params_d)
        # leave data already entered unchanged
        params_and_errors.update(err)  # include errors
        return render_template(
            "run.html",
            robot=robot,
            division=get_division_label(robot['division']),
            input=params_and_errors,
            all_runs=all_runs
        )

    # calculate score
    score = get_score(robot, params_d)
    # convert dict values to tuple to prepare to insert to DB
    params_t = convert_to_tuple(params_d, robot_id, score)
    # insert into databse
    r.get_registry()['RUNS'].record_run(*params_t)
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
    robots = add_scoreboard_params(robots)

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
    robots = add_scoreboard_params(robots)

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
    if int(level) not in [1,2,3]:
        return render_template("not_found.html")

    robots = r.get_registry()['ROBOTS'].get_all_robots()

    if not robots:
        return render_template("not_found.html")

    # add additional parameters to be displayed on scoreboard
    robots = add_scoreboard_params(robots)

    # filter robots
    filtered_robots = filter_robots(robots, int(level))

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

# adds necessary parameters to be displayed on the scoreboard
def add_scoreboard_params(robots):
    for robot in robots:
        runs = r.get_registry()['RUNS'].get_runs(robot['id'])
        best_scores, attempted_levels, total_score, num_successful = (
            ScoreCalculator.get_best_scores(runs)
        )
        robot.update(best_scores)
        robot['TFS'] = total_score
        robot['completed'] = attempted_levels
        robot['num_successful'] = num_successful

    return robots

# filter robots that should be shown on scoreboard
def filter_robots(robots, level):
    if level == 1:
        filtered = [robot for robot in robots if 1 in robot['completed'] and 2 not in robot['completed']]
    elif level == 2:
        filtered = [robot for robot in robots if 2 in robot['completed']]
    else:
        filtered = [robot for robot in robots if 3 in robot['completed']]

    return filtered

# convert dict values to tuple to prepare to insert to DB
def convert_to_tuple(dic, robot_id, score):
    # convert the dictionary values to tuples, order matters
    l = []

    l.append(dic['level'])
    l.append(dic['run_disqualified'])
    l.append((to_float(dic['seconds_to_put_out_candle_1']) +
              to_float(dic['seconds_to_put_out_candle_2'])) / 2.0)
    # average times by the 2 judges
    l.append(dic['non_air'])
    l.append(dic['furniture'])
    l.append(dic['arbitrary_start'])
    l.append(dic['return_trip'])
    l.append(dic['no_candle_circle'])
    l.append(dic['stopped_within_30'])
    l.append(dic['candle_detected'])
    l.append(to_int(dic['number_of_rooms_searched']))
    l.append(dic['kicked_dog'])
    l.append(to_int(dic['touched_candle']))
    l.append(to_int(dic['wall_contact_cms']))
    l.append(dic['ramp_used'])
    l.append(dic['baby_relocated'])
    l.append(dic['all_candles'])
    l.append(dic['versa_valve_used'])
    l.append(score)
    l.append(robot_id)

    return tuple(l)

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

# convert string to float
def to_float(input_s):
    if input_s:
        return float(input_s)

    # only true when run is disqualified
    return 0

# convert string to float
def to_int(input_s):
    if input_s:
        return int(input_s)

    # only true when run is disqualified
    return 0

# validate input
def validate_params(input_data, level, div, name):
    # create a dictionary out of input data
    data = dict(input_data)

    err = dict()
    # if disqualified, need to check for name, AT and num of rooms
    if(data['run_disqualified']): 
        if not validate_name(data['name'], name):
            err['NAME_ERR'] = True
        if not validate_actual_time(data['seconds_to_put_out_candle_1'],level, True):
            err["TIME_ERR_1"] = True
        if not validate_actual_time(data['seconds_to_put_out_candle_2'],level, True):
            err["TIME_ERR_2"] = True
        if not validate_actual_time_compare(data['seconds_to_put_out_candle_1'],
                                            data['seconds_to_put_out_candle_2']):
            err["TIME_ERR_DIFF"] = True
        if ((level == 1)
            and (div in ['junior', 'walking'])
            and (not validate_num_rooms(data['number_of_rooms_searched'], level))):
            err["ROOM_ERR"] = True

    # else validate every input
    else:
        for p in RunParameters.ALL:
            if p in data:
                if p == 'name':
                    if not validate_name(data[p], name):
                        err['NAME_ERR'] = True
                elif p == 'seconds_to_put_out_candle_1':
                    if not validate_actual_time(data[p],level, False):
                        err["TIME_ERR_1"] = True
                elif p == 'seconds_to_put_out_candle_2':
                    if not validate_actual_time(data[p],level, False):
                        err["TIME_ERR_2"] = True
                elif p == 'number_of_rooms_searched':
                    if not validate_num_rooms(data[p], level):
                        err["ROOM_ERR"] = True
                elif p == 'wall_contact_cms':
                    if not validate_wall_contact(data[p]):
                        err["WALL_ERR"] = True
                elif p == 'touched_candle':
                    if not validate_touched_candle(data[p]):
                        err["CANDLE_ERR"] = True
    return err


def validate_name(name, robot_name):
    return name == robot_name

def validate_actual_time_compare(time_j1, time_j2):

    time_j1 = time_j1.strip()
    time_j2 = time_j2.strip()

    if time_j1.isdigit() and time_j2.isdigit():
        return float(time_j1) == float(time_j2)
    return False

# valide actual time
def validate_actual_time(time_s, level, failed):
    # minimum and maximum time allowed for each level

    time_s = time_s.strip()

    min_123 = 0  # minimum for any level
    max_1 = 180  # 3 minutes for level 1
    max_2 = 240  # 4 minutes for level 2
    max_3 = 300  # 5 minutes for level 3

    # special AT values in case of a failed trial
    fail_123 = 600  # trial failed (any level)
    traversed_3 = 500  # failed but traversed from arean A to B (level 3)
    found_baby_3 = 450  # failed but found baby (level 3)
    picked_baby_3 = 400  # failed but picked up baby (level 3)

    # check if input string is a number
    

    # convet to a float
    try: 
        time = float(time_s)
    except ValueError:
        return False

    # validation for level 1
    if level == 1:
        if failed and (time != fail_123):
            return False;
        elif (not failed) and  (time < min_123 or time > max_1):
            return False

    # validation for level 2
    elif level == 2:
        if failed and (time != fail_123):
            return False;
        elif (not failed) and  (time < min_123 or time > max_2):
            return False

    # validation for level 3
    elif level == 3:
        if (failed
            and (time != fail_123)
            and (time != traversed_3)
            and (time != found_baby_3)
            and (time != picked_baby_3)):

            return False;

        elif (not failed) and  (time < min_123 or time > max_3):
            return False
    return True


# validate number of rooms
def validate_num_rooms(num_s, level):

    num_s = num_s.strip()
    # minimum and maximum allowed values
    min_123 = 0
    max_123 = 4

    # check if input string is a number
    if level in [1, 2]:
        if not num_s.isdigit():
            return False

        return (int(num_s) >= min_123) and (int(num_s) <= max_123)

    return True


# validate wall contact distance
def validate_wall_contact(num_s):

    num_s = num_s.strip()
    # minimum and maximum allowed values
    min_123 = 0
    max_123 = 500 # length of arena

    # check if input string is a number
    if not num_s.isdigit():
        return False

    return (int(num_s) >= min_123) and (int(num_s) <= max_123)

#validate touched_candle 
def validate_touched_candle(num_s):

    num_s = num_s.strip()
    
    # Just check if it's digit for now
    # minimum allowed value
    min_123 = 0

    # check if input string is a number
    if not num_s.isdigit():
        return False

    return int(num_s) >= min_123

# creates a dictionary out of data entered for new run
def bind_params(input_data, id, level):
    # create a dictionary out of input data
    data = dict(input_data)
    # create a dictionary of all parameters
    args = {}
    args['level'] = level
    for p in RunParameters.ALL:
        if p in RunParameters.BOOLEANS:
            args[p] = bool(data.get(p))
        else:
            # data dict is of form {key:value}
            # where value is of form [u'str']
            args[p] = data[p][0] if data.get(p) else None
    return args


# calculate and return score of current run
def get_score(robot, data):
    return r.get_registry()['RUNS'].calculate_run_score(
        robot['division'],
        robot['level'],
        data['run_disqualified'],
        (to_float(data['seconds_to_put_out_candle_1']) +
         to_float(data['seconds_to_put_out_candle_2'])) / 2.0,
        data['non_air'],
        data['furniture'],
        data['arbitrary_start'],
        data['return_trip'],
        data['no_candle_circle'],
        data['stopped_within_30'],
        data['candle_detected'],
        to_int(data['number_of_rooms_searched']),
        data['kicked_dog'],
        to_int(data['touched_candle']),
        to_int(data['wall_contact_cms']),
        data['ramp_used'],
        data['baby_relocated'],
        data['all_candles'])


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
