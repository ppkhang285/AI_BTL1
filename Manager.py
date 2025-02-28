import sys
import time
import tracemalloc
import os



def load_input(testcase: int):
    path = "input/input" +str(testcase) +".txt"
    board = []
    with open(path) as f:
        size = int(f.readline().strip())
        for _ in range(size):  
            line = f.readline().strip().split() 
            board.append([int(num) for num in line])
    return board

def read_result(mode: int, testcase: int):
    path = ""

    if mode == 1:  # DFS
        path = "output/dfs/output" + str(testcase) + ".txt"
    elif mode == 2:  # A*
        path = "output/astar/output" + str(testcase) + ".txt"

    try:
        with open(path, "r") as f:
            path_read = [tuple(map(int, line.strip().split(','))) for line in f]
        return path_read
    except FileNotFoundError:
        print(f"Error: File {path} not found.")
        return []

def write_result(mode: int, testcase: int, path_data: list):
    path = ""

    if mode == 1:  # DFS
        path = "output/dfs/output" + str(testcase) + ".txt"
    elif mode == 2:  # A*
        path = "output/astar/output" + str(testcase) + ".txt"

    # Ensure the directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    try:
        with open(path, "w") as f:
            for point in path_data:
                f.write(f"{point[0]},{point[1]}\n")
        print(f"Path successfully written to {path}")
    except Exception as e:
        print(f"Error writing to {path}: {e}")



def measure_performance(func, *args, **kwargs):
    tracemalloc.start()
    start_time = time.perf_counter()

    result = func(*args, **kwargs)

    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Thời gian chạy: {end_time - start_time:.6f} giây")
    print(f"Dung lượng bộ nhớ hiện tại: {current / 1024:.2f} KB")
    print(f"Dung lượng bộ nhớ tối đa: {peak / 1024:.2f} KB")

    return result

def getTestcase():
    if len(sys.argv) < 2:
        print("Error: Please provide a valid testcase number as an argument.")
        sys.exit(1)  # Exit the program with an error status

    try:
        testcase = int(sys.argv[1])  # Convert argument to integer
    except ValueError:
        print("Error: Testcase must be an integer.")
        sys.exit(1)

    if testcase <=0 or testcase >4:
        print("Testcase must be in [1,2,3,4]")
        sys.exit(1)
    return testcase