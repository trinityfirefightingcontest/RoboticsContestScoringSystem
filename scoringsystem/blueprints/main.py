# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for
import registry as r

main = Blueprint('main', __name__)


@main.route('/home', methods=['GET', 'POST'])
def home():
    robots = [
        {
            'id': '0',
            'name': 'union',
            'school': 'school1'
        }, {
            'id': '1',
            'name': 'uhartford',
            'school': 'school2'
        }, {
            'id': '2',
            'name': 'providence',
            'school': 'school3'
        }, {
            'id': '3',
            'name': 'brown',
            'school': 'school4'
        }, {
            'id': '4',
            'name': 'tufts',
            'school': 'school5'
        }, {
            'id': '5',
            'name': 'trinity',
            'school': 'school1'
        }, {
            'id': '6',
            'name': 'colby',
            'school': 'school2'
        }, {
            'id': '7',
            'name': 'uconn',
            'school': 'school3'
        }, {
            'id': '8',
            'name': 'bates',
            'school': 'school4'
        }, {
            'id': '9',
            'name': 'williams',
            'school': 'school5'
        }
    ]
    for rb in robots:
        rb['endpoint'] = url_for('main.robot_detail', robot_id=rb['id'])
    return render_template(
        "home.html",
        robots=robots
    )


@main.route('/', methods=['GET', 'POST'])
def signin():
    return render_template("signin.html")


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
    return render_template(
        "run.html",
        robot_name=robot['name'],
        level_number=1,
        division='junior',
        input={'versa_valve_used': False}
    )
