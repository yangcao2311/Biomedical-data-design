# Biomedical-data-design
Project1: Coding a Rank-order Assignment Algorithm

Member:
CAO Yang: ycao95@jh.edu /
XU Chaohui: cxu86@jh.edu /
GUO Yiting: yguo140@jh.edu

A Python implementation of an optimal patient-doctor assignment system using the Hungarian Algorithm (Kuhn-Munkres Algorithm) to maximize patient satisfaction while respecting doctor capacity constraints.

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Algorithm Description](#algorithm-description)
- [Experimental Setup](#experimental-setup)
- [Design Decisions and Model Assumptions](#design-decisions-and-model-assumptions)
- [Usage](#usage)
- [Example Output](#example-output)
- [Team Contributions](#team-contributions)

## Overview

This system solves the assignment problem of matching patients to doctors based on patient preferences while considering doctor capacity limits. The goal is to maximize overall patient satisfaction by assigning patients to their most preferred available doctors.

## Installation

### Required Packages

Install the following Python packages before running the code:

```bash
pip install numpy scipy num2words
```

### Package Details:
- **numpy**: For matrix operations and numerical computations
- **scipy**: Provides the `linear_sum_assignment` function implementing the Hungarian algorithm
- **num2words**: Converts numerical rankings to ordinal words (e.g., "1" to "first")

### Alternative Installation:
You can also install all dependencies at once:
```bash
pip install -r requirements.txt
```

## Algorithm Description

### Hungarian Algorithm (Kuhn-Munkres Algorithm)

The system uses the **Hungarian Algorithm**, a combinatorial optimization algorithm that solves the assignment problem in polynomial time O(n³). 

**Key Features:**
- **Optimal Solution**: Guarantees the globally optimal assignment that maximizes total satisfaction
- **Bipartite Matching**: Efficiently handles one-to-one matching between patients and doctor slots
- **Cost Matrix Based**: Transforms preference rankings into a cost minimization problem

**Algorithm Steps:**
1. **Data Preparation**: Convert doctor capacities into individual slots
2. **Cost Matrix Construction**: Transform patient preferences into numerical costs
3. **Optimization**: Apply Hungarian algorithm to find optimal assignment
4. **Result Processing**: Convert algorithmic output back to human-readable assignments

## Experimental Setup

### Input Format

**Patient Preferences:**
```python
patient_pref = {
    'Patient_Name': ['Doctor1', 'Doctor2', 'Doctor3', ...],  # Ordered by preference
    # ... more patients
}
```

**Doctor Capacities:**
```python
doc_cap = {
    'Doctor_Name': capacity_number,  # Number of patients each doctor can handle
    # ... more doctors
}
```

### Scoring System

- **Preference Ranking**: Higher preference = Higher score
- **Score Calculation**: `score = max_doctors - preference_rank`
- **Cost Transformation**: `cost = max_doctors - score`
- **Penalty**: Unranked doctors receive high penalty costs

## Design Decisions and Model Assumptions

### Core Assumptions

1. **Complete Preferences**: Each patient provides a complete ranking of all available doctors
2. **Fixed Capacities**: Doctor capacities are predetermined and cannot be exceeded
3. **Availability**: All doctors are available for assignment during the scheduling period

### Design Decisions

1. **Slot-Based Modeling**: 
   - Each doctor capacity is decomposed into individual slots
   - Enables proper handling of multi-patient assignments per doctor
   - Example: Doctor with capacity 2 → `['Doctor:1', 'Doctor:2']`

2. **Cost Matrix Design**:
   - Lower costs represent more preferred assignments
   - Penalty system for unranked preferences prevents infeasible assignments
   - Matrix size: `num_patients × total_doctor_slots`

3. **Optimization Objective**:
   - Maximize total patient satisfaction score
   - Equivalent to minimizing total assignment cost

4. **Error Handling**:
   - Validates that total doctor capacity ≥ number of patients

## Usage

```python
from patient_doctor_assignment import KM_solve

# Define patient preferences and doctor capacities
patient_pref = {
    'Sam': ['doctor1', 'doctor3', 'doctor4', 'doctor2'],
    'Tom': ['doctor2', 'doctor1', 'doctor3', 'doctor4'],
    # ... more patients
}

doctor_capacity = {
    'doctor1': 1,
    'doctor2': 1,
    'doctor3': 1,
    'doctor4': 2,
}

# Solve the assignment problem
final_score, assignments = KM_solve(patient_pref, doctor_capacity)

# Results are automatically printed during execution
```

## Example Output

```
--- Allocation Process ---
Assign patient 'Sam' to doctor 'doctor1' (the first choice, grade: 4)
Assign patient 'Tom' to doctor 'doctor2' (the first choice, grade: 4)
Assign patient 'Stella' to doctor 'doctor4' (the second choice, grade: 3)
Assign patient 'Tim' to doctor 'doctor4' (the second choice, grade: 3)
Assign patient 'David' to doctor 'doctor3' (the first choice, grade: 4)

--- Final allocation results ---
doctor1 (Capacity: 1): Sam
doctor2 (Capacity: 1): Tom
doctor3 (Capacity: 1): David
doctor4 (Capacity: 2): Stella, Tim

Total patient satisfaction score: 18
```

## Team Contributions

### Yang Cao
- **Algorithm Design**: Designed the overall system architecture and optimization approach
- **Core Implementation**: Developed the main `KM_solve` function and Hungarian algorithm integration

### Chaohui Xu
- **Code Development**: Implemented data preprocessing and result processing modules
- **Documentation**: Added comprehensive inline comments and code documentation

### Yiting Guo
- **Literature Review**: Conducted research on assignment algorithms and optimization methods
- **Algorithm Analysis**: Provided theoretical background and performance analysis of the Hungarian algorithm
