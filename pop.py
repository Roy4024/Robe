import time
import random

def generate_and_save_output(file_name="output_log.txt"):
    with open(file_name, "a") as file:
        while True:
            # Generate a random number between 1 and 100
            random_number = random.randint(1, 100)
            
            # Get the current time
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            
            # Write the output to the file
            file.write(f"{current_time} - Random Number: {random_number}\n")
            file.flush()  # Ensure that the data is written to the file immediately
            
            # Print the output to the console (optional)
            print(f"{current_time} - Random Number: {random_number}")
            
            # Wait for 1 second before generating the next output
            time.sleep(1)

# Run the function
generate_and_save_output()
