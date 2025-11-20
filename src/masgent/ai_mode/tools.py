# masgent/ai_mode/tools.py

import os, warnings, datetime
from ase.build import bulk
from ase.io import write
from pymatgen.core import Structure
from pymatgen.io.vasp.sets import MPStaticSet, MPRelaxSet, MPNonSCFSet, MPScanRelaxSet, MPScanStaticSet, MPMDSet

from masgent.utils import os_path_setup
from masgent.ai_mode.schemas import GenerateSimplePOSCARSchema, GenerateIncarFromPoscar

# Do not show warnings
warnings.filterwarnings('ignore')

def generate_simple_poscar(input: GenerateSimplePOSCARSchema) -> str:
    '''Creating a simple bulk POSCAR
    '''
    print(f'[Debug: Function Calling] generate_simple_poscar with input: {input}')

    name = input.name
    crystalstructure   = input.crystalstructure
    a    = input.a
    b    = input.b
    c    = input.c
    alpha = input.alpha

    try:
        base_dir, runs_dir, output_dir = os_path_setup()
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        runs_timestamp_dir = os.path.join(runs_dir, f'runs_{timestamp}')
        os.makedirs(runs_timestamp_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)

        atoms = bulk(
            name=name,
            crystalstructure=crystalstructure,
            a=a,
            b=b,
            c=c,
            alpha=alpha,
        )

        # Write POSCAR file to the timestamped run directory
        write(os.path.join(runs_timestamp_dir, 'POSCAR'), atoms, format='vasp', direct=True)
        # Also write to the main target directory for easy access
        write(os.path.join(output_dir, 'POSCAR'), atoms, format='vasp', direct=True)

        return f'\nUpdated POSCAR in {output_dir}.'

    except Exception as e:
        return f'\nPOSCAR generation failed: {str(e)}'
    
def generate_incar_from_poscar(input: GenerateIncarFromPoscar) -> str:
    '''Generate VASP INCAR (and optionally other inputs) using pymatgen input sets.
    '''
    print(f'[Debug: Function Calling] generate_incar_from_poscar with input: {input}')
    
    poscar_path = input.poscar_path
    vasp_input_sets = input.vasp_input_sets

    VIS_MAP = {
        'MPRelaxSet': MPRelaxSet,
        'MPStaticSet': MPStaticSet,
        'MPNonSCFSet': MPNonSCFSet,
        'MPScanRelaxSet': MPScanRelaxSet,
        'MPScanStaticSet': MPScanStaticSet,
        'MPMDSet': MPMDSet,
    }
    vis_class = VIS_MAP[vasp_input_sets]

    try:
        base_dir, runs_dir, output_dir = os_path_setup()
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        runs_timestamp_dir = os.path.join(runs_dir, f'runs_{timestamp}')
        os.makedirs(runs_timestamp_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        
        structure = Structure.from_file(poscar_path)
        vis = vis_class(structure)

        # Write INCAR and POSCAR to the timestamped run directory
        vis.incar.write_file(os.path.join(runs_timestamp_dir, 'INCAR'))
        vis.poscar.write_file(os.path.join(runs_timestamp_dir, 'POSCAR'), direct=True)
        # Also write to the main target directory for easy access
        vis.incar.write_file(os.path.join(output_dir, 'INCAR'))
        vis.poscar.write_file(os.path.join(output_dir, 'POSCAR'), direct=True)
        
        return f'\nUpdated INCAR based on {vasp_input_sets} in {output_dir}.'
    
    except Exception as e:
        return f'\nVASP INCAR generation failed: {str(e)}'


