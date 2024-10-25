# -*- coding: utf-8 -*-
"""
Created on October 25 2024
@author: Rob Bemthuis

Script: 06_combined_summaries_with_stats.py
Purpose: This script aggregates and calculates cumulative statistics, including average and standard deviation, 
         for precision and product cycle times across multiple experiments. It builds on previously summarized 
         results and provides statistical insights across all runs.
Inputs: Text summary files from previous experiments, containing precision and cycle time metrics.
Outputs: A comprehensive text file that combines metrics with cumulative statistics, providing enhanced insights 
         across experiments, saved in an output directory.
"""

import os
import re
import statistics

# Directory containing the summary files
final_dir = "05_summaries_per_experiment"
output_file_path = os.path.join(final_dir, "combined_results_with_stats.txt")

# Regular expressions to extract precision and cycle time
precision_pattern = re.compile(r"Precision \(Token-Based Replay\): ([0-9.]+)")
cycle_time_pattern = re.compile(r"Average Product Cycle Time: ([0-9.]+) seconds")

# Number of experiments and runs
num_experiments = 27
num_runs = 20

# Open the output file
with open(output_file_path, 'w') as output_file:
    # Write header
    output_file.write("Experiment_Run;Precision;Average_Product_Cycle_Time_Seconds;Cumulative_Average_Precision;Cumulative_StdDev_Precision;Cumulative_Average_Cycle_Time;Cumulative_StdDev_Cycle_Time\n")

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
        
        # Initialize lists for cumulative statistics
        precisions = []
        cycle_times = []
        
        for run_data in runs_data:
            # Extract run number
            run_match = re.search(r"Run (\d+):", run_data)
            if not run_match:
                continue  # Skip if run number is not found
            run_number = int(run_match.group(1))
            
            # Extract precision
            precision_match = precision_pattern.search(run_data)
            if precision_match:
                precision = float(precision_match.group(1))
                precisions.append(precision)
            else:
                precision = "N/A"
            
            # Extract average product cycle time
            cycle_time_match = cycle_time_pattern.search(run_data)
            if cycle_time_match:
                cycle_time = float(cycle_time_match.group(1))
                cycle_times.append(cycle_time)
            else:
                cycle_time = "N/A"
            
            # Compute cumulative averages and standard deviations
            if precisions and precision != "N/A":
                cum_avg_precision = sum(precisions) / len(precisions)
                if len(precisions) > 1:
                    cum_stddev_precision = statistics.stdev(precisions)
                else:
                    cum_stddev_precision = 0.0  # Standard deviation with one value is zero
            else:
                cum_avg_precision = "N/A"
                cum_stddev_precision = "N/A"
            
            if cycle_times and cycle_time != "N/A":
                cum_avg_cycle_time = sum(cycle_times) / len(cycle_times)
                if len(cycle_times) > 1:
                    cum_stddev_cycle_time = statistics.stdev(cycle_times)
                else:
                    cum_stddev_cycle_time = 0.0
            else:
                cum_avg_cycle_time = "N/A"
                cum_stddev_cycle_time = "N/A"
            
            # Write to output file
            output_line = f"{exp};{run_number};{precision};{cycle_time};{cum_avg_precision};{cum_stddev_precision};{cum_avg_cycle_time};{cum_stddev_cycle_time}\n"
            output_file.write(output_line)
    
    print(f"Combined results with cumulative statistics have been written to '{output_file_path}'.")
