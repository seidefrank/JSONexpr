r"""
JSOX -- JavaScript Object eXpressions.

Write JSON but with JavaScript expressions, variables, and comments -- JSOX.
This function will run the JSOX string through a JavaScript interpreter
and return the result as valid JSON.

Example input string:

  greeting = "Hello",
  addressee = "World",
  { // JSON but allowing expressions in these variables
    "text": greeting + " " + addressee + "!",
  }

Copyright (c) 2022 Frank Seide. MIT License.
"""

__version__ = '0.0'
__all__ = [
    'load', 'loads', 'to_json',
]

__author__ = 'Frank Seide <frank.seide@gmail.com>'

def to_json(jsox: str, interpreter_command: list=["node"]) -> str:
    import subprocess
    res = subprocess.run(
        interpreter_command,  # binary to run, typ. node.js
        # wrap the expression into code that evaluates it and writes it out as JSON
        input=f'process.stdout.write(JSON.stringify(({jsox}), null, "  "))',
        text=True,  # input is text
        capture_output=True  # read result from stdout
    )
    if res.returncode == 0:
        return res.stdout
    else:
        raise ValueError(res.stderr)

def loads(jsox: str, **kw):
    import json
    return json.loads(to_json(jsox), **kw)

def load(fp, **kw):
    return loads(fp.read(), **kw)