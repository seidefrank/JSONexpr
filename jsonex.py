"""
Evaluate a JavaScript expression into JSON. This allows better readable
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
    "text": greeting + " " + world,
  }
"""

def jsonex_to_json(jsonex):
    import subprocess
    print(f'process.stdout.write(JSON.stringify(({jsonex}), null, "  "))')
    return subprocess.run(
        ["node"],  # run via node.js
        input=f'process.stdout.write(JSON.stringify(({jsonex}), null, "  "))',
        text=True,  # input is text
        capture_output=True  # read result from stdout
    ).stdout
