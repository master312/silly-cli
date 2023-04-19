# File used as glue to glue click commands and cli_looper class

# Important to be imported first
from cli_looper import CliLooper

# Import other command files here
import example_commands

# Initialize looper singleton
CliLooper()

# Register example commands
example_commands.register_example_commands()

# Run infinite loop
CliLooper().run()
