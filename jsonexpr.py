"""
Evaluate a JSON-like JavaScript expression into JSON. This allows better readable
configuration files, allowing
* comments (!)
* variables (!!)
* expressions (!!!)

Normally, the input is mostly JSON, with a few variables and expressions
sprinkled in. This leverages the fact that (var = val, expr_of(var)) is
valid JavaScript. Example input string:

  greeting = "Hello",
  addressee = "World",
  { // JSON but allowing expressions in these variables
    "text": greeting + " " + adressee + "!",
  }

Copyright (c) 2022 Frank Seide. MIT License.
"""

def jsonexpr_to_json(jsonex):
    import subprocess
    return subprocess.run(
        ["node"],  # run via node.js
        input=f'process.stdout.write(JSON.stringify(({jsonex}), null, "  "))',
        text=True,  # input is text
        capture_output=True  # read result from stdout
    ).stdout

# That's all.
