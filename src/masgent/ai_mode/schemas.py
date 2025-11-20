# masgent/ai_mode/schemas.py

import os, re

from pymatgen.core.periodic_table import Element

from pydantic import BaseModel, Field, model_validator
from typing import Literal, Optional

class GenerateVaspPoscarSchema(BaseModel):
    '''
    Schema for generating VASP POSCAR file from user inputs or from Materials Project database.
    '''

    formula: str = Field(..., description='Chemical formula, e.g., Cu, NaCl, MgO')

    @model_validator(mode="after")
    def validator(self):
        # ensure formula is valid
        matches = re.findall(r'([A-Z][a-z]?)(\d*)', self.formula)
        valid = True
        for elem, num in matches:
            try:
                Element(elem)  # will fail for invalid elements
            except:
                valid = False
                break

        if not valid:
            raise ValueError(f'Invalid chemical formula: {self.formula}')

        return self
    
class ConvertStructureFormatSchema(BaseModel):
    '''
    Schema for converting structure files between different formats (CIF, POSCAR, XYZ).
    '''
    input_path: str = Field(
        ...,
        description='Path to the input structure file. Must exist.'
    )

    input_format: Literal[
        'POSCAR', 'CIF', 'XYZ'
        ] = Field(
            ...,
            description='Format of the input structure file. Must be one of POSCAR, CIF, or XYZ.'
        )
    
    output_format: Literal[
        'POSCAR', 'CIF', 'XYZ'
        ] = Field(
            ...,
            description='Desired format of the output structure file. Must be one of POSCAR, CIF, or XYZ.'
        )

    @model_validator(mode='after')
    def validator(self):
        # ensure input file exists
        if not os.path.isfile(self.input_path):
            raise ValueError(f'Input structure file not found: {self.input_path}')
        # ensure input_format and output_format are not the same
        if self.input_format == self.output_format:
            raise ValueError('Input format and output format must be different.')

        return self
    
class ConvertPoscarCoordinatesSchema(BaseModel):
    '''
    Schema for converting POSCAR between direct and cartesian coordinates.
    '''
    poscar_path: str = Field(
        ...,
        description='Path to the POSCAR file. Must exist.'
    )

    to_cartesian: bool = Field(
        ...,
        description='If True, convert to cartesian coordinates; if False, convert to direct coordinates.'
    )

    @model_validator(mode='after')
    def validator(self):
        # ensure POSCAR exists
        if not os.path.isfile(self.poscar_path):
            raise ValueError(f'POSCAR file not found: {self.poscar_path}')

        return self
    
class GenerateVaspInputsFromPoscar(BaseModel):
    '''
    Schema for generating VASP input files (INCAR, KPOINTS, POTCAR) from POSCAR using pymatgen input sets.
    '''
    poscar_path: str = Field(
        ...,
        description='Path to POSCAR file. Must exist.'
    )

    vasp_input_sets: Literal[
        'MPRelaxSet', 'MPStaticSet', 'MPNonSCFSet',
        'MPScanRelaxSet', 'MPScanStaticSet', 'MPMDSet'
        ] = Field(
            ...,
            description='Type of Pymatgen VASP input set class to use. Must be one of the supported types.'
        )

    @model_validator(mode='after')
    def validator(self):
        # ensure POSCAR exists
        if not os.path.isfile(self.poscar_path):
            raise ValueError(f'POSCAR file not found: {self.poscar_path}')

        return self

class CustomizeVaspKpointsWithAccuracy(BaseModel):
    '''
    Schema for customizing VASP KPOINTS from POSCAR with specified accuracy level.
    '''
    poscar_path: str = Field(
        ...,
        description='Path to POSCAR file. Must exist.'
    )

    accuracy_level: Literal[
        'Low', 'Medium', 'High'
        ] = Field(
            ...,
            description='Type of accuracy level for KPOINTS generation. Must be one of Low, Medium, or High.'
        )

    @model_validator(mode='after')
    def validator(self):
        # ensure POSCAR exists
        if not os.path.isfile(self.poscar_path):
            raise ValueError(f'POSCAR file not found: {self.poscar_path}')
        # ensure accuracy_level is valid
        if self.accuracy_level not in {'Low', 'Medium', 'High'}:
            raise ValueError(f'Invalid accuracy_level: {self.accuracy_level}. Must be one of Low, Medium, or High.')

        return self