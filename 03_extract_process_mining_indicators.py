# -*- coding: utf-8 -*-
"""
Created on October 25 2024
@author: Rob Bemthuis

Script: 03_extract_process_mining_indicators.py
Purpose: This script performs process discovery on XES event logs, creating process models using the Inductive Miner. 
         It exports the discovered Petri net models in PNML format and generates visualizations as PNG images.
Inputs: XES files from a specified input directory.
Outputs: PNML files containing the discovered Petri nets and corresponding PNG images for visual representation, 
         all saved in an output directory.
"""

import pm4py
import os

from pm4py.objects.petri_net.exporter import exporter as pnml_exporter
from pm4py.visualization.petri_net import visualizer as pn_visualizer

# Define the input and output directories
input_dir = "02_processed_input"
output_dir = "04_process_discovery_conformance"

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through all .xes files in the "output" directory
for file_name in os.listdir(input_dir):
    if file_name.endswith(".xes"):
        print(f"Processing file: {file_name}")
        # Load the event log
        file_path = os.path.join(input_dir, file_name)
        event_log = pm4py.read_xes(file_path)

        # Discover the process model using the Inductive Miner
        net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(event_log)

        # Save the process model (Petri net) to PNML file
        output_model_file = os.path.join(
            output_dir, f"{os.path.splitext(file_name)[0]}.pnml"
        )
        pnml_exporter.apply(net, initial_marking, output_model_file)

        # Visualize and save the Petri net as an image
        output_image_file = os.path.join(
            output_dir, f"{os.path.splitext(file_name)[0]}.png"
        )
        gviz = pn_visualizer.apply(net, initial_marking, final_marking)
        pn_visualizer.save(gviz, output_image_file)

        # Compute fitness using token-based replay
        fitness_tbr = pm4py.fitness_token_based_replay(
            event_log, net, initial_marking, final_marking
        )

        # Print the fitness_tbr dictionary to inspect its contents
        print("Fitness TBR Dictionary:", fitness_tbr)

        # Access the fitness value using the correct key
        average_fitness_tbr = fitness_tbr['percentage_of_fitting_traces']

        # Compute precision using token-based replay
        precision_tbr = pm4py.precision_token_based_replay(
            event_log, net, initial_marking, final_marking
        )

        # Prepare the output metrics file name
        output_metrics_file = os.path.join(
            output_dir, f"{os.path.splitext(file_name)[0]}_metrics.txt"
        )

        # Write the metrics to a text file
        with open(output_metrics_file, "w") as f:
            f.write(f"Fitness (Token-Based Replay): {average_fitness_tbr:.2f}%\n")
            f.write(f"Precision (Token-Based Replay): {precision_tbr:.4f}\n")

        # Display success message
        print(f"Process model and metrics saved for {file_name}")
