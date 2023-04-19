# File used as glue to glue click commands and cli_looper class

# Important to be imported first
from cli_looper import CliLooper

# Import other command files here
import example_commands

# Initialize looper singleton
CliLooper()

# Register example commands
example_commands.register_example_commands()


def tick_when_idle():
    # print("TICKING WHILE IDLEEEE")
    pass


# Run infinite loop
CliLooper().set_tick_when_idle(tick_when_idle)
CliLooper().run()
