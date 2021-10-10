cd /home/ubuntu/ToTheMoon
# PATH=/usr/local/bin:$PATH
pipenv run python3 db/insert_klines_for_past_hour.py >> /home/ubuntu/ToTheMoon/db/log.txt 2>&1