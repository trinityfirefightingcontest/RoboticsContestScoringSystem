# RoboticsContestScoringSystem

More Info: http://www.trincoll.edu/events/robot/rules-1.html


# Setup
- cd ~
- virtualenv robotics
- source robotics/bin/activate
- pip install -r requirements.txt
- service mysql start
- redis-server start
- (if first time) run load.py to create SQL table
- gunicorn --bind 0.0.0.0:8090 run

# Requirements:
###### Enclosed in parenthesis is the Ubuntu package name
- MySQL (mysql-server)
- Python 2.7.3 (python)
- Redis (redis-server)

## Additional packages that may be required on VPS (Ubuntu):
###### (Ubuntu) To install these packages and packages above, use sudo apt-get install <package_name>
- python-dev
- build-essential
- libmysqlclient-dev (different from mysql-server)
