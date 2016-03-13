# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, request, redirect
import registry as r

main = Blueprint('main', __name__)

# name of all html form inputs, order matters
params_all = ['name',
        'run_disqualified',
        'seconds_to_put_out_candle_1',
        'seconds_to_put_out_candle_2',
        'non_air',
        'furniture',
        'arbitrary_start',
        'return_trip',
        'no_candle_circle',
        'stopped_within_30',
        'candle_detected',
        'number_of_rooms_searched',
        'kicked_dog',
        'touched_candle',
        'wall_contact_cms',
        'ramp_used',
        'baby_relocated',
        'all_candles',
        'versa_valve_used']

# sublist of name of all checkboxes
boolean_params = ['run_disqualified',
                'non_air',
                'furniture',
                'arbitrary_start',
                'return_trip',
                'no_candle_circle',
                'stopped_within_30',
                'candle_detected',
                'kicked_dog',
                'touched_candle',
                'ramp_used',
                'baby_relocated',
                'all_candles',
                'versa_valve_used']

# sublist of name of inputs that need string input
input_params = ['name',
            'seconds_to_put_out_candle_1',
            'seconds_to_put_out_candle_2',
            'number_of_rooms_searched',
            'wall_contact_cms']


@main.route('/home', methods=['GET', 'POST'])
def home():
    robots = r.get_registry()['ROBOTS'].get_all_robots()
    for rb in robots:
        rb['endpoint'] = url_for('main.robot_detail', robot_id=rb['id'])
    return render_template(
        "home.html",
        robots=robots
    )


@main.route('/', methods=['GET', 'POST'])
def signin():
    return render_template("signin.html")


@main.route('/schedule', methods=['GET', 'POST'])
def schedule():
    return render_template("schedule.html")


@main.route('/not_found', methods=['GET', 'POST'])
def not_found():
    return render_template("not_found.html")


@main.route('/robot/<robot_id>', methods=['GET', 'POST'])
def robot_detail(robot_id):
    robot = r.get_registry()['ROBOTS'].get_robot(robot_id)

    # if POST advance robot's level and redirect to add run page
    if request.method == 'POST':
        r.get_registry()['ROBOTS'].advance_level(robot_id, robot['level'])
        return redirect(url_for('main.robot_add_run', robot_id = robot_id))

    runs = r.get_registry()['RUNS'].get_runs(robot_id)
    run_levels = get_values_of_dicts('id', list(runs))

    # check if disqualifited and eligibility to advnace to next level
    disqualified, eligible = check_if_eligible(runs, robot['level'])

    # get current score data
    scores= {}
    scores['LS1'], scores['LS2'], scores['LS3'], scores['TFS'], scores['completed']= calculate_scores(runs)

    print "Is disqulified: " + str(disqualified)
    print "Is eligible: " + str(eligible)

    if not robot:
        return render_template("not_found.html")
    if not runs and robot:
        return render_template(
            "robot.html",
            robot_name=robot['name'],
            robot_id=robot_id,
            robot_level=robot['level']
        )
    else:
        return render_template(
            "robot.html",
            robot_name=robot['name'],
            robot_id=robot_id,
            robot_runs = runs,
            robot_level=robot['level'],
            disqualified=disqualified,
            eligible=eligible,
            scores=scores,
            applied_factors = [applied_factors(id, robot_id) for id in run_levels]
        )

@main.route('/robot/<robot_id>/addrun', methods=['GET', 'POST'])
def robot_add_run(robot_id):
    robot = r.get_registry()['ROBOTS'].get_robot(robot_id)
    runs = r.get_registry()['RUNS'].get_runs(robot_id)

    if not robot:
        return render_template("not_found.html")

    if request.method == 'GET':
        #get all previous runs
        all_runs = r.get_registry()['RUNS'].get_runs(robot_id)
        #get data from previous run
        runs = r.get_registry()['RUNS'].get_runs_robot_level(robot['id'], robot['level'])

        if runs:
            last_run = runs[-1]

            return render_template(
                "run.html",
                level_number=1,
                robot=robot,
                input=get_data_from_prev(last_run),
                all_runs=all_runs
            )

        return render_template(
                "run.html",
                level_number=1,
                robot=robot,
                input=request.args,
                all_runs=all_runs
        )
    else:
        # get data from html form
        input_data = request.form

        # bind all paramters to associated values
        params_d = bind_params(input_data,robot_id, robot['level'])

        print params_d

        # if invalide input data
        err = validate_params(params_d, robot['level'], robot['name'])
        if len(err) > 0:
            err['ERR'] = True
            params_and_errors = {}
            params_and_errors.update(params_d) # leave data already entered unchanged
            params_and_errors.update(err) # include errors
            return render_template(
                "run.html",
                level_number=1,
                robot=robot,
                input=params_and_errors
            )

        # calculate score
        score = get_score(robot, params_d)
        print "DICT"
        print params_d

        # convert dict values to tuple to prepare to insert to DB
        params_t = convert_to_tuple(params_d, robot_id, score)
        print "TUPLE"
        print params_t

        # insert into databse
        print params_t
        r.get_registry()['RUNS'].record_run(*params_t)

        return redirect(url_for('main.robot_detail', robot_id = robot_id))

@main.route('/scoreboard', methods=['GET', 'POST'])
def scoreboard_home():
    return render_template("scoreboard_home.html")


@main.route('/scoreboard/<division>', methods=['GET', 'POST'])
def scoreboard(division):
    robots = r.get_registry()['ROBOTS'].get_all_robots_division(division)

    if not robots:
        return render_template("not_found.html")

    # get score for each level and total score
    for robot in robots:
        runs = r.get_registry()['RUNS'].get_runs(robot['id'])

        # calculate lowes scores for each level and TFS, returns tuple
        robot['LS1'], robot['LS2'], robot['LS3'], robot['TFS'], robot['completed']= calculate_scores(runs)

    # sort based on name then total score
    sorted_robots = sorted(list(robots), key=lambda k: k['name'])
    sorted_robots = sorted(list(sorted_robots), key=lambda k: k['TFS'])

    # page header label
    if division == 'junior':
        label = "Junior Division"
    elif division == 'walking':
        label = "Walking Division"
    elif division == 'high_school':
        label = "High School Division"
    else:
        label = "Senior Division"

    return render_template(
        "scoreboard.html",
        robots = sorted_robots,
        division = label
    )

#Calculate LS1, LS2, LS3, TFS to be displayed on the scoreboard
def calculate_scores(runs):
    LS1 = 600
    LS2 = 600
    LS3 = 600

    completed = []

    for run in runs:
        if run['level'] == 1:
            if 1 not in completed:
                completed.append(1)
            if run['score'] <= LS1:
                LS1 = run['score']
        if run['level'] == 2:
            if 2 not in completed:
                completed.append(2)
            if run['score'] <= LS2:
                LS2 = run['score']
        if run['level'] == 3:
            if 3 not in completed:
                completed.append(3)
            if run['score'] <= LS3:
                LS3 = run['score']

    TFS = LS1 + LS2 + LS3

    return (LS1, LS2, LS3, TFS, completed)

def get_data_from_prev(prev_run):
    return {
        'non_air': prev_run['non_air'],
        'furniture': prev_run['furniture'],
        'arbitrary_start': prev_run['arbitrary_start'],
        'return_trip': prev_run['return_trip'],
        'no_candle_circle': prev_run['candle_location_mode'],
        'versa_valve_used': prev_run['used_versa_valve']
    }

# check if robot is eligible to advnace to new level and if robot is disqulified
def check_if_eligible(runs, current_level):
    # initial values
    disqualified = False
    eligible = False

    if runs:
        current_level_runs = 0
        cons_failed_count = 0
        successful_trial = False

        for run in runs:
            if current_level == run['level']:
                current_level_runs += 1
                if run['failed_trial']:
                    cons_failed_count += 1
                else:
                    successful_trial = True

                    # reset consecutive failure counter
                    cons_failed_count = 0

                # if three consecutive failures
                if cons_failed_count == 3:
                    break

        print "cons_failed count: " + str(cons_failed_count)

        # if robot has attempted current level
        if current_level_runs > 0:
            # if atleast one succesful trial
            if successful_trial:
                eligible = True

            # if has made three failed attempts at current level
            if cons_failed_count == 3 and current_level in [1,2]:
                disqualified = True

    return (disqualified, eligible)



#Getting values of specific key in the list of dictionaries
def get_values_of_dicts(key, runs):
    result = []
    for entries in runs:
        result.append(entries.get(key))
    return result

# convert dict values to tuple to prepare to insert to DB
def convert_to_tuple(dic, robot_id, score):
    # convert the dictionary values to tuples, order matters
    l = []

    l.append(dic['level'])
    l.append(dic['run_disqualified'])
    l.append((to_float(dic['seconds_to_put_out_candle_1']) +
              to_float(dic['seconds_to_put_out_candle_2']))/2.0) # average times by the 2 judges
    l.append(dic['non_air'])
    l.append(dic['furniture'])
    l.append(dic['arbitrary_start'])
    l.append(dic['return_trip'])
    l.append(dic['no_candle_circle'])
    l.append(dic['stopped_within_30'])
    l.append(dic['candle_detected'])
    l.append(to_int(dic['number_of_rooms_searched']))
    l.append(dic['kicked_dog'])
    l.append(dic['touched_candle'])
    l.append(to_int(dic['wall_contact_cms']))
    l.append(dic['ramp_used'])
    l.append(dic['baby_relocated'])
    l.append(dic['all_candles'])
    l.append(dic['versa_valve_used'])
    l.append(score)
    l.append(robot_id)

    return tuple(l)

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
def validate_params(input_data, level, name):
    # create a dictionary out of input data
    data = dict(input_data)

    err = dict()
    # if disqualified, only need to check for name
    if(data['run_disqualified']): 
        if not validate_name(data['name'], name):
            err['NAME_ERR'] = True
    # else validate every input
    else: 
        for p in input_params:
            if p in data:
                if p == 'name':
                    if not validate_name(data[p], name):
                        print "name error"
                        err['NAME_ERR'] = True
                elif p == 'seconds_to_put_out_candle_1':
                    if not validate_actual_time(data[p],level):
                        err["TIME_ERR_1"] = True
                elif p == 'seconds_to_put_out_candle_2':
                    if not validate_actual_time(data[p],level):
                        err["TIME_ERR_2"] = True
                elif p == 'number_of_rooms_searched':
                    if not validate_num_rooms(data[p], level):
                        err["ROOM_ERR"] = True
                elif p == 'wall_contact_cms':
                    if not validate_wall_contact(data[p]):
                        err["WALL_ERR"] = True
    return err


def validate_name(name, robot_name):
    return name == robot_name

# valide actual time
def validate_actual_time(time_s, level):
    # minimum and maximum time allowed for each level
    min_123 = 0 # minimum for any level
    max_1 = 180 # 3 minutes for level 1
    max_2 = 240 # 4 minutes for level 2
    max_3 = 300 # 5 minutes for level 3

    # special AT values in case of a failed trial
    fail_123 = 600 # trial failed (any level)
    traversed_3 = 500 # failed but traversed from arean A to B (level 3)
    found_baby_3 = 450 # failed but found baby (level 3)
    picked_baby_3 = 400 # failed but picked up baby (level 3)

    # check if input string is a number
    if not time_s.isdigit():
        return False

    # convet to a float
    time = float(time_s)

    # validation for level 1
    if ((level == 1)
        and (time < min_123 or time > max_1)
        and (time != fail_123)):

        return False

    # validation for level 2
    elif ((level == 2)
        and (time < min_123 or time > max_2)
        and (time != fail_123)):

        return False

    # validation for level 3
    elif ((level == 3)
        and (time < min_123 or time > max_3)
        and (time != fail_123)
        and (time != traversed_3)
        and (time != found_baby_3)
        and (time != picked_baby_3)):

        return False

    return True

# validate number of rooms
def validate_num_rooms(num_s, level):
    # minimum and maximum allowed values
    min_123 = 1
    max_123 = 4

    # check if input string is a number
    if level in [1,2]:
        if not num_s.isdigit():
            return False

        return (int(num_s) >= min_123) and (int(num_s) <= max_123)

    return True

# validate wall contact distance
def validate_wall_contact(num_s):
    # minimum and maximum allowed values
    min_123 = 0
    max_123 = 250 # length of arena

    # check if input string is a number
    if not num_s.isdigit():
        return False

    return (int(num_s) >= min_123) and (int(num_s) <= max_123)

# creates a dictionary out of data entered for new run
def bind_params(input_data, id, level):
    # create a dictionary out of input data
    data = dict(input_data)

    # create a dictionary of all parameters
    args = dict()

    args['level'] = level

    for p in params_all:
        # if key exists
        if p in data:
            if p in boolean_params:
                # if boolean and exists add True
                args[p] = True
            else:
                # data dict is of form {key:value} where value is of form [u'str']
                args[p] = data[p][0]
        else:
            if p in boolean_params:
                # if boolean and doesnt exist add False
                args[p] = False
            else:
                # add null for other non exisiting inputs params
                args[p] = None
    return args

# calculate and return score of current run
def get_score(robot, data):
    return r.get_registry()['RUNS'].calculate_run_score(
                        robot['division'],
                        robot['level'],
                        data['run_disqualified'],
                        (to_float(data['seconds_to_put_out_candle_1']) +
                        to_float(data['seconds_to_put_out_candle_2']))/2.0,
                        data['non_air'],
                        data['furniture'],
                        data['arbitrary_start'],
                        data['return_trip'],
                        data['no_candle_circle'],
                        data['stopped_within_30'],
                        data['candle_detected'],
                        to_int(data['number_of_rooms_searched']),
                        data['kicked_dog'],
                        data['touched_candle'],
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

    print 'run data'
    print run_data

    query = ("""SELECT division FROM robots where id = %(robot_id)s;""")
    data = {
        'robot_id': robot_id
    }
    robot_div = r.get_registry()['MY_SQL'].get(query, data).get('division')

    run_level = run_data['level']

    print robot_div

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
        applied_pp += 'PP.candle=50\n' if run_data.get('touched_candle', 0) == 1 else ''
        if run_data.get('slide', 0) > 0:
            applied_pp += 'PP.slide=%d cm/2\n' % (run_data.get('cont_wall_contact', 0)) == 1
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
 
