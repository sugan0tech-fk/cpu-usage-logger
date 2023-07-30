import psutil
import time
from datetime import datetime
import MacTmp as cpu_temp
import matplotlib.pyplot as plt

def get_cpu_usage():
    return psutil.cpu_percent(interval=0.1)

def get_cpu_temperature():
    return cpu_temp.CPU_Temp()

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main(log_file):
    timestamps = []
    cpu_usages = []
    cpu_temperatures = []
    with open(log_file, "a") as file:
        try:
            while True:
                cpu_usage = get_cpu_usage()
                cpu_temperature = get_cpu_temperature()
                current_time = get_current_time()
                file.write(f"{current_time},{cpu_usage:.2f}%,{cpu_temperature}°C\n")
                file.flush()  # Flush the buffer to ensure data is written to the file immediately
                timestamps.append(current_time)
                cpu_usages.append(cpu_usage)
                cpu_temperatures.append(cpu_temperature)
                time.sleep(1)
        except KeyboardInterrupt:
            print("Logging stopped.")

    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, cpu_usages, label="CPU Usage (%)", marker="o")
    plt.plot(timestamps, cpu_temperatures, label="CPU Temperature (°C)", marker="o")
    plt.xlabel("Timestamp")
    plt.ylabel("Percentage / Temperature")
    plt.title("CPU Usage and Temperature Over Time")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.savefig("cpu_usage_temp_plot.png")
    plt.show()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Log CPU usage and temperature and provide statistics.")
    parser.add_argument("--log-file", default="cpu_usage_temp_log.csv", help="Specify the log file name.")
    parser.add_argument("--stats", choices=["average"], help="Specify the statistics to calculate.")

    args = parser.parse_args()

    if args.stats:
        if args.stats == "average":
            try:
                with open(args.log_file, "r") as f:
                    lines = f.readlines()
                    if lines:
                        cpu_usages = [float(line.split(",")[1]) for line in lines]
                        average_cpu_usage = sum(cpu_usages) / len(cpu_usages)

                        cpu_temperatures = [float(line.split(",")[2].strip()[:-2]) for line in lines]
                        average_cpu_temperature = sum(cpu_temperatures) / len(cpu_temperatures)

                        print(f"Average CPU Usage: {average_cpu_usage:.2f}%")
                        print(f"Average CPU Temperature: {average_cpu_temperature:.2f}°C")
                    else:
                        print("No data in the log file.")
            except FileNotFoundError:
                print("Log file not found.")
        else:
            print("Invalid statistics option.")
    else:
        main(args.log_file)

