import math

def run():

    def get_angle():
        while True:
            try:
                angle_deg = float(input("What is your firing angle in degrees (0°-180°): "))
                if not (0 <= angle_deg <= 180):
                    print("Error! The angle value must be between 0° and 180°.")
                else:
                    return angle_deg
            except ValueError:
                print("Error! The angle must be expressed as a number!")

    def calculations(angle_deg, input_rms_voltage, load_resistance):
        alpha = math.radians(angle_deg)

        V_m = input_rms_voltage * math.sqrt(2)

        # RMS current: I_rms = (Vm / (√2 · R)) · √[ (1/π)·((π−α) + sin(2α)/2) ]
        factor = (1.0 / math.pi) * ((math.pi - alpha) + (math.sin(2 * alpha) / 2))
        factor = max(factor, 0)
        rms_current = (V_m / (math.sqrt(2) * load_resistance)) * math.sqrt(factor)

        # DC output: V_dc = (Vm/π)(1 + cosα)
        output_dc_voltage = (V_m / math.pi) * (1 + math.cos(alpha))
        avg_current = output_dc_voltage / load_resistance

        calc_rms_voltage = rms_current * load_resistance                                         # V_rms = I_rms × R

        # Displacement factor: DF = cos(arctan((cos2α − 1) / ((π−α) + sin(2α)/2)))

        calc_dc_power   = output_dc_voltage * avg_current                                        # P_dc = V_dc × I_dc
        calc_ac_power   = (rms_current ** 2) * load_resistance                                   # P_ac = I_rms² × R
        calc_efficiency = (calc_dc_power / calc_ac_power) * 100 if calc_ac_power > 0 else 0     # η = P_dc / P_ac × 100

        return output_dc_voltage, avg_current, rms_current, calc_rms_voltage, calc_dc_power, calc_ac_power, calc_efficiency

    print("\nAwesome! A few questions before we start: ")

    while True:
        try:
            input_rms_voltage = float(input("Please type your input RMS voltage in volts (V): "))
            if input_rms_voltage < 0:
                print("The input RMS voltage cannot be negative.")
            else:
                break
        except ValueError:
            print("Error! The voltage value must be a number.")

    while True:
        try:
            load_resistance = float(input("What is the value of your resistor in Ohms (Ω): "))
            if load_resistance <= 0:
                print("Error! The load resistance must be a positive number.")
            else:
                break
        except ValueError:
            print("Error! The input must be numerical.")

    print("\nNow, let's get started!\n")
    print("--- Evaluation Loop ---")
    print("You will be asked for the firing angle and your measured load voltage and current.")
    print("The results will then be evaluated and compared against theoretical predictions.")

    results = []

    while True:
        print()
        angle_deg = get_angle()
        calc_voltage, avg_current, rms_current, calc_rms_voltage, calc_dc_power, calc_ac_power, calc_efficiency = calculations(angle_deg, input_rms_voltage, load_resistance)

        form_factor = rms_current / avg_current if avg_current > 0 else 1.0

        print(f"Firing angle: {angle_deg}.")
        print(f"Theoretical DC average load voltage: {calc_voltage:.2f} V.")

        # --- User voltage input and check ---
        while True:
            try:
                user_load_voltage = float(input("Type in your measured DC average load voltage: "))
                break
            except ValueError:
                print("Error! Input must be a number.")

        while True:
            voltage_diff = abs(calc_voltage - user_load_voltage)
            if calc_voltage * 0.9 <= user_load_voltage <= calc_voltage * 1.1:
                print(f"Your results are within a 10% margin of expected measurements! The difference is {voltage_diff:.2f} V.")
                break
            else:
                print(f"Your results are not within the 10% margin of expected measurements. The difference is {voltage_diff:.2f} V.")
                answer = input("Would you like to repeat the measurement? (yes/no): ").strip().lower()
                if answer != "yes":
                    break
                while True:
                    try:
                        user_load_voltage = float(input("Enter your new measured DC average load voltage: "))
                        break
                    except ValueError:
                        print("Error! Input must be numerical.")

        # --- User current input and check ---
        print(f"Theoretical expected DC average current: {avg_current:.2f} A")

        while True:
            try:
                user_avg_current = float(input("Please type in your measured DC average load current: "))
                break
            except ValueError:
                print("Error! Input must be numerical.")

        while True:
            current_diff = abs(avg_current - user_avg_current)
            if avg_current * 0.9 <= user_avg_current <= avg_current * 1.1:
                print(f"Your results are within a 10% margin of expected measurements! The difference is {current_diff:.2f} A.")
                break
            else:
                print(f"Your results are not within the 10% margin of expected measurements. The difference is {current_diff:.2f} A.")
                answer = input("Would you like to repeat the measurement? (yes/no): ").strip().lower()
                if answer != "yes":
                    break
                while True:
                    try:
                        user_avg_current = float(input("Enter your new measured DC average load current: "))
                        break
                    except ValueError:
                        print("Error! Input must be numerical.")

        # --- User figures of merit ---
        user_dc_power    = user_load_voltage * user_avg_current                                  # P_dc = V_dc × I_dc
        user_ac_power    = calc_ac_power                                                         # P_ac = I_rms² × R (theoretical)
        user_efficiency  = (user_dc_power / user_ac_power) * 100 if user_ac_power > 0 else 0    # η = P_dc / P_ac × 100

        print(f"\n--- Ideal results ---")
        print(f"DC Output Voltage:  {calc_voltage:.2f} V")
        print(f"DC current:         {avg_current:.2f} A")
        print(f"AC power:           {calc_ac_power:.2f} W")
        print(f"DC power:           {calc_dc_power:.2f} W")
        print(f"Efficiency:         {calc_efficiency:.2f} %")
        print(f"\n--- Your results ---")
        print(f"DC Output Voltage:  {user_load_voltage:.2f} V")
        print(f"DC current:         {user_avg_current:.2f} A")
        print(f"AC power:           {calc_ac_power:.2f} W")
        print(f"DC power:           {user_dc_power:.2f} W")
        print(f"Efficiency:         {user_efficiency:.2f} %")

        results.append({
            "firing_angle":       angle_deg,
            "ideal_voltage":      calc_voltage,
            "user_voltage":       user_load_voltage,
            "ideal_avg_current":  avg_current,
            "user_avg_current":   user_avg_current,
            "calc_ac_power":      calc_ac_power,        # was missing from dict
            "calc_dc_power":      calc_dc_power,
            "user_dc_power":      user_dc_power,
            "calc_efficiency":    calc_efficiency,
            "user_efficiency":    user_efficiency
        })

        again = input("\nEvaluate another firing angle? (yes/no): ").strip().lower()
        if again != "yes":
            print("\nExiting phase control evaluation.")
            break

    return results