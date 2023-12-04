# Let's execute the provided bash script to check if it works correctly.
# Since the execution environment is Python, we'll use Python to simulate the bash script behavior.

import time

def loading_bar(duration):
    max_width = 30  # Maximum width of the loading bar
    progress = 0

    while progress < duration:
        bar = ""
        blocks = int(progress * max_width / duration)

        # Use a block character
        bar += "█" * blocks
        # Fill the rest with spaces
        bar += " " * (max_width - blocks)

        # Update the text dynamically based on progress
        if progress < duration / 3:
            text = "Data receiving..."
        elif progress < 2 * duration / 3:
            text = "Data received, processing..."
        else:
            text = "Task completing..."

        # Display the loading bar with the dynamic text
        print(f"\r[{bar}] {int(progress * 100 / duration)}% {text}", end='')
        time.sleep(1)
        progress += 1

    print("\nTask completed.")

# Start the loading bar with a duration of 5 seconds
loading_bar(5)
