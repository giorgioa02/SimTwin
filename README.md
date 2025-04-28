# Code Clone Detection Tool

This tool performs code clone detection using Z3 SMT solver for symbolic reasoning.

## Setup Instructions

### 1. Clone the repository
```bash
git clone ...
cd SimTwin
```

### 2. Create and activate the virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## Running the Tool

To run the code clone detection:

```bash
python3 SimTwin.py T2_samples/func1.py T2_samples/func2.py
```

Make sure your virtual environment is activated before running the script.

### Deactivate virtual environment (optional)
After using the tool, deactivate your virtual environment by running:

```bash
deactivate
```

---

**Note:** Ensure you have Python 3 installed on your machine.

---

# Example Test Cases

Here are some example comparisons you can run to validate the tool:

### ******* TYPE 1 EXAMPLES *******
```bash
python3 SimTwin.py T1_samples/func0.py T1_samples/func1.py
python3 SimTwin.py T1_samples/func1.py T1_samples/func2.py
python3 SimTwin.py T1_samples/func3.py T1_samples/func4.py
```

### ******* TYPE 2 EXAMPLES *******
```bash
python3 SimTwin.py T2_samples/func1.py T2_samples/func2.py
python3 SimTwin.py T2_samples/func3.py T2_samples/func4.py
```

### ******* TYPE 3 EXAMPLES *******
```bash
python3 SimTwin.py T3_samples/func1.py T3_samples/func2a.py
python3 SimTwin.py T3_samples/func1.py T3_samples/func2b.py
python3 SimTwin.py T3_samples/func2a.py T3_samples/func2b.py

python3 SimTwin.py T3_samples/func3.py T3_samples/func4.py

python3 SimTwin.py T3_samples/func5.py T3_samples/func6.py
python3 SimTwin.py T3_samples/func5.py T3_samples/func7.py
python3 SimTwin.py T3_samples/func5.py T3_samples/func8.py
python3 SimTwin.py T3_samples/func6.py T3_samples/func7.py
python3 SimTwin.py T3_samples/func6.py T3_samples/func8.py
python3 SimTwin.py T3_samples/func7.py T3_samples/func8.py
```

### ******* TYPE 4 EXAMPLES *******
```bash
python3 SimTwin.py T4_samples/func1.py T4_samples/func2.py
python3 SimTwin.py T4_samples/func3.py T4_samples/func4.py
```

### ****** NO CLONE EXAMPLES ******
```bash
python3 SimTwin.py T1_samples/func1.py T4_samples/func2.py
python3 SimTwin.py T1_samples/func1.py T4_samples/func4.py
python3 SimTwin.py T1_samples/func1.py T3_samples/func5.py
```
