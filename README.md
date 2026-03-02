# Task B: Event Registration with Waitlist

## System Description

In this lab, you will design and implement an **Event Registration with Waitlist** system using an LLM assistant as your primary programming collaborator. You are asked to implement a Python module that manages registration for a single event with a fixed capacity. The system must:

·  Accept a fixed capacity.

·  Register users until capacity is reached.

·  Place additional users into a FIFO waitlist.

·  Automatically promote the earliest waitlisted user when a registered user cancels.

·  Prevent duplicate registrations.

·  Allow users to query their current status.

The system must ensure that:

·  The number of registered users never exceeds capacity.

·  Waitlist ordering preserves FIFO behavior.

·  Promotions occur deterministically under identical operation sequences.

The module must preserve the following invariants:

·  A user may not appear more than once in the system.

·  A user may not simultaneously exist in multiple states.

·  The system state must remain consistent after every operation.

The system must correctly handle non-trivial scenarios such as:

·  Multiple cancellations in sequence.

·  Users attempting to re-register after canceling.

·  Waitlisted users canceling before promotion.

·  Capacity equal to zero.

·  Simultaneous or rapid consecutive operations.

·  Queries during state transitions.

The output consists of the updated registration state and ordered lists of registered and waitlisted users after each operation.

 

# How to Run Test Cases 

---

## 1. Install pytest

If you don't already have `pytest` installed, you can install it using pip:

```bash
pip install pytest
```

Verify the installation:

```bash
pytest --version
```

---

## 2. Organize Your Files

Place your implementation and test files in the same directory:

```
/project-folder
    solution.py         # your implementation
    test_solution.py    # your test cases
```

* `solution.py` contains the `is_allocation_feasible` function.
* `test_solution.py` contains the test functions.

> **Note:** If your file names are different, adjust the instructions below accordingly.

---

## 3. Update Test File Import

In `test_solution.py`, import your implementation module. For example:

```python
import pytest
from solution import is_allocation_feasible # replace "solution" with your implementation file name without .py
```

---

## 4. Run All Tests

Navigate to the folder containing the files and run:

```bash
pytest
```

Or with more detailed output:

```bash
pytest -v
```

---

## 5. Run a Specific Test Function

To run a single test function, use the `-k` option:

```bash
pytest -v -k test_name
```

---

## 6. If Your File Names Are Different

* **Test file**: If your test file doesn't match `test_*.py` or `*_test.py`, specify it explicitly:

```bash
pytest mytests.py
```

* Run a single test in a differently named file:

```bash
pytest -v mytests.py -k test_name
```

---

## Summary

1. Install `pytest`
2. Organize files
3. Update the import in test file if necessary
4. Run all tests: `pytest -v`
5. Run a single test: `pytest -v -k <test_name>`
6. Adjust commands if file names differ

---

You are ready to run the test cases for your `is_allocation_feasible` implementation!
