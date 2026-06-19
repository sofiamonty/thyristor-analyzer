import math
import openpyxl

print("=== THYRISTOR EVALUATION PROGRAM ===")
print()
print("In this program, we will evaluate these aspects of a single-phase full-wave thyristor bridge rectifier:")
print("1. Firing angle.")
print("2. Output DC voltage.")
print("3. Output DC current.")
print("4. AC input power.")
print("5. DC output power")
print("6. Rectification efficiency.")

answer = input("Are you ready to start? (yes/no): ").strip().lower()
while True:
    if answer == "yes":
        import calculator
        results = calculator.run()

        # --- Summary ---
        print_summary = input("Would you like to print a summary of the results? (yes/no): ").strip().lower()
        if print_summary == "yes":
            print("\n=== RESULTS SUMMARY ===")

            col1  = 6   # Angle
            col2  = 8   # Ideal V
            col3  = 7   # User V
            col4  = 11  # Ideal Avg C
            col5  = 10  # User Avg C
            col6  = 11  # Ideal AC P
            col7  = 11  # Ideal DC P
            col8  = 10  # User DC P
            col9  = 12  # Ideal Eff
            col10 = 10  # User Eff

            header1 = (
                f"{'Angle':>{col1}} | "
                f"{'Ideal V':>{col2}} | "
                f"{'User V':>{col3}} | "
                f"{'Ideal Avg C':>{col4}} | "
                f"{'User Avg C':>{col5}} | "
                f"{'Ideal AC P':>{col6}} | "
                f"{'Ideal DC P':>{col7}} | "
                f"{'User DC P':>{col8}} | "
                f"{'Ideal Eff':>{col9}} | "
                f"{'User Eff':>{col10}}"
            )

            header2 = (
                f"{'(°)':>{col1}} | "
                f"{'(V)':>{col2}} | "
                f"{'(V)':>{col3}} | "
                f"{'(A)':>{col4}} | "
                f"{'(A)':>{col5}} | "
                f"{'(W)':>{col6}} | "
                f"{'(W)':>{col7}} | "
                f"{'(W)':>{col8}} | "
                f"{'(%)':>{col9}} | "
                f"{'(%)':>{col10}}"
            )

            separator = "-" * len(header1)

            print(header1)
            print(header2)
            print(separator)

            for r in results:
                print(
                    f"{r['firing_angle']:>{col1}.1f} | "
                    f"{r['ideal_voltage']:>{col2}.2f} | "
                    f"{r['user_voltage']:>{col3}.2f} | "
                    f"{r['ideal_avg_current']:>{col4}.2f} | "
                    f"{r['user_avg_current']:>{col5}.2f} | "
                    f"{r['calc_ac_power']:>{col6}.2f} | "
                    f"{r['calc_dc_power']:>{col7}.2f} | "
                    f"{r['user_dc_power']:>{col8}.2f} | "
                    f"{r['calc_efficiency']:>{col9}.2f} | "
                    f"{r['user_efficiency']:>{col10}.2f}"
                )
        else:
            print("Goodbye!")
            break

        # --- Excel export ---
        export_results = input("Would you like to export the results to an Excel sheet? (yes/no): ").strip().lower()
        if export_results == "yes":
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Thyristor Rectifier"

            ws.append([
                "Firing Angle (°)",
                "Ideal Voltage (V)",
                "User Voltage (V)",
                "Ideal Avg Current (A)",
                "User Avg Current (A)",
                "Ideal AC Power (W)",
                "Ideal DC Power (W)",
                "User DC Power (W)",
                "Ideal Efficiency (%)",
                "User Efficiency (%)"
            ])

            for r in results:
                ws.append([
                    r["firing_angle"],
                    round(r["ideal_voltage"], 2),
                    round(r["user_voltage"], 2),
                    round(r["ideal_avg_current"], 2),
                    round(r["user_avg_current"], 2),
                    round(r["calc_ac_power"], 2),
                    round(r["calc_dc_power"], 2),
                    round(r["user_dc_power"], 2),
                    round(r["calc_efficiency"], 2),
                    round(r["user_efficiency"], 2)
                ])

            filename = "THYRISTOR_results.xlsx"
            wb.save(filename)
            print(f"Results exported to {filename}.")

        # --- Harmonic analysis (independent of Excel export) ---
        run_harmonics = input("Would you like to run harmonic analysis? (yes/no): ").strip().lower()
        if run_harmonics == "yes":
            import harmonics
            harmonics.run(results)

        break

    elif answer == "no":
        print("Goodbye")
        break
    else:
        answer = input("Error! Please type 'yes' or 'no': ")