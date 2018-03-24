# RoboticsContestScoringSystem

More Info: http://www.trincoll.edu/events/robot/rules-1.html


# Setup
- cd ~
- virtualenv robotics
- source robotics/bin/activate
- pip install -r requirements.txt
- mysql.server start
- redis-server start
- gunicorn --bind 0.0.0.0:8090 run

# Requirements:
- MySQL (mysql-server)
- Python 2.7.3 (python)
- Redis 

# Additional packages that may be required on VPS:
- python-dev
- build-essential
- libmysqlclient-dev (different from mysql-server)
