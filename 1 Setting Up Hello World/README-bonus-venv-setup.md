# Setting Up a Python Virtual Environment

A **virtual environment** keeps your workshop project isolated so dependencies don’t conflict with other Python projects on your machine.

Follow these steps to set up and activate a virtual environment for the Agentic AI Workshop.

---

## 1. Check Python Installation
Make sure Python 3.9+ is installed:

```bash
python --version
# or
python3 --version
```

If you don’t have Python installed, download it from [https://www.python.org/downloads/](https://www.python.org/downloads/).

---

## 2. Create a Virtual Environment

Navigate to the folder where you want to store your workshop code, then run:

```bash
# Windows (PowerShell)
python -m venv venv

# macOS/Linux
python3 -m venv venv
```

This will create a new folder called `venv/` that contains an isolated Python installation.

---

## 3. Activate the Virtual Environment

Run the command for your operating system:

```bash
# Windows (PowerShell)
venv\Scripts\Activate

# macOS/Linux (bash/zsh)
source venv/bin/activate
```

If successful, your terminal prompt will change to show `(venv)` at the beginning.

---

## 4. Install Dependencies

Once the virtual environment is active, install the workshop dependencies:

```bash
pip install -r requirements.txt
```

This ensures all packages are installed **inside the venv**, not globally.

---

## 5. Deactivate the Virtual Environment

When you’re done, you can exit the virtual environment with:

```bash
deactivate
```

Your terminal will return to normal, and the `(venv)` prefix will disappear.

---

## 6. Reactivate Later

Whenever you come back to the project, re-run the activation command:

```bash
# Windows
venv\Scripts\Activate

# macOS/Linux
source venv/bin/activate
```

---

✅ You’re now ready to use a clean Python environment for all the workshop modules!
