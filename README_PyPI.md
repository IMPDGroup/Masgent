# Masgent
Masgent: Materials Simulation Agent

## Overview
Masgent is a materials simulation AI agent that streamlines DFT workflows and analysis, fast MLP-based simulations, and simple ML modeling for materials science. With automated tools for structure handling, VASP setup, and rapid property prediction, Masgent simplifies complex simulation workflows and boosts productivity for both researchers and students.

## Features
1. Density Functional Theory (DFT) Simulations
  - 1.1 Structure Preparation & Manipulation
    - 1.1.1 Generate POSCAR from chemical formula
    - 1.1.2 Convert POSCAR coordinates (Direct <-> Cartesian)
    - 1.1.3 Convert structure file formats (CIF, POSCAR, XYZ)
    - 1.1.4 Generate structures with defects (Vacancies, Substitutions, Interstitials with Voronoi)
    - 1.1.5 Generate supercells
    - 1.1.6 Generate Special Quasirandom Structures (SQS)
    - 1.1.7 Generate surface slabs
    - 1.1.8 Generate interface structures
  
  - 1.2 VASP Input File Preparation
    - 1.2.1 Prepare full VASP input files (INCAR, KPOINTS, POTCAR, POSCAR)
    - 1.2.2 Generate INCAR templates (relaxation, static, etc.)
    - 1.2.3 Generate KPOINTS with specified accuracy
    - 1.2.4 Generate HPC job submission script
  
  - 1.3 Standard VASP Workflows Preparation
    - 1.3.1 Convergence test (ENCUT, KPOINTS)
    - 1.3.2 Equation of State (EOS)
    - 1.3.3 Elastic constants calculations
    - 1.3.4 Ab-initio Molecular Dynamics (AIMD)
    - 1.3.5 Nudged Elastic Band (NEB) calculations
  
  - 1.4 (Planned) Workflow Output Analysis
    - 1.4.1 (Planned) Convergence test analysis
    - 1.4.2 (Planned) Equation of State (EOS) analysis
    - 1.4.3 (Planned) Elastic constants analysis 
    - 1.4.4 (Planned) Ab-initio Molecular Dynamics (AIMD) analysis
    - 1.4.5 (Planned) Nudged Elastic Band (NEB) analysis

2. Fast Simulations Using Machine Learning Potentials (MLPs)
  - Supported MLPs:
    - 2.1 SevenNet
    - 2.2 CHGNet
    - 2.3 Orb-v3
    - 2.4 MatSim
  - Implemented Simulations for all MLPs:
    - Single Point Energy Calculation
    - Equation of State (EOS) Calculation
    - Elastic Constants Calculation
    - Molecular Dynamics Simulation (NVT)

3. (Planned) Simple Machine Learning for Materials Science
  - 3.1 (Planned) Data Preparation & Feature Engineering
  - 3.2 (Planned) Model Design & Hyperparameter Tuning
  - 3.3 (Planned) Model Training & Evaluation

## Installation
1. Requirements:
   - Python >= 3.11, < 3.14
2. Optional requirements:
   - For AI functionalities: get your OpenAI API key from [platform.openai.com](https://platform.openai.com/account/api-keys)
   - For Materials Project access: get your Materials Project API key from [materialsproject.org](https://next-gen.materialsproject.org/api)
3. Install via pip:
  ```bash
  pip install -U masgent
  ```

## Usage
- After installation, run the following command to start the Masgent:
  ```bash
  masgent
  ```

## Issues and Suggestions
If you encounter any issues or have suggestions for improvements, please open an issue on our [GitHub issues](https://github.com/aguang5241/masgent/issues).

## Cite Us
If you use Masgent in your research, please cite the following reference:
```
@article{
  title={Masgent: A Materials Simulation Agent},
  journal={},
  volume={},
  pages={},
  year={},
  issn={},
  doi={},
}
```