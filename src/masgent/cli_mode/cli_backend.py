# masgent/cli_mode/cli_backend.py

import sys
import tabulate

from masgent.cli_mode import functions
from masgent.utils import color_print, color_input
from importlib.metadata import version, PackageNotFoundError

def print_banner():
    '''Print the Masgent ASCII banner and metadata inside a box.'''

    # Retrieve installed version
    try:
        pkg_version = version('masgent')
    except PackageNotFoundError:
        pkg_version = 'dev'

    # ASCII banner
    ascii_banner = rf'''
╔═════════════════════════════════════════════════════════════════════════╗
║                                                                         ║
║  ███╗   ███╗  █████╗  ███████╗  ██████╗  ███████╗ ███╗   ██╗ ████████╗  ║
║  ████╗ ████║ ██╔══██╗ ██╔════╝ ██╔════╝  ██╔════╝ ████╗  ██║ ╚══██╔══╝  ║
║  ██╔████╔██║ ███████║ ███████╗ ██║  ███╗ █████╗   ██╔██╗ ██║    ██║     ║
║  ██║╚██╔╝██║ ██╔══██║ ╚════██║ ██║   ██║ ██╔══╝   ██║╚██╗██║    ██║     ║
║  ██║ ╚═╝ ██║ ██║  ██║ ███████║ ╚██████╔╝ ███████╗ ██║ ╚████║    ██║     ║
║  ╚═╝     ╚═╝ ╚═╝  ╚═╝ ╚══════╝  ╚═════╝  ╚══════╝ ╚═╝  ╚═══╝    ╚═╝     ║
║                                                                         ║
║                                   MASGENT: Materials Simulation Agent   ║
║                                      Copyright (c) 2025 Guangchen Liu   ║
║                                                                         ║
║  Version:         {pkg_version:<52}  ║
║  Licensed:        MIT License                                           ║
║  Repository:      https://github.com/aguang5241/masgent                 ║
║  Citation:        Liu, G. et al. (2025), DOI:10.XXXX/XXXXX'             ║
║  Contact:         gliu4@wpi.edu                                         ║
║                                                                         ║
╚═════════════════════════════════════════════════════════════════════════╝
    '''
    color_print(ascii_banner, 'yellow')

def print_entry_message():
    msg = '''
Welcome to Masgent — Your Materials Simulation Agent.

Please select a mode code to proceed:
  0. Density Functional Theory (DFT) Simulations
  1. Machine Learning Potentials (MLP)
  2. Machine Learning Model Training & Evaluation
  3. Data Analysis & Visualization

Global commands:
  ai    —>  Chat with the AI assistant
  back  —>  Switch back to console mode
  help  —>  List all available functions
  exit  —>  Quit the program
    '''
    color_print(msg, 'green')

def print_help():
    title = '\n Masgent - Available Commands and Functions '
    color_print(title, "green")
    headers = ['Code', 'Description']
    rows = [
        ['0', 'Density Functional Theory (DFT) Simulations'],
        ['00', 'Generate VASP POSCAR from chemical formula'],
        ['01', 'Prepare VASP input files (INCAR, KPOINTS, POTCAR)'],
        ['02', 'Prepare HPC job submission script for VASP'],
        ['03', 'Analyze VASP output files'],

        ['1', 'Machine Learning Potentials (MLP)'],
        ['10', 'MACE'],
        ['11', 'CHGNet'],
        ['12', 'SevenNet'],
        ['13', 'Orb-v3'],
        ['14', 'MatterSim'],
        ['15', 'Nequix'],
        ['16', 'PET-MAD'],

        ['2', 'Machine Learning Model Training & Evaluation'],
        ['20', 'Prepare training dataset'],
        ['21', 'Train ML model'],
        ['22', 'Evaluate ML model'],

        ['3', 'Data Analysis & Visualization'],
        ['30', 'Plot material properties'],
        ['31', 'Visualize atomic structures'],
        ['32', 'Statistical analysis'],
    ]
    table = tabulate.tabulate(rows, headers, tablefmt='fancy_grid')
    color_print(table, "green")

def main():
    commands = {
        '0': functions.command_0,
        '1': functions.command_1,
        '2': functions.command_2,
        '3': functions.command_3,
    }

    try:
        while True:
            user_input = color_input('\nMasgent > ', 'yellow').strip().lower()

            if not user_input:
                continue

            if user_input in {'ai'}:
                return 'ai-mode'
            elif user_input in {'back'}:
                return 'cli-mode'
            elif user_input in {'help'}:
                print_help()
            elif user_input in {'exit'}:
                return 'exit-mode'
            elif user_input in commands:
                commands[user_input]()
            else:
                color_print(f'Unknown command: {user_input}', 'green')
                color_print('Type "help" to see available commands.\n', 'green')

    except (KeyboardInterrupt, EOFError):
        color_print('\nExiting Masgent. Goodbye!\n', 'green')
        sys.exit(0)

if __name__ == '__main__':
    main()