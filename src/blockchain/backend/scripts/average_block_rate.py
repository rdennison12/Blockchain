import csv
import time
from blockchain.backend.blockchain.blockchain import Blockchain
from blockchain.backend.config import SECONDS

blockchain = Blockchain()

times = []
records = []
csv_file_path = "average_block_rate.csv"

try:
    print("Program running... Press Ctrl+C to stop.")
    for i in range(100):
        start_time = time.time_ns()
        blockchain.add_block(i)
        end_time = time.time_ns()

        time_to_mine = (end_time - start_time) / SECONDS
        times.append(time_to_mine)
        average_time = sum(times) / len(times)
        difficulty = blockchain.chain[-1].difficulty

        records.append({
            "block_index": i + 1,
            "difficulty": difficulty,
            "time_to_mine": time_to_mine,
            "average_time": average_time,
        })

        print(f'New block difficulty: {difficulty}')
        print(f'Time to mine a new block: {time_to_mine}s')
        print(f'Average time to add blocks: {average_time}s\n')
except KeyboardInterrupt:
    print("\nProgram interrupted by user. Terminating gracefully.")
except Exception as e:
    print(f"An unexpected error has occurred: {e}")
finally:
    if records:
        try:
            with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
                fieldnames = ["block_index", "difficulty", "time_to_mine", "average_time"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(records)
            print(f"Benchmark results successfully saved to {csv_file_path}")
        except Exception as file_err:
            print(f"Failed to write CSV output: {file_err}")