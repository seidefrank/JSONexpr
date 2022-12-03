r"""
JSOX -- JavaScript Object eXpressions.

JSOX is JSON but with JavaScript expressions, variables, and comments. All
valid JSON is also valid JSOX.

This module is a drop-in replacement for ``json.load()`` and ``json.loads()``.
These replacement functions run the JSOX string through a JavaScript interpreter
to convert it into a valid JSON document, which is then loaded via the original
``json.load()`` function.

Examples:

>>> s = '''
... greeting = "Hello",  // variables -- note the comma
... addressee = "World",  // comments
... {
...   text: greeting + " " + addressee + "!",  // expressions
... }
... '''
>>> import jsox
>>> j = jsox.loads(s)
>>> print(json.dumps(j, indent=True))
{
 "text": "Hello World!"
}

>>> s = '''
... welcome = true,
... // helper function
... repeat = ((n,a) => [].concat(...new Array(n).fill(a))),
... [
...   ...repeat(3, [
...     (
...       // block with a nested variable -- must be in parentheses
...       welcomeText = (welcome ? "Hello" : "Bye Bye"),
...       { text: welcomeText + " World!" }
...     )
...   ])
... ]
... '''
>>> import jsox
>>> j = jsox.loads(s)
>>> print(json.dumps(j, indent=True))
[
 {
  "text": "Hello World!"
 },
 {
  "text": "Hello World!"
 },
 {
  "text": "Hello World!"
 }
]

>>> s = '''
... // simplified from https://www.drupal.org/node/2008800
... foldersToSync = ["folder1", "folder2"],
... {"synced_folders": [
...   ...foldersToSync.map(folder => (
...    {
...      "host_path": "data/" + folder,
...      "guest_path": "/var/www/" + folder,
...      "type": "nfs"
...    }
...    ))
...  ]}
... '''
>>> import jsox
>>> j = jsox.loads(s)
>>> print(json.dumps(j, indent=True))
{
 "synced_folders": [
  {
   "host_path": "data/folder1",
   "guest_path": "/var/www/folder1",
   "type": "nfs"
  },
  {
   "host_path": "data/folder2",
   "guest_path": "/var/www/folder2",
   "type": "nfs"
  }
 ]
}
"""

__version__ = "0.0"
__all__ = ["load", "loads", "to_json"]

__author__ = "Frank Seide"
__license__ = "MIT"

import json
import shutil
import subprocess


def to_json(jsox: str, interpreter_args: list = ["node"]) -> str:
    """Execute ``jsox`` (a ``str`` instance containing a JSOX expression) as a single
    JavaScript expression, and serialize the result to a JSON document.

    ``interpreter_args`` (a ``list[str]``) is a command to invoke the JavaScript
    interpreter.
    """
    binary = shutil.which(interpreter_args[0])  # find interpreter binary
    if not binary:  # so that we can have a distinct error message if it is missing
        raise FileNotFoundError(
            "JavaScript interpreter for JSOX not found: " + interpreter_args[0])
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
        raise ValueError("JSOX JavaScript error\n" + res.stderr)


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
        pass
    return json.loads(to_json(jsox), **kw)
