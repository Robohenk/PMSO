# -*- coding: utf-8 -*-
"""
Created on October 25 2024
@author: Rob Bemthuis

Script: 05_combined_summaries.py
Purpose: This script consolidates summary data from multiple experiments by extracting relevant metrics such as 
         precision and average product cycle time from experiment summaries. It then compiles these metrics into 
         a single overview file.
Inputs: Text summary files, organized by experiment, containing metrics and cycle time data.
Outputs: A combined text file that consolidates all experiment results, highlighting metrics for each run across 
         experiments, saved in a specified output directory.
"""

import os
import re

# Directory containing the summary files
final_dir = "05_summaries_per_experiment"
output_file_path = os.path.join(final_dir, "combined_results.txt")

# Regular expressions to extract precision and cycle time
precision_pattern = re.compile(r"Precision \(Token-Based Replay\): ([0-9.]+)")
cycle_time_pattern = re.compile(r"Average Product Cycle Time: ([0-9.]+) seconds")

# Initialize a list to hold all results
results = []

# Number of experiments and runs
num_experiments = 27
num_runs = 20

# Iterate over each experiment
for exp in range(1, num_experiments + 1):
    summary_file_path = os.path.join(final_dir, f"Exp{exp}_summary.txt")
    
    if not os.path.exists(summary_file_path):
        print(f"Summary file for Experiment {exp} not found.")
        continue  # Skip to the next experiment if the file is missing
    
    with open(summary_file_path, 'r') as summary_file:
        content = summary_file.read()
    
    # Split the content by runs using the separator lines
    runs_data = content.split("-" * 50 + "\n")
    
    for run_data in runs_data:
        # Extract run number
        run_match = re.search(r"Run (\d+):", run_data)
        if not run_match:
            continue  # Skip if run number is not found
        run_number = int(run_match.group(1))
        
        # Extract precision
        precision_match = precision_pattern.search(run_data)
        if precision_match:
            precision = precision_match.group(1)
        else:
            precision = "N/A"
        
        # Extract average product cycle time
        cycle_time_match = cycle_time_pattern.search(run_data)
        if cycle_time_match:
            cycle_time = cycle_time_match.group(1)
        else:
            cycle_time = "N/A"
        
        # Append the extracted data to results
        results.append(f"{exp};{run_number};{precision};{cycle_time}")

# Write all results to the output file
with open(output_file_path, 'w') as output_file:
    # Write header
    output_file.write("Experiment;Run;Precision;Average_Product_Cycle_Time_Seconds\n")
    for line in results:
        output_file.write(line + "\n")

print(f"Combined results have been written to '{output_file_path}'.")
