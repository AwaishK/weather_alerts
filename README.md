# QUICK START

## PROJECT STRUCTURE

```bash

├── app
│   ├── weather_alerts_api
│   │   │── core
│   │   │   │── models
│   │   │   │   │── subscription.py
│   │   │   │   │── database.py
│   │   │   │── schemas
│   │   │   │   │── subscription.py
│   │   │   │   │
│   │   │   │── views
│   │   │   │   │── subscription.py
│   │   │   │   │
│   │── main.py                    
│   │   │   
│   │   │ 
├── open_weather_map
│   │   │── api.py
│   │   │── exceptions.py
│   │   │── schedule.py
│   │   │
├── utils
│   │   │── config_parser.py
│   │   │── database_connection.py
│   │   │
└── README.md
└── Makefile
└── requirements.txt
└── config.ini
└── .env
└── env
```

## Database 

Please ensure you have database with the name `weather_alerts` and `test_weather_alerts`

## Installation & Setup

Run the following commands to clone the project and then create virtual enviroment

```bash
git clone git@github.com:AwaishK/weather_alerts.git
cd weather_alerts
make dev-env
```

Run the following command to add environemtns variable to your virtual env

```bash
printf "\nexport \$(grep -v '^#' .env | xargs)" >> env/bin/activate
```

Please use below given template to create a config file 
config_dot_ini_template is dummy file, please you same configuration but remember to change username and password

```bash
    config_dot_ini_template -> config.ini
```

Please use below given template to create a .env file
dot_env is dummy file, please use same env variables but remember to update the values

```bash
    dot_env -> .env
```

Please run below command to schedule the data pipeline

```bash
    python open_weather_map/schedule.py
```

Please run below command to run restful api

```bash
    python app/main.py
```

