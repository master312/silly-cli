from cli_looper import CliLooper
from datetime import datetime


def time():
    """ Prints current time """
    print(f"Current Time ={datetime.now()}")


def param_call(test_param: str):
    """ Prints test param. Param 1 = any str"""
    print(f"Param '{test_param}'")


def register_example_commands():
    CliLooper().register_command("time", time)
    CliLooper().register_command("param_test", param_call)
