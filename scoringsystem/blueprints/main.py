# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, request
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
    runs = r.get_regitstry()['runs'].get_runs(robot_id);
    if not robot:
        return render_template("not_found.html")
    return render_template(
        "robot.html",
        robot_name=robot['name'],
        robot_id=robot_id,
        robot_runs = get_runs(robot_id)
    )


@main.route('/robot/<robot_id>/addrun', methods=['GET', 'POST'])
def robot_add_run(robot_id):
    robot = r.get_registry()['ROBOTS'].get_robot(robot_id)
    if not robot:
        return render_template("not_found.html")
    return render_template(
        "run.html",
        level_number=1,
        robot=robot,
        input=request.args
    )
