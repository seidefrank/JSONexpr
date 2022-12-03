r"""
JSOX -- JavaScript Object eXpressions.

Write JSON but with JavaScript expressions, variables, and comments -- JSOX.
This function will run the JSOX string through a JavaScript interpreter
and return the result as valid JSON.

Example input string (JSOX):

  greeting = "Hello",
  addressee = "World",
  {
    text: greeting + " " + addressee + "!",
  }

Result (JSON):

  {
    "text": "Hello World!",
  }
"""

__version__ = "0.0"
__all__ = ["load", "loads", "to_json"]

__author__ = "Frank Seide"
__license__ = "MIT"

import json
import shutil
import subprocess

def to_json(jsox: str, interpreter_args: list[str]=["node"]) -> str:
    """Execute ``jsox`` (a ``str`` instance containing a JSOX expression) as a single
    JavaScript expression, and serialize the result to a JSON document.
    
    ``interpreter_args`` (a ``list[str]``) is a command to invoke the JavaScript
    interpreter.
    """
    binary = shutil.which(interpreter_args[0])
    if not binary:
        raise ValueError("JavaScript interpreter not found: " + interpreter_args[0])
    interpreter_args[0] = binary
    res = subprocess.run(
        interpreter_args,  # command to run, just "node" for node.js
        # wrap the expression into code that evaluates it and writes it out as JSON
        input=f'process.stdout.write(JSON.stringify(({jsox}), null, "  "))',
        text=True,  # input is text
        capture_output=True  # read result from stdout
    )
    if res.returncode == 0:
        return res.stdout
    else:
        raise ValueError("Invalid JSOX, JavaScript interpretation failed\n" + res.stderr)

def load(fp, **kw):
    """Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
    a JSOX expression) to a Python object. ``kw`` are the same as ``json.load()``.
    """
    return loads(fp.read(), **kw)

def loads(jsox: str, **kw):
    """Deserialize ``s`` (a ``str`` instance containing a JSOX expression) to a
    Python object. ``kw`` are the same as ``json.loads()``.
    """
    try:  # try first whether it is just regular JSON
        return json.loads(jsox, **kw)
    except:  # not: interpret as JavaScript
        return json.loads(to_json(jsox), **kw)
