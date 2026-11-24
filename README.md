# Experiment No. 15: Automatic vs. Manual Garbage Collection Analysis

**Course Outcome:** CO-5  
**Student:** Vastav Nandedkar  
**Institution:** School of Computing, MIT Art, Design and Technology University, Pune  

## Aim
Evaluate Python's automatic garbage collection mechanism by experimenting with manual garbage collection using the `gc` module and analyzing its impact on memory usage and performance.

## Problem Statement
Write a Python program using the built-in `gc`, `tracemalloc`, and `time` modules to:
1. Inspect default garbage collector status, generation counts (`gc.get_count()`), and thresholds (`gc.get_threshold()`).
2. Create cyclic object references (which reference counting alone cannot immediately reclaim) and measure peak/current memory allocation.
3. Compare memory usage and execution runtime across two modes:
   - **Automatic Garbage Collection** (`gc.enable()`)
   - **Manual Garbage Collection** (`gc.disable()` followed by explicit `gc.collect()` calls)

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/Experiment-15-Garbage-Collection.git
   cd Experiment-15-Garbage-Collection
   ```
2. Run the script:
   ```bash
   python gc_evaluation.py
   ```
