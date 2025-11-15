# src/vasp_agent/cli.py
import sys
from vasp_agent import hello_world

def main():
    if len(sys.argv) < 2:
        print("Usage: vasp-agent <command>")
        print("Available commands: hello, goodbye")
        sys.exit(1)

    command = sys.argv[1].lower()

    commands = {
        "hello": hello_world.say_hello,
        "goodbye": hello_world.say_goodbye,
    }

    if command in commands:
        commands[command]()
    else:
        print(f"Unknown command: {command}")
        print("Available commands: hello, goodbye")
