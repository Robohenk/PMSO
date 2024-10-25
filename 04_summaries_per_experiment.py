# -*- coding: utf-8 -*-
"""
Created on October 25 2024
@author: Rob Bemthuis

Script: 04_summaries_per_experiment.py
Purpose: This script consolidates metrics and cycle time data from multiple experiments and runs, generating a summary 
         file for each experiment. The summary includes metrics and cycle times per run.
Inputs: Text files for metrics and cycle times, organized by experiment and run in two separate directories.
Outputs: A summary text file per experiment, aggregating relevant metrics and cycle times for each run, saved in 
         an output directory.
"""

import os

# Directories for the input files
metrics_dir = "04_process_discovery_conformance"
cycle_time_dir = "03_event_log_KPIs"
output_dir = "05_summaries_per_experiment"

# Create the output directory if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Number of experiments and runs
num_experiments = 27
num_runs = 20

# Process each experiment
for exp in range(1, num_experiments + 1):
    # Create a new file for each experiment
    output_file_path = os.path.join(output_dir, f"Exp{exp}_summary.txt")
    
    with open(output_file_path, 'w') as output_file:
        output_file.write(f"Experiment {exp} Overview\n")
        output_file.write("=" * 50 + "\n")
        
        # Process each run
        for run in range(1, num_runs + 1):
            # File names for metrics and cycle time
            metrics_file = os.path.join(metrics_dir, f"Exp{exp}Run{run}_metrics.txt")
            cycle_time_file = os.path.join(cycle_time_dir, f"Exp{exp}Run{run}.txt")
            
            output_file.write(f"Run {run}:\n")
            
            # Extract and write the metrics data
            if os.path.exists(metrics_file):
                with open(metrics_file, 'r') as mf:
                    metrics_data = mf.read().strip()
                    output_file.write("Metrics:\n")
                    output_file.write(metrics_data + "\n")
            else:
                output_file.write("Metrics: File not found\n")
            
            # Extract and write the product cycle time data
            if os.path.exists(cycle_time_file):
                with open(cycle_time_file, 'r') as cf:
                    cycle_time_data = cf.readline().strip()
                    output_file.write("Product Cycle Time:\n")
                    output_file.write(cycle_time_data + "\n")
            else:
                output_file.write("Product Cycle Time: File not found\n")
            
            output_file.write("-" * 50 + "\n")

print("Summary files generated in the 'final' directory.")
