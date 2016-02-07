# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for

main = Blueprint('main', __name__)


@main.route('/home', methods=['GET', 'POST'])
def home():
    robots = [
        {
            'name': 'union',
            'school': 'school1'
        }, {
            'name': 'uhartford',
            'school': 'school2'
        }, {
            'name': 'providence',
            'school': 'school3'
        }, {
            'name': 'brown',
            'school': 'school4'
        }, {
            'name': 'tufts',
            'school': 'school5'
        }, {
            'name': 'trinity',
            'school': 'school1'
        }, {
            'name': 'colby',
            'school': 'school2'
        }, {
            'name': 'uconn',
            'school': 'school3'
        }, {
            'name': 'bates',
            'school': 'school4'
        }, {
            'name': 'williams',
            'school': 'school5'
        }
    ]
    for r in robots:
        r['endpoint'] = url_for('main.robot_detail', robot=r['name'])
    return render_template(
        "home.html",
        robots=robots
    )


@main.route('/', methods=['GET', 'POST'])
def signin():
    return render_template("signin.html")


@main.route('/robot/<robot>', methods=['GET', 'POST'])
def robot_detail(robot):
    return render_template("signin.html")
