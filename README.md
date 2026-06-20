## Thyristor Bridge Rectifier Analyzer
A Python-based interactive analysis tool for analyzing the electrical behavior of a single-phase full-wave thyristor bridge rectifier across multiple firing angles.

The tool computes theoretical output values, validates them against user-supplied measurements, generates a full results summary with CSV export, and performs harmonics spectrum analysis from the 1st to the 20th harmonic for each firing angle tested.

Background: This project originated as a laboratory experiment in EMI analysis. When persistent hardware failure made the original measurements impossible, the scope was restructured around software-based harmonic characterization, turning an equipment failure into a working analysis tool.

## Features
 - Interactive command-line interface with user-guided input
 - Theoretical calculation of DC output voltage, current, AC input power, DC output power, and rectification efficiency
 - Real-time validation of user measurements against theoretical values with 10% tolerance warning
 - Multi-angle batch processing across firing angles from 0° to 180°
 - Results summary table comparing ideal and measured values across all tested angles
 - CSV export of full results for external analysis
 - Harmonic spectrum analysis from the 1st to 20th harmonic for each firing angle
 - Color-coded bar chart with THD and ripple factor display, exportable as an image

## Project structure
thyristor-analyzer/
 - thyristor_evaluator.py   # Main entry point — user interface and program flow
 - calculator.py            # Theoretical calculations and measurement validation
 - harmonics.py             # FFT-based harmonic spectrum analysis and plot generation
 - README.md                # This file

## Requirements

Python 3.x is required. Install dependencies with:

pip install numpy matplotlib openpyxl

The `math` module is part of the Python standard library and requires no installation.

## How to use

1. Clone the repository:
   git clone https://github.com/sofiamonty/thyristor-analyzer.git

2. Navigate to the project folder:
   cd thyristor-analyzer

3. Install the required libraries:
   pip install numpy matplotlib openpyxl

4. Run the main script:
   python thyristor_evaluator.py

5. Follow the on-screen prompts:
   - Enter a firing angle in degrees (0°–180°)
   - Enter your measured DC output voltage and current
   - The program will validate your measurements against theoretical values
   - Repeat for each firing angle you wish to analyse

6. Once all angles are entered, the program will:
   - Display a full results summary table
   - Export results to a CSV file
   - Generate a harmonic spectrum plot for each firing angle

## Background and motivation

This project originated as a laboratory experiment in EMI analysis of a 
single-phase full-wave thyristor bridge rectifier. The original goal was 
to measure and characterise electromagnetic interference using standard 
lab equipment.

When persistent hardware failures made the EMI measurements impossible, 
the scope was restructured rather than abandoned. Voltage and current data 
were collected manually across seven firing angles (0°, 30°, 60°, 90°, 
120°, 150°, 180°), and a Python-based analysis tool was developed from 
scratch to extract meaningful power quality information from the results.

The decision to pivot from hardware measurement to software-based harmonic 
characterisation turned an equipment problem into a more complete analysis 
than the original experiment would have produced — covering theoretical 
validation, measurement comparison, and full harmonic spectrum analysis up 
to the 20th harmonic.