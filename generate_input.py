import random


def create_random_file(filename, num_processes):
    """
    Generates a synthetic dataset with random process attributes.
    Format: PID, Arrival, Burst, Priority
    """
    with open(filename, 'w') as f:
        for i in range(1, num_processes + 1):
            pid = f"P{i}"
            arrival = random.randint(0, 20)  # Random arrival between 0-20
            burst = random.randint(1, 10)  # Random burst time between 1-10
            priority = random.randint(1, 5)  # Random priority between 1-5
            f.write(f"{pid}, {arrival}, {burst}, {priority}\n")

    print(f"File '{filename}' generated with {num_processes} random processes.")


# Generate a small test file (10 processes)
create_random_file("random_test.txt", 10)

# Generate a stress test file (100 processes)
create_random_file("stress_test.txt", 100)