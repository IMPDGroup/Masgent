# masgent/utils.py

import os
from importlib.metadata import version, PackageNotFoundError

def os_path_setup():
    '''Set up base and target directories for VASP input files.'''
    base_dir = os.getcwd()
    runs_dir = os.path.join(base_dir, 'masgent_runs')
    output_dir = os.path.join(base_dir, 'masgent_outputs')
    return base_dir, runs_dir, output_dir

def print_title():
    '''Print the Masgent ASCII banner and metadata inside a box.'''

    # Retrieve installed version
    try:
        pkg_version = version('masgent')
    except PackageNotFoundError:
        pkg_version = 'dev'

    # ASCII banner
    ascii_banner = rf'''
+---------------------------------------------------------------------------+
|                                                                           |
|   ███╗   ███╗  █████╗  ███████╗  ██████╗  ███████╗ ███╗   ██╗ ████████╗   |
|   ████╗ ████║ ██╔══██╗ ██╔════╝ ██╔════╝  ██╔════╝ ████╗  ██║ ╚══██╔══╝   |
|   ██╔████╔██║ ███████║ ███████╗ ██║  ███╗ █████╗   ██╔██╗ ██║    ██║      |
|   ██║╚██╔╝██║ ██╔══██║ ╚════██║ ██║   ██║ ██╔══╝   ██║╚██╗██║    ██║      |
|   ██║ ╚═╝ ██║ ██║  ██║ ███████║ ╚██████╔╝ ███████╗ ██║ ╚████║    ██║      |
|   ╚═╝     ╚═╝ ╚═╝  ╚═╝ ╚══════╝  ╚═════╝  ╚══════╝ ╚═╝  ╚═══╝    ╚═╝      |
|                            A Materials Simulation AI Agent Framework      |
|                                               (c) 2025 Guangchen Liu      |
|   Version:         {pkg_version:<53}  |
|   Licensed:        MIT License                                            |
|   Repository:      https://github.com/aguang5241/masgent                  |
|   Citation:        Liu, G. et al. (2025), DOI:10.XXXX/XXXXX'              |
|   Contact:         gliu4@wpi.edu                                          |
|                                                                           |
+---------------------------------------------------------------------------+
    '''
    print(ascii_banner)