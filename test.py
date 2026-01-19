import time

interval = 1.0  # desired interval in seconds
print("Program started with high precision.")

# Run indefinitely, press Ctrl+C to stop
try:
    while True:
        start_time = time.perf_counter()

        # Code to execute each second
        current_time = time.strftime("%H:%M:%S", time.localtime())
        print(f"Current time is: {current_time}")

        # Calculate how long the actions took and how much time to sleep
        elapsed_time = time.perf_counter() - start_time
        time_to_sleep = interval - elapsed_time
        print(time_to_sleep)
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

except KeyboardInterrupt:
    print("\nProgram finished by user.")
    print(f"Total runtime: {time.perf_counter() - start_time:.6f} seconds")
