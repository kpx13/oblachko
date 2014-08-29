# -*- coding: utf-8 -*-
import tornado.options
import os
import logging.config
from jinja2 import Environment, FileSystemLoader


app_options = {
    "dev" : {
        'db_name': 'bb_dev',
        'log_db_name': 'log_bb_dev',
        'pycket' : {
                'engine': 'memcached',
                'storage': {'servers': ('localhost:11211',)},
                'cookies': {'expires_days': 120}},
    },

    "test": {
        'db_name': 'bb_test',
        'log_db_name': 'log_bb_test',
    }
               
}


STATIC_ROOT = os.path.join(os.path.dirname(__file__), "./static")
TEMPLATE_ROOT = os.path.join(os.path.dirname(__file__), "./templates")

default_app_options = dict(
    template_path = TEMPLATE_ROOT,
    static_path = STATIC_ROOT,
    xsrf_cookies = True,
    cookie_secret= "11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    login_url = "/auth/login",
    autoescape = None,

)

jinja_settings = {
    'autoescape': True,
    'extensions': [
        'jinja2.ext.with_'
    ],
}
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_ROOT),
    **jinja_settings)



# See PEP 391 and logconfig for formatting help.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'main_formatter': {
            'format': '%(levelname)-12s %(filename)-24s [LINE:%(lineno)d][%(asctime)s]  %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'rotate_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(os.path.dirname(__file__), "./logs/main.log"),
            'when': 'midnight',
            'interval':    1,  # day
            'backupCount': 7,
            'formatter': 'main_formatter',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
            # 'filters': ['require_local_true'],
        },
    },
    'loggers': {
        '': {
            'handlers': ['rotate_file', 'console'],
            'level': 'DEBUG',
        }
    }
}

logging.config.dictConfig(LOGGING)


def get(key):
    if 'environment' in tornado.options.options:
        env = tornado.options.options.environment
    else:
        env = 'test'

    if env not in app_options:
        raise Exception("Invalid Environment (%s)" % env)
    v = app_options.get(env).get(key) or default_app_options.get(key)
    if callable(v):
        return v()
    return v
