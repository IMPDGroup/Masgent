# src/vasp_agent/cli.py
import sys
from importlib.metadata import version, PackageNotFoundError

import vasp_agent.hello_world as hello_world
import vasp_agent.ai.ai_backend as ai_backend

def print_title():
    '''Print the VASP-Agent ASCII banner and metadata inside a box.'''

    # Retrieve installed version
    try:
        pkg_version = version('vasp-agent')
    except PackageNotFoundError:
        pkg_version = 'dev'

    # ASCII banner
    ascii_banner = rf'''
+-------------------------------------------------------------------------------------+
|                                                                                     |
|  ██╗   ██╗ █████╗ ███████╗██████╗      █████╗  ██████╗ ███████╗███╗   ██╗████████╗  |
|  ██║   ██║██╔══██╗██╔════╝██╔══██╗    ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝  |
|  ██║   ██║███████║███████╗██████╔╝    ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║     |
|  ╚██╗ ██╔╝██╔══██║╚════██║██╔═══╝     ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║     |
|   ╚████╔╝ ██║  ██║███████║██║         ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║     |
|    ╚═══╝  ╚═╝  ╚═╝╚══════╝╚═╝         ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝     |
|                                                          (c) 2025 Guangchen Liu     |
|  VASP-Agent CLI:  {pkg_version:<64}  |
|  Licensed:        MIT License                                                       |
|  Citation:        Liu, G. et al. (2025), DOI:10.XXXX/XXXXX'                         |
|  Repository:      https://github.com/aguang5241/VASP-Agent                          |
|  Contact:         gliu4@wpi.edu                                                     |
|                                                                                     |
+-------------------------------------------------------------------------------------+
    '''
    print(ascii_banner)

def print_help():
    print('\nVASP-Agent CLI')
    print('  Usage: vasp-agent <command>\n')
    print('Available commands:')
    print('  hello              → Print a hello message')
    print('  goodbye            → Print a goodbye message')
    print('  help               → Show this help message')
    print('  exit               → Exit the program\n')

def main():
    print_title()

    commands = {
        'hello': hello_world.say_hello,
        'goodbye': hello_world.say_goodbye,
        'ai': ai_backend.main,
    }

    try:
        # Enter interactive loop
        while True:
            user_input = input('Ask anything > ').strip().lower()

            if not user_input:
                continue  # ignore empty input
            if user_input in {'exit'}:
                print('Exiting VASP-Agent. Goodbye!')
                break
            elif user_input in {'help', '-h', '--help'}:
                print_help()
            elif user_input in commands:
                commands[user_input]()
            elif user_input.startswith('ai'):
                ai_backend.main()
            else:
                print(f'Unknown command: {user_input}')
                print('Type "help" to see available commands.')

    except (KeyboardInterrupt, EOFError):
        print('\nExiting VASP-Agent. Goodbye!')
        sys.exit(0)

if __name__ == '__main__':
    main()
