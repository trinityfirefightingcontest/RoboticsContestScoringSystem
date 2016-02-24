# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, request, redirect
import registry as r

main = Blueprint('main', __name__)

# name of all html form inputs, order matters
params_all = ['run_disqualified',
        'seconds_to_put_out_candle',
        'reached_time_limit',
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
                'reached_time_limit',
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
input_params = ['seconds_to_put_out_candle',
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
    if not robot:
        return render_template("not_found.html")
    return render_template(
        "robot.html",
        robot_name=robot['name'],
        robot_id=robot_id
    )


@main.route('/robot/<robot_id>/addrun', methods=['GET', 'POST'])
def robot_add_run(robot_id):
    robot = r.get_registry()['ROBOTS'].get_robot(robot_id)
    if not robot:
        return render_template("not_found.html")

    if request.method == 'GET':
        return render_template(
            "run.html",
            level_number=1,
            robot=robot,
            input=request.args
        )
    else:
        # get data from html form
        input_data = request.form

        # bind all paramters to associated values
        params_d = bind_params(input_data,robot_id, robot['level'])

        # if invalide input data
        err = validate_params(params_d, robot['level'])
        if len(err) > 0:
            params_and_errors = {}
            params_and_errors.update(params_d)
            params_and_errors.update(err)
            return render_template(
                "run.html",
                level_number=1,
                robot=robot,
                input=params_and_errors
            )

        # convert dict values to tuple
        params_t = convert_to_tuple(params_d)

        # insert into databse
        print params_t
        r.get_registry()['RUNS'].record_run(*params_t)

        return redirect(url_for('main.robot_detail', robot_id = robot_id))


def convert_to_tuple(dic):
    # convert the dictionary values to tuples, order matters
    l = []
    l.append(dic['id'])
    l.append(dic['level'])
    for p in params_all:
        l.append(dic[p])

    return tuple(l)

def validate_params(input_data, level):
    # create a dictionary out of input data
    data = dict(input_data)

    err = dict()
    # validate each parameter
    for p in input_params:
        if p in data:
            if p == 'seconds_to_put_out_candle':
                if not validate_actual_time(data[p],level):
                    err["TIME_ERR"] = True
            elif p == 'number_of_rooms_searched':
                if not validate_num_rooms(data[p]):
                    err["ROOM_ERR"] = True
            elif p == 'wall_contact_cms':
                if not validate_wall_contact(data[p]):
                    err["WALL_ERR"] = True
    return err

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

    # convet to an integer
    time = int(time_s)

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
        and (time != traversedAtoB_3)
        and (time != found_baby_3)
        and (time != picked_baby_3)):

        return False

    return True


def validate_num_rooms(num_s):
    # minimum and maximum allowed values
    min_123 = 1
    max_123 = 8

    # check if input string is a number
    if not num_s.isdigit():
        return False

    return (int(num_s) >= min_123) and (int(num_s) <= max_123)

def validate_wall_contact(num_s):
    # minimum and maximum allowed values
    min_123 = 0
    max_123 = 250 # length of arena

    # check if input string is a number
    if not num_s.isdigit():
        return False

    return (int(num_s) >= min_123) and (int(num_s) <= max_123)

def bind_params(input_data, id, level):
    # create a dictionary out of input data
    data = dict(input_data)

    # create a dictionary of all parameters
    args = dict()

    args['id'] = id
    args['level'] = level

    for p in params_all:
        # if key exists
        if p in data:
            if p in boolean_params:
                # if boolean and exists add True
                args[p] = True
            else:
                # dict is of form {key:value} where value is of form [u'str']
                args[p] = data[p][0]
        else:
            if p in boolean_params:
                # if boolean and doesnt exist add False
                args[p] = False
            else:
                # add null for other non exisiting inputs params
                args[p] = None

    return args
