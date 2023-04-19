import logging
import select
import sys
from typing import Dict, Callable, List


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


# A quick CLI implementation
# Main CLI loop is located here
def cmd_help():
    """ Shows all available commands """
    print("Available commands:")
    for item in CliLooper().commands:
        name = list(item.keys())[0]
        func = item[name]
        print(f"{name} - {func.__doc__}")


class CliLooper(metaclass=SingletonMeta):
    def __init__(self):
        # self.commands = List[Dict[str, Callable]]
        self.commands = [
            {"help": cmd_help}
        ]

        self.tick_while_idle = None

    def register_command(self, custom_name: str, callback: Callable):
        """ Register callback function """

        custom_name = custom_name.lower()

        if self.commands is not None and len(self.commands) > 0:
            for item in self.commands:
                name = list(item.keys())[0]
                if name == custom_name:
                    raise Exception("Tried to register same CLI command multiple times")

        self.commands.append({custom_name: callback})
        logging.debug(f"New command '{custom_name}' added.")

    def set_tick_when_idle(self, method: Callable):
        self.tick_while_idle = method

    def run(self):
        """ Infinite loop that runs CLI """
        print("Welcome to the silly command line interface")
        while True:
            selection = select.select([sys.stdin], [], [], 0.0)[0]
            if not selection or len(selection) == 0:
                # User has not entered anything
                if self.tick_while_idle is not None:
                    self.tick_while_idle()

                continue

            # Read the input
            in_string = input('> ')

            in_string = in_string.strip()
            if in_string is None or in_string == "":
                continue

            cmd_split = None
            cmd_name = None

            try:
                cmd_split = in_string.split()
                cmd_name = cmd_split[0]
                cmd_split.pop(0)
            except Exception as e:
                logging.error(f"Error! Could not parse command {str(e)}")

            if cmd_name is None:
                continue

            cmd_name = cmd_name.lower()
            cmd_found = False
            for item in self.commands:
                name = list(item.keys())[0]
                func = item[name]

                if name == cmd_name:
                    # noinspection PyBroadException
                    try:
                        if len(cmd_split) > 0:
                            func(*cmd_split)
                        else:
                            func()
                    except Exception as e:
                        # TODO: better error handling and parameterization
                        logging.error("Method execution Exception: Probably invalid parameter. Details: " + str(e))

                    cmd_found = True
                    break

            if not cmd_found:
                logging.warning(f"Command '{cmd_name}' not found")
