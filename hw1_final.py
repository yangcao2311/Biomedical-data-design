#!/usr/bin/env python

import numpy as np
from scipy.optimize import linear_sum_assignment
from num2words import num2words


def KM_solve(patient_pref, doc_cap):
    '''
    Solve patient-doctor assignment problem using Hungarian algorithm (Kuhn-Munkres)
    
    Args:
        patient_pref(dict): It includes the list of the patients' preferences for doctors.
                           e.g. {'patient1': ['doctor1',...], 'patient2': ['doctor3',...]}
        doc_cap(dict): It includes the capacity of each doctor.
                      e.g. {'doctor1': 2, 'doctor2': 3,.....}
    
    Returns:
        Tuple: It includes the allocation and the final score.
        The allocation(dict): e.g. 'patient1' is allocated to 'doctor2'
        The score: int
    '''
    
    ### Data Preparation
    patients = list(patient_pref.keys())  # return every keys from the dictionary that include "keys: values"
    doctors = list(doc_cap.keys())  # another dictionary
    num_patients = len(patients)
    
    # Create doctor positions depends on the capacities of doctors
    doc_cap_slot = []  # Initialize an empty list
    for doc, cap in doc_cap.items():  # for loop go through every set of keys:values in the dictionary, doc is the name of doctor and cap is the value of doctor capacity
        for i in range(cap):  # will cycle based on the current doctor's cap, if the cap is 2, will cycle twice
            doc_cap_slot.append(f'{doc}:{i+1}')  # create a particular position name for doctors, and add them in the list called "doc_cap_slot"
    
    num_doc_capacity = len(doc_cap_slot)
    
    # Make sure the capacity number of doctor is enough
    if num_doc_capacity < num_patients:
        raise ValueError("The capacity of the doctors doesn't satisfy the patients' needs.")
    
    ### Cost matrix
    # Set up the score rule, higher score is better
    max_score = len(doctors)
    
    # Initialize basic matrix. row: patients, column: doctors
    # Initialize cost matrix with high penalty values for unpreferred assignments
    cost_matrix = np.full((num_patients, num_doc_capacity), max_score * 3)
    
    # Fill the cost matrix based on patient preferences
    for i, patient in enumerate(patients):  # browse each patients, with number and patients name
        pref = patient_pref[patient]
        for j, doc in enumerate(doc_cap_slot):
            doc_name = doc.split(':')[0]
            try:
                rank = pref.index(doc_name)  # find this doctor in the rank of patient's preference
                score = max_score - rank
                cost = max_score - score
                cost_matrix[i][j] = cost
            except ValueError:  # if the doctor not in the preference list, will return a large number
                pass
    
    ### Optimization
    # The Hungarian algorithm in the Scipy library is specifically designed to solve the assignment problem
    row_index, col_index = linear_sum_assignment(cost_matrix)
    
    # Initialize results
    final_score = 0
    assignment = {doc: [] for doc in doctors}  # browse each doctor's name and create a key for each doctor
    
    print("\n--- Allocation Process ---")
    for i in range(len(patients)):
        patient_index = row_index[i]
        doc_index = col_index[i]  # make sure one patient for one doctor
        
        patient = patients[patient_index]
        doctor_slot = doc_cap_slot[doc_index]
        doc_name = doctor_slot.split(':')[0]
        
        # Add the patient to the corresponding doctor list
        assignment[doc_name].append(patient)
        
        # Calculate the score
        cost = cost_matrix[patient_index][doc_index]
        score = max_score - cost
        final_score += score
        
        # Find the position of doctor in the preference list
        rank = patient_pref[patient].index(doc_name) + 1
        rank_ordinal = num2words(rank, to='ordinal')
        
        print(f"Assign patient '{patient}' to doctor '{doc_name}' (the {rank_ordinal} choice, score: {score})")
    
    return final_score, assignment


# --- Data example ---
# Each patient has individual preference list
patient_pref = {
    'Sam': ['Doctor1', 'Doctor3', 'Doctor4', 'Doctor2'],
    'Tom': ['Doctor2', 'Doctor1', 'Doctor3', 'Doctor4'],
    'Stella': ['Doctor1', 'Doctor4', 'Doctor2', 'Doctor3'],
    'Tim': ['Doctor1', 'Doctor4', 'Doctor3', 'Doctor2'],
    'David': ['Doctor3', 'Doctor2', 'Doctor1', 'Doctor4'],
}

doctor_capacity = {
    'Doctor1': 1,
    'Doctor2': 1,
    'Doctor3': 1,
    'Doctor4': 2,
}

# --- Run the algorithm and print the results ---
score, assignment = KM_solve(patient_pref, doctor_capacity)

print("\n--- Final allocation results ---")
for doctor, patient in assignment.items():
    print(f'{doctor} (Capacity: {doctor_capacity[doctor]}): {", ".join(patient) if patient else "none"}')

print(f'\nTotal patient satisfaction score: {score}')
