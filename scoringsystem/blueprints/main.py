# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, request, redirect
import registry as r

main = Blueprint('main', __name__)


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
    runs = r.get_registry()['RUNS'].get_runs(robot_id)
    if not robot:
        return render_template("not_found.html")
    if not runs and robot:
        return render_template(
            "robot.html",
            robot_name=robot['name'],
            robot_id=robot_id
        )
    else:
        return render_template(
            "robot.html",
            robot_name=robot['name'],
            robot_id=robot_id,
            robot_runs = runs
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

        # TODO: validate input data

        # insert into databse
        params = bind_params(input_data,robot_id, 1)
        print params
        r.get_registry()['RUNS'].record_run(*params)

        return redirect(url_for('main.robot_detail', robot_id = robot_id))


def bind_params(input_data, id, level):
    # name of all html form inputs, order matters
    params = ['run_disqualified',
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

    # sublist of name of all checkboxes in form
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

    # create a dictionary out of data
    data = dict(input_data)

    # create a list of all arguments using input data
    args = [id, level]
    for p in params:
        # if key exists
        if p in data:
            if p in boolean_params:
                # if boolean and exists add True
                args.append(True)
            else:
                # dict is of form {key:value} where value is of form [u'str']
                args.append(data[p][0])
        else:
            if p in boolean_params:
                # if boolean and doesnt exist add False
                args.append(False)
            else:
                # add null for other non exisiting inputs params
                args.append(None)

    # convert list to tuple
    args_t = tuple(args)

    return args_t
    
