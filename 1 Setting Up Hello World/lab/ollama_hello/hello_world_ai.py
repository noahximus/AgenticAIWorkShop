# Requires Ollama installed and a model pulled locally.
# First run in terminal: `ollama run llama3`

import subprocess, sys

def ask_ollama(prompt, model="llama3"):
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return result.stdout.decode().strip()
    except subprocess.CalledProcessError as e:
        sys.stderr.write(e.stderr.decode())
        raise

print(ask_ollama("Say hello world in a fun way!"))
