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