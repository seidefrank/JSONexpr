r"""
JSOX -- JavaScript Object eXpressions.

Write JSON but with JavaScript expressions, variables, and comments -- JSOX.
This function will run the JSOX string through a JavaScript interpreter
and return the result as valid JSON.

Example input string (JSOX):

  greeting = "Hello",
  addressee = "World",
  {
    "text": greeting + " " + addressee + "!",
  }

Result (JSON):

  {
    "text": "Hello World!",
  }

Copyright (c) 2022 Frank Seide. MIT License.
"""

__version__ = '0.0'
__all__ = [
    'load', 'loads', 'to_json',
]

__author__ = 'Frank Seide <frank.seide@gmail.com>'

def to_json(jsox: str, interpreter_command: list[str]=["node"]) -> str:
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

def load(fp, **kw):
    """Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
    a JSOX expression) to a Python object. ``kw`` are the same as ``json.load()``.
    """
    return loads(fp.read(), **kw)

def loads(jsox: str, **kw):
    """Deserialize ``s`` (a ``str`` instance containing a JSOX expression) to a
    Python object. ``kw`` are the same as ``json.load()``.
    """
    import json
    return json.loads(to_json(jsox), **kw)
