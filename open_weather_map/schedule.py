"""This file is scheduing the pipeline to run it every day at 3 am 
"""
from pathlib import Path
from crontab import CronTab
from utils.config_parser import configuration_parser
import os


def main():
    """It will initializes and adds the cron job to cron tab
    """
    home_dir = Path(__file__).resolve().parent.parent
    file = f"{home_dir}/open_weather_map/api.py"
    env_comamnd = f"{home_dir}/env/bin/python"

    config = configuration_parser()
    system_user = dict(config["SYSTEM"])['username']
    
    cron = CronTab(user=system_user)

    job = cron.new(command=f'{env_comamnd} {file}', comment="weather_alerts")
    job.minute.every(1)
    
    job.setall('0 3 * * *')
    cron.write()


if __name__ == "__main__":
    main()
    