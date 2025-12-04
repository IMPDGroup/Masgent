# Masgent
Masgent: Materials Simulation Agent

## Demos
### Basic Usage:  
<div align=left><img src='./res/basic_sm.gif' alt='Basic Usage' width='800'/></div>

### AI Agent:  
<div align=left><img src='./res/ai_sm.gif' alt='AI Agent' width='800'/></div>

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
2. Install via pip:
  ```bash
  pip install -U masgent
  ```

## Usage
1. After installation, run the following command to start the Masgent:
  ```bash
  masgent
  ```
2. Optional preparation:
  - For AI functionalities, obtain your OpenAI API key from [platform.openai.com](https://platform.openai.com/account/api-keys).
  - For Materials Project access, obtain your API key from [materialsproject.org](https://next-gen.materialsproject.org/api).
