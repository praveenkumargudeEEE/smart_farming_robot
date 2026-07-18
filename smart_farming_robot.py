import time
import random
import os
import math


class SmartFarmingRobotSim:
    def __init__(self):
        # Operational parameters & thresholds
        self.moisture_lower_threshold = 35.0  # Trigger irrigation below 35%
        self.moisture_optimal_target = 60.0  # Stop irrigation once 60% is reached
        self.temp_upper_bound = 40.0  # Emergency shutdown threshold in °C

        # Initializing Robot Hardware/State Parameters
        self.current_state = "IDLE"  # System States: IDLE, SCANNING, IRRIGATING, EMERGENCY
        self.pump_relay_pin = False  # False = Low/Off, True = High/On
        self.water_tank_level = 100.0  # Starts at 100% capacity
        self.report_path = "farming_automation_report.txt"

        # Initialize an empty file with headers for reporting metrics
        with open(self.report_path, "w") as f:
            f.write("========================================================\n")
            f.write("    CODEC TECHNOLOGIES: INDUSTRIAL SMART FARMING LOG    \n")
            f.write("========================================================\n\n")

    def calibrate_adc_to_moisture(self, raw_adc):
        """
        Calibrates raw 12-bit ADC values (0 to 4095) from a capacitive moisture sensor
        into a meaningful volumetric water content percentage.
        Uses an inverse relationship mapping: Dry soil (~3200 ADC) -> 0% | Wet soil (~1500 ADC) -> 100%
        """
        dry_air_value = 3200.0
        saturated_water_value = 1500.0

        # Constrain input bounds
        constrained_adc = max(min(raw_adc, dry_air_value), saturated_water_value)

        # Linear conversion equation
        moisture_percentage = ((dry_air_value - constrained_adc) / (dry_air_value - saturated_water_value)) * 100.0
        return round(moisture_percentage, 2)

    def process_camera_matrix(self):
        """
        Simulates parsing a spatial image array frame captured by the robot's camera.
        Calculates a mock NDVI (Normalized Difference Vegetation Index) value.
        NDVI = (NIR - Red) / (NIR + Red)
        """
        # Generating raw simulated channel reflections for Near-Infrared and Red spectrums
        near_infrared_channel = random.uniform(0.4, 0.9)
        red_channel = random.uniform(0.1, 0.5)

        ndvi = (near_infrared_channel - red_channel) / (near_infrared_channel + red_channel)

        # Crop health analysis classification based on index value ranges
        if ndvi > 0.6:
            return "Healthy Crop (High Chlorophyll Activity)", round(ndvi, 2)
        elif 0.3 <= ndvi <= 0.6:
            return "Stressed Crop (Nutrient Deficient / Under-watered)", round(ndvi, 2)
        else:
            return "Anomalous / Disease Patch Detected", round(ndvi, 2)

    def run_state_machine_iteration(self, cycle_num):
        print(f"\n--- Execution Cycle #{cycle_num} | System State: [{self.current_state}] ---")

        # Simulate environment changes or readings
        simulated_raw_adc = random.randint(1400, 3300)
        moisture_pct = self.calibrate_adc_to_moisture(simulated_raw_adc)
        temperature = round(random.uniform(22.0, 43.0), 2)

        # State Execution Logic
        if self.current_state == "IDLE":
            # Transition to active processing
            self.current_state = "SCANNING"

        elif self.current_state == "SCANNING":
            crop_health, ndvi_score = self.process_camera_matrix()
            print(f"[Telemetry] Sensor ADC: {simulated_raw_adc} -> Moisture: {moisture_pct}% | Temp: {temperature}°C")
            print(f"[Vision Pipeline] NDVI Score: {ndvi_score} -> Diagnosis: {crop_health}")

            # Critical Safety Interlock check
            if temperature >= self.temp_upper_bound:
                self.current_state = "EMERGENCY"
                return

            # Decisions driving Actuator control loops
            if moisture_pct < self.moisture_lower_threshold:
                print(f"[Alert] Moisture dropped below critical threshold ({self.moisture_lower_threshold}%)!")
                self.current_state = "IRRIGATING"
                self.pump_relay_pin = True
            else:
                print("[Info] Moisture profiles stable. Transitioning back to IDLE state.")
                self.current_state = "IDLE"

            self.log_event(moisture_pct, temperature, crop_health, ndvi_score)

        elif self.current_state == "IRRIGATING":
            # Action execution inside the loop
            self.water_tank_level -= random.uniform(4.0, 7.0)
            print(
                f"[Actuator] Pump Subroutine Active (Relay: HIGH) | Main Water Supply Tank Level: {round(self.water_tank_level, 1)}%")

            # Check if moisture profiles have recovered or if we ran dry
            if self.water_tank_level <= 5.0:
                print("[System Stop] Low water levels. Disengaging active pumps.")
                self.pump_relay_pin = False
                self.current_state = "IDLE"
            elif moisture_pct >= self.moisture_optimal_target:
                print(f"[Target Met] Optimal soil moisture matrix reached ({moisture_pct}%). Terminating flow.")
                self.pump_relay_pin = False
                self.current_state = "IDLE"
            else:
                # Retain irrigation state to continuously add water over sequential cycles
                print(f"[Update] Soil absorbing moisture. Currently at {moisture_pct}%. Continuing irrigation cycle.")

            self.log_event(moisture_pct, temperature, "Skipped - Active Irrigation Mode", N / A = True)

            elif self.current_state == "EMERGENCY":
            print(f"[FATAL FAILURE DETECTED] Ambient thermal values exceeding maximum hardware tolerances!")
            print("[Action] Forcing hardware trip protection. Emergency shutdown engaged. Safe-state active.")
            self.pump_relay_pin = False
            # Log failure parameters
            self.log_event(moisture_pct, temperature, "ABORTED - HARDWARE SAFETY TRIP", 0.0, fault=True)
            # Re-calibrating/cooling down to simulate restoration
            self.current_state = "IDLE"

    def log_event(self, moisture, temp, health_desc, ndvi, fault=False, N/

        A = False):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    ndvi_str = "N/A" if N / A else str(ndvi)
    pump_str = "ACTIVE (HIGH)" if self.pump_relay_pin else "OFF (LOW)"

    status_line = "CRITICAL FAULT DETECTED" if fault else f"Moisture: {moisture}% | Temp: {temp}°C | NDVI: {ndvi_str}"

    log_entry = (
        f"[{timestamp}] State: {self.current_state.ljust(10)} | "
        f"{status_line} | Pump Relay: {pump_str} | Tank Capacity: {round(self.water_tank_level, 1)}%\n"
        f"   Visual Diagnostics: {health_desc}\n"
        f"----------------------------------------------------------------------------------------\n"
    )

    with open(self.report_path, "a") as f:
        f.write(log_entry)


def execute_simulation(self, steps=10):
    print("Initializing Autonomous Farming Drone Simulation...")
    time.sleep(1)
    for step in range(1, steps + 1):
        self.run_state_machine_iteration(step)
        time.sleep(1.2)
    print(f"\n[Process Finalized] Simulation compiled. Inspection report generated: '{self.report_path}'")


if __name__ == "__main__":
    robot_system = SmartFarmingRobotSim()
    robot_system.execute_simulation(10)