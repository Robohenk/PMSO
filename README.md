# PMSO

Repository for the manuscript **"Towards Process Mining-based Simulation Optimization"**

## Overview

This repository contains a series of Python scripts developed to support event log analysis, process mining, and key performance indicator (KPI) extraction. The scripts automate the conversion of raw data to structured event logs, perform process mining, and consolidate metrics for detailed performance analysis.

**Data Source**: The input data for these scripts is derived from the dataset provided in the repository "Data underlying the paper Using agent-based simulation for emergent behavior detection in cyber-physical systems" ([DOI](https://doi.org/10.4121/14743263.v1)). This dataset is associated with the paper "Using agent-based simulation for emergent behavior detection in cyber-physical systems" ([DOI](https://doi.org/10.1109/WSC48552.2020.9383956)).

The project primarily uses [PM4Py](https://pm4py.fit.fraunhofer.de/) to handle XES log files, perform process discovery, and extract meaningful process metrics.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Scripts](#scripts)
  - [01_convert_to_xes.py](#01_convert_to_xespy)
  - [02_extract_event_log_indicators.py](#02_extract_event_log_indicatorspy)
  - [03_extract_process_mining_indicators.py](#03_extract_process_mining_indicatorspy)
  - [04_summaries_per_experiment.py](#04_summaries_per_experimentpy)
  - [05_combined_summaries.py](#05_combined_summariespy)
  - [06_combined_summaries_with_stats.py](#06_combined_summaries_with_statspy)
- [Citation](#citation)
- [License](#license)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/username/your-repo-name.git
   cd your-repo-name

2. **Install dependencies**:
   
   ```bash
   pip install -r requirements.txt

## Usage
To run these scripts, follow the steps below to ensure smooth data flow between them:

1. **Prepare the input data**: Download the dataset from the ([4TU.ResearchData repository](https://doi.org/10.4121/14743263.v1)) and place it in the `data/raw_data` directory.
2. **Convert raw data to XES event logs**: Run `01_convert_to_xes.py` to convert your raw data into XES event log format.
3. **Extract KPIs from event logs**: Use `02_extract_event_log_indicators.py` to extract relevant KPIs from the event logs.
4. **Perform process mining and generate models**: Run `03_extract_process_mining_indicators.py` to perform process discovery and generate process models.
5. **Summarize experimental metrics**: Use `04_summaries_per_experiment.py` to generate summaries per experiment.
6. **Combine summaries**: Run `05_combined_summaries.py` to combine all summaries into a single file.
7. **Generate statistical insights**: Use `06_combined_summaries_with_stats.py` to calculate cumulative statistics across experiments.

## Scripts

### 01_convert_to_xes.py
Converts tabular data from a pandas DataFrame into XES event log format.

**Inputs**: `DataFrame` with required columns (e.g., `uniqueID`, `event`, `timeStamp`).

**Outputs**: An `XES file` compatible with process mining tools.

### 02_extract_event_log_indicators.py
Processes the `XES event log files` to extract KPIs such as case durations.

**Inputs**: `XES files`.

**Outputs**: A `text file` with calculated KPIs for each event log.

### 03_extract_process_mining_indicators.py
Performs process discovery on `XES event logs` using the `Inductive Miner algorithm`, generating `Petri net models` and visualizations.

**Inputs**: `XES files` from a specified input directory.

**Outputs**: `PNML files` containing Petri nets and corresponding PNG images.

### 04_summaries_per_experiment.py
Generates summary files for each experiment, aggregating metrics and cycle time data by experiment and run.

**Inputs**: Metrics and cycle time text files organized by experiment and run.

**Outputs**: A summary file per experiment with consolidated metrics and cycle times.

### 05_combined_summaries.py
Combines all summary files into a single text file, consolidating metrics across all experiments.

**Inputs**: Summary files organized by experiment.

**Outputs**: A combined text file summarizing results from all experiments.

### 06_combined_summaries_with_stats.py
Calculates cumulative statistics, including average and standard deviation, for precision and cycle times across experiments.

**Inputs**: Summary files from previous experiments.

**Outputs**: A `text file` with consolidated metrics and cumulative statistics.

## Citation
If you are using materials in your scientific work, please cite the original manuscript:

**Rob Bemthuis**. (n.d.). *Towards Process Mining-based Simulation Optimization*. Journal/Conference. [DOI](https://doi.org/t.b.d.)

BiBTeX:

```bibtex
   @article{bemthuis2024towards,
    author = {Bemthuis, Rob},
    title = {Towards Process Mining-based Simulation Optimization},
    journal = {Journal/Conference Name},
    year = {2024},
    note = {Under review}
  }
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.
