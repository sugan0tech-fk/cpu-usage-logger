import psutil
import time
from datetime import datetime
import MacTmp as cpu_temp
import matplotlib.pyplot as plt
import numpy as np

def get_cpu_usage():
    return psutil.cpu_percent(interval=0.1)

def get_cpu_temperature():
    return cpu_temp.CPU_Temp()

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def read_number_from_file():
    try:
        with open("hang_time.log", 'r') as file:
            number = int(file.read())
            return number
    finally:
        return 0

def gen_graph(cpu_usages):
    plt.plot(cpu_usages, label="CPU Usage (%)")
    plt.xlabel("Time (seconds)")
    plt.ylabel("CPU ")
    plt.title("CPU Usage Over Time")
    plt.legend()
    plt.grid(True)
    plt.savefig("cpu_usage_over_time.png")
    plt.show()

def update_hang_time(hang_time: int):
    with open("hang_time.log", "w") as file:
        file.write(str(hang_time + read_number_from_file() ))


def log_csv(log_file):
    timestamps = []
    cpu_usages = []
    cpu_temperatures = []
    hang_time = 0
    with open(log_file, "a") as file:
        try:
            while True:
                cpu_usage = get_cpu_usage()
                cpu_temperature = get_cpu_temperature()
                current_time = get_current_time()
                file.write(f"{current_time},{cpu_usage:.2f}%,{cpu_temperature}°C\n")
                if(cpu_usage > 65):
                    hang_time += 1
                file.flush()  # Flush the buffer to ensure data is written to the file immediately
                timestamps.append(current_time)
                cpu_usages.append(cpu_usage)
                cpu_temperatures.append(cpu_temperature)
                time.sleep(1)
        except KeyboardInterrupt:
            print("Logging stopped.")

    gen_graph(cpu_usages)
    update_hang_time(hang_time)

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
        log_csv(args.log_file)

