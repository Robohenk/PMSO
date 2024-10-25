# -*- coding: utf-8 -*-
"""
Created on October 25 2024
@author: Rob Bemthuis

Script: 02_extract_event_log_indicators.py
Purpose: This script processes XES event logs to extract key performance indicators (KPIs) such as case duration. 
         It calculates indicators by reading each case in the event log, identifying start and end events, 
         and computing the duration per case.
Inputs: XES files from a specified input directory, with expected columns such as 'case:concept:name' and 'concept:name'.
Outputs: A summary file saved in an output directory, containing calculated indicators (e.g., case durations) for each event log.
"""

import pm4py
import pandas as pd
import os
from pm4py.statistics.traces.generic.log import case_statistics

# Define the input and output directories
input_dir = "02_processed_input"
output_dir = "03_event_logs_KPIs"

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through all .xes files in the "output" directory
for file_name in os.listdir(input_dir):
    if file_name.endswith(".xes"):
        # Load the event log
        file_path = os.path.join(input_dir, file_name)
        event_log = pm4py.read_xes(file_path)

        # Convert event log to DataFrame
        event_df = pm4py.convert_to_dataframe(event_log)

        # Ensure 'case:concept:name' column is present
        if 'case:concept:name' not in event_df.columns:
            print(f"'case:concept:name' column not found in {file_name}, skipping.")
            continue

        # Initialize a list to store durations
        durations = []

        # Group by cases
        for case_id, group in event_df.groupby('case:concept:name'):
            # Get the timestamp where 'concept:name' == 'productCallsForTransportRegion1'
            start_events = group[group['concept:name'] == 'productCallsForTransportRegion1']
            if start_events.empty:
                # No start event for this case, skip
                continue
            start_time = start_events['time:timestamp'].min()

            # Get the timestamp where 'concept:name' == 'droppedOffRegion3'
            end_events = group[group['concept:name'] == 'droppedOffRegion3']
            if end_events.empty:
                # No end event for this case, skip
                continue
            end_time = end_events['time:timestamp'].max()

            # Compute duration in seconds
            duration = (end_time - start_time).total_seconds()
            durations.append(duration)

        # Compute average cycle time
        if durations:
            avg_cycle_time = sum(durations) / len(durations)
        else:
            avg_cycle_time = 0

        # Filter events that involve vehicle activities
        vehicle_df = event_df[
            event_df['concept:name'].str.contains(r'assignedToVehicle|pickedUp|droppedOff', case=False, na=False)
        ]

        # If there are no vehicle events, skip this log
        if vehicle_df.empty:
            print(f"No vehicle events found in {file_name}, skipping.")
            continue

        # Ensure 'org:resource' and 'time:timestamp' columns are present
        if 'org:resource' not in vehicle_df.columns or 'time:timestamp' not in vehicle_df.columns:
            print(f"Necessary columns not found in {file_name}, skipping.")
            continue

        # Get unique vehicles involved in the event log
        unique_vehicles = vehicle_df['org:resource'].unique()

        # Initialize a dictionary to store utilization time per vehicle
        vehicle_utilization = {}

        # Calculate utilization time for each vehicle
        for vehicle in unique_vehicles:
            vehicle_subset = vehicle_df[vehicle_df['org:resource'] == vehicle]
            # Calculate the time vehicle was active
            utilization_time = vehicle_subset['time:timestamp'].max() - vehicle_subset['time:timestamp'].min()
            vehicle_utilization[vehicle] = utilization_time.total_seconds()

        # Convert to DataFrame for easier analysis
        vehicle_utilization_df = pd.DataFrame.from_dict(
            vehicle_utilization, orient='index', columns=['UtilizationTime']
        )

        # Calculate total time span in the event log
        total_time_span = event_df['time:timestamp'].max() - event_df['time:timestamp'].min()
        total_time_span = total_time_span.total_seconds()

        # Check for zero total time span to avoid division by zero
        if total_time_span == 0:
            print(f"Total time span is zero in {file_name}, skipping.")
            continue

        # Calculate the utilization rate for each vehicle (utilization time / total event log time span)
        vehicle_utilization_df['UtilizationRate'] = vehicle_utilization_df['UtilizationTime'] / total_time_span

        # Calculate the average utilization rate for all vehicles
        average_utilization_rate = vehicle_utilization_df['UtilizationRate'].mean()

        # Prepare the output file name
        output_file_name = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.txt")

        # Write the results to a text file
        with open(output_file_name, 'w') as f:
            f.write(f"Average Product Cycle Time: {avg_cycle_time:.2f} seconds\n")
            f.write(f"Average Resource Utilization Rate (Vehicles): {average_utilization_rate:.4f}\n\n")
            f.write("Utilization Time and Rate for each vehicle:\n")
            for vehicle, row in vehicle_utilization_df.iterrows():
                f.write(
                    f"Vehicle {vehicle}: Utilization Time: {row['UtilizationTime']:.2f} seconds, "
                    f"Utilization Rate: {row['UtilizationRate']:.4f}\n"
                )

        # Display success message
        print(f"Processed {file_name}, results saved to {output_file_name}")
