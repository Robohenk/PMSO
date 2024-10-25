# -*- coding: utf-8 -*-
"""
Created on October 25 2024
@author: Rob Bemthuis

Script: 01_convert_to_xes.py
Purpose: This script converts a tabular dataset (in a pandas DataFrame) into an XES (eXtensible Event Stream) log 
         format, which is widely used for process mining and event log analysis.
Inputs: A pandas DataFrame with specific required columns (e.g., 'uniqueID', 'event', 'timeStamp').
Outputs: An XES file that represents the input data in a structured event log format, compatible with process 
         mining tools such as PM4Py.
"""
import os
import pandas as pd
import pm4py
from pm4py.objects.log.obj import EventLog, Trace, Event
from pm4py.objects.log.exporter.xes import exporter as xes_exporter

def create_event_log(df):
    # Check if necessary columns exist
    required_columns = ['uniqueID', 'productNr', 'event', 'timeStamp', 'productType',
                        'vehicleType', 'vehicle', 'currentDecayLevel', 'processingStation',
                        'productIDStr', 'productID']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"The column '{col}' is not present in the DataFrame.")

    # Handle missing or NaN values in 'productNr' (drop rows with NaN in 'productNr')
    df = df.dropna(subset=['productNr'])

    # Create the EventLog object
    log = EventLog()

    # Modify the extensions dictionary directly
    log.extensions['Time'] = {'prefix': 'time', 'uri': 'http://www.xes-standard.org/time.xesext', 'name': 'Time'}
    log.extensions['Lifecycle'] = {'prefix': 'lifecycle', 'uri': 'http://www.xes-standard.org/lifecycle.xesext', 'name': 'Lifecycle'}
    log.extensions['Concept'] = {'prefix': 'concept', 'uri': 'http://www.xes-standard.org/concept.xesext', 'name': 'Concept'}
    log.extensions['Organizational'] = {'prefix': 'org', 'uri': 'http://www.xes-standard.org/org.xesext', 'name': 'Organizational'}

    # Define classifiers directly as dictionaries
    log.classifiers['Event Name'] = ["concept:name"]
    log.classifiers['(Event Name AND Lifecycle transition)'] = ["concept:name", "lifecycle:transition"]

    # Add log attributes
    log.attributes["concept:name"] = "XES Event Log"

    # Group by productNr (case concept)
    grouped = df.groupby('productNr')
    for productNr, group in grouped:
        # Create a trace and set 'productNr' as the case identifier
        trace = Trace(attributes={"concept:name": str(productNr)})
        for _, row in group.iterrows():
            # Create an event with the relevant attributes
            event = Event({
                "concept:name": row["event"],  # Name of the event (activity)
                "lifecycle:transition": "complete",  # Add lifecycle transition
                "time:timestamp": pd.to_datetime(row["timeStamp"]),  # Convert timestamp to datetime
                "productType": row["productType"],  # Product type
                "productNr": row["productNr"],  # Product number
                "vehicleType": str(row["vehicleType"]),  # Vehicle type (if applicable)
                "org:resource": str(row["vehicle"]),  # Vehicle involved (if applicable)
                "uniqueID": int(row["uniqueID"]),  # Unique ID for the event
                "currentDecayLevel": float(row["currentDecayLevel"]),  # Current decay level
                "productIDStr": row["productIDStr"],  # Product ID string
                "processingStation": str(row["processingStation"]) if pd.notna(row["processingStation"]) else "NA",  # Processing station
                "productID": row["productID"]  # Include productID as per your XES snippet
            })
            trace.append(event)  # Append event to trace
        log.append(trace)  # Append trace to the event log
    return log

# Function to load data from txt
def load_data(file_path):
    # Assuming the .txt file is tab-separated, adjust delimiter if necessary
    df = pd.read_csv(file_path, delimiter='\t')
    return df

# Function to process all files
def process_all_files(input_folder, output_folder):
    print(f"Processing files in folder: {input_folder}")  # Debugging statement
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Create output folder if it doesn't exist
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".txt"):
            file_path = os.path.join(input_folder, file_name)
            print(f"Processing file: {file_name}")  # Debugging statement
            df = load_data(file_path)
            log = create_event_log(df)
            output_path = os.path.join(output_folder, file_name.replace(".txt", ".xes"))
            print(f"Saving XES to: {output_path}")  # Debugging statement
            xes_exporter.apply(log, output_path)

# Get current working directory
current_directory = os.getcwd()

# Specify input and output directories relative to the current directory
input_folder = os.path.join(current_directory, "01_raw_input")  # replace "input2" with your actual folder name
output_folder = os.path.join(current_directory, "02_processed_input")  # specify the folder for XES files

# Start the procedure when running the script
if __name__ == "__main__":
    process_all_files(input_folder, output_folder)
