import os
import warnings
from ase.build import bulk
from ase.io import write
from ase.data import chemical_symbols
from pymatgen.core import Structure
from pymatgen.io.vasp.sets import MPRelaxSet

from pydantic_ai import Tool

from vasp_agent.utils import os_path_setup

# Do not show warnings
warnings.filterwarnings('ignore')

@Tool
def generate_simple_poscar(
        name: str = 'Cu',
        crystalstructure: str = 'fcc',
        a: float = 3.5,
    ) -> str:
    '''Generate simple bulk POSCARs (sc, fcc, bcc, hcp) for testing or VASP input.

    name: str
        Single chemical symbol of the element, e.g., 'Si', 'Cu', 'Fe', 'Mg'
    crystalstructure: str
        Must be one of sc, fcc, bcc, hcp
    a: float
        Lattice constant in Angstroms
    '''
    print(f'[Function Calling: generate_simple_POSCAR] Generating {crystalstructure} {name} POSCAR with a={a} Angstroms...')

    # Set up directories
    target_dir = os_path_setup()[1]
    os.makedirs(target_dir, exist_ok=True)

    # Validate element, if not valid, set it to 'Cu' by default
    if name not in chemical_symbols:
        name = 'Cu'

    # Generate bulk structure and write POSCAR
    atoms = bulk(name=name, crystalstructure=crystalstructure, a=a)
    write(os.path.join(target_dir, 'POSCAR'), atoms, format='vasp')

    return f'Generated {crystalstructure} {name} POSCAR with a={a} Angstroms and saved to {target_dir}/POSCAR.'

@Tool
def generate_vasp_inputs_from_poscar() -> str:
    '''Generate standard VASP input files using pymatgen's MPRelaxSet from an existing POSCAR file in the base directory.
    '''
    print(f'[Function Calling: generate_vasp_inputs_from_poscar] Generating VASP input files from POSCAR...')
    base_dir, target_dir = os_path_setup()

    if not os.path.exists(os.path.join(target_dir, 'POSCAR')):
        return f'No POSCAR file found in {target_dir}. Please provide a valid POSCAR file first or let the AI generate one for you.'

    structure = Structure.from_file(os.path.join(target_dir, 'POSCAR'))
    vis = MPRelaxSet(structure)

    os.makedirs(target_dir, exist_ok=True)
    vis.write_input(target_dir)

    return f'Generated VASP input files (INCAR, KPOINTS, POTCAR) from POSCAR and saved to {target_dir}.'

