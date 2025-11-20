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