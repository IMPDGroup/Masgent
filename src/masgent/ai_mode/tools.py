# masgent/ai_mode/tools.py

import os, warnings, datetime
from ase.io import read, write
from pymatgen.core import Structure
from pymatgen.io.vasp.sets import MPStaticSet, MPRelaxSet, MPNonSCFSet, MPScanRelaxSet, MPScanStaticSet, MPMDSet, Kpoints
from pymatgen.io.vasp import Poscar
from mp_api.client import MPRester

from masgent.utils import os_path_setup
from masgent.ai_mode.schemas import GenerateVaspPoscarSchema, ConvertStructureFormatSchema, ConvertPoscarCoordinatesSchema, GenerateVaspInputsFromPoscar, CustomizeVaspKpointsWithAccuracy

# Do not show warnings
warnings.filterwarnings('ignore')

def generate_vasp_poscar(input: GenerateVaspPoscarSchema) -> str:
    '''
    Generate VASP POSCAR file from user inputs or from Materials Project database.
    '''
    print(f'[Debug: Function Calling] generate_vasp_poscar with input: {input}')
    
    formula = input.formula

    try:
        base_dir, runs_dir, output_dir = os_path_setup()
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        runs_timestamp_dir = os.path.join(runs_dir, f'runs_{timestamp}')
        os.makedirs(runs_timestamp_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        
        with MPRester() as mpr:
            docs = mpr.materials.summary.search(formula=formula)
            if not docs:
                return f'\nNo materials found in Materials Project database for formula: {formula}'
            
            mid = docs[0].material_id   # pick the first match
            structure = mpr.get_structure_by_material_id(mid)
            poscar = Poscar(structure)

        # Write POSCAR file to the timestamped run directory
        poscar.write_file(os.path.join(runs_timestamp_dir, 'POSCAR'), direct=True)
        # Also write to the main target directory for easy access
        poscar.write_file(os.path.join(output_dir, 'POSCAR'), direct=True)

        return f'\nUpdated POSCAR in {output_dir}.'

    except Exception as e:
        return f'\nPOSCAR generation failed: {str(e)}'
    
def generate_vasp_inputs_from_poscar(input: GenerateVaspInputsFromPoscar) -> str:
    '''
    Generate VASP input files (INCAR, KPOINTS, POTCAR) using pymatgen input sets.
    '''
    print(f'[Debug: Function Calling] generate_vasp_inputs_from_poscar with input: {input}')
    
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
        vis.kpoints.write_file(os.path.join(output_dir, 'KPOINTS'))
        vis.potcar.write_file(os.path.join(output_dir, 'POTCAR'))
        
        return f'\nUpdated VASP input files based on {vasp_input_sets} in {output_dir}.'
    
    except Exception as e:
        return f'\nVASP input files generation failed: {str(e)}'
    
def convert_structure_format(input: ConvertStructureFormatSchema) -> str:
    '''
    Convert structure files between different formats (CIF, POSCAR, XYZ).
    '''
    print(f'[Debug: Function Calling] convert_structure_format with input: {input}')
    
    input_path = input.input_path
    input_format = input.input_format
    output_format = input.output_format
    
    format_map = {
        "POSCAR": "vasp",
        "CIF": "cif",
        "XYZ": "xyz"
    }

    try:
        base_dir, runs_dir, output_dir = os_path_setup()
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        runs_timestamp_dir = os.path.join(runs_dir, f'runs_{timestamp}')
        os.makedirs(runs_timestamp_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        
        atoms = read(input_path, format=format_map[input_format])
        filename_wo_ext = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(output_dir, f'{filename_wo_ext}.{output_format.lower()}')
        write(output_path, atoms, format=format_map[output_format])

        return f'\nConverted structure saved to {output_path}.'
    
    except Exception as e:
        return f'\nStructure conversion failed: {str(e)}'
    
def convert_poscar_coordinates(input: ConvertPoscarCoordinatesSchema) -> str:
    '''
    Convert POSCAR between direct and cartesian coordinates.
    '''
    print(f'[Debug: Function Calling] convert_poscar_coordinates with input: {input}')
    
    poscar_path = input.poscar_path
    to_cartesian = input.to_cartesian

    try:
        base_dir, runs_dir, output_dir = os_path_setup()
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        runs_timestamp_dir = os.path.join(runs_dir, f'runs_{timestamp}')
        os.makedirs(runs_timestamp_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        
        structure = Structure.from_file(poscar_path)
        poscar = Poscar(structure)

        # Write converted POSCAR to the timestamped run directory
        poscar.write_file(os.path.join(runs_timestamp_dir, 'POSCAR'), direct=not to_cartesian)
        # Also write to the main target directory for easy access
        poscar.write_file(os.path.join(output_dir, 'POSCAR'), direct=not to_cartesian)

        coord_type = 'Cartesian' if to_cartesian else 'Direct'
        return f'\nConverted POSCAR to {coord_type} coordinates in {output_dir}.'

    except Exception as e:
        return f'\nPOSCAR coordinate conversion failed: {str(e)}'
    
def customize_vasp_kpoints_with_accuracy(input: CustomizeVaspKpointsWithAccuracy) -> str:
    '''
    Customize VASP KPOINTS from POSCAR with specified accuracy level.
    '''
    print(f'[Debug: Function Calling] customize_vasp_kpoints_with_accuracy with input: {input}')
    
    poscar_path = input.poscar_path
    accuracy_level = input.accuracy_level
    
    DENSITY_MAP = {
        'Low': 1000,
        'Medium': 3000,
        'High': 5000,
    }
    kppa = DENSITY_MAP[accuracy_level]

    try:
        base_dir, runs_dir, output_dir = os_path_setup()
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        runs_timestamp_dir = os.path.join(runs_dir, f'runs_{timestamp}')
        os.makedirs(runs_timestamp_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        
        structure = Structure.from_file(poscar_path)
        kpoints = Kpoints.automatic_density(structure, kppa=kppa)

        # Write KPOINTS to the timestamped run directory
        kpoints.write_file(os.path.join(runs_timestamp_dir, 'KPOINTS'))
        # Also write to the main target directory for easy access
        kpoints.write_file(os.path.join(output_dir, 'KPOINTS'))
        
        return f'\nUpdated KPOINTS with {accuracy_level} accuracy in {output_dir}.'

    except Exception as e:
        return f'\nVASP KPOINTS generation failed: {str(e)}'