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
