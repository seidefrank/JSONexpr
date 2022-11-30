# JSON expressions

Variables, expressions, and comments (!) in JSON config files. Finally.

This repository contains a near-trivial Python function, `jsonex_to_json()`,
that converts a _JSON expression_ to valid JSON. We define a JSON expression
as a JavaScript expression that evaluates to JSON. You can use variables,
JavaScript expressions, and... comments. Use this as a preprocessor
when reading JSON-based configuration files.

Example:
```
// define variables, comma-separated (not: semicolon)
greeting = "Hello",  // line-end comment
addressee = "World",
{ // JSON but allowing expressions in these variables
  "text": greeting + " " + addressee + "!",  // JavaScript expression
}
```
If you pass this to `jsonex_to_json()`, the resulting string is the following
proper JSON:
```
{
  "text": "Hello World!"
}
```
Notice how the expression, `greeting + " " + addressee + "!"`, was replaced by
its actual value, and how all variables and comments were removed. The result
is fully compliant JSON, acceptable to any and all JSON parsers, for example
JSON-based configuration-file readers.

### Prerequisites

Your system must have _node.js_ installed. You are set up correctly when the
command `node --help` responds with node.js' help screen. The Internet has
many instructions on installing node.js on your machine.

### Example use

Assume you currently read your configuration file as follows:
```
import json
config = open(CONFIGPATH, "r").read()  # read config into a string
args = json.loads(config)
```
Just change it to
```
import json
from jsonex import jsonex_to_json
config_ex = open(CONFIGPATH, "r").read()  # read config expression into a string
config = jsonex_to_json(config_ex)  # evaluate to JSON
args = json.loads(config)  # as before
```

### How does it work?

Any JSON is valid also always a valid JavaScript expression. So we simply invoke
a JavaScript interpreter to evaluate the JSON. If your JSON includes expressions,
such as `1 + 2`, the JavaScript interpreter will evaluate them. If your JSON
contains comments, no problem, the interpreter will ignore them. The result
is then formatted again into JSON/

The magic lies in JavaScript's _comma operator_. It allows to assign variables
_inside_ expressions.
For example, `(x = 42, y = 13, x + y)` is a valid JavaScript expression that
defines variables `x` and `y`, assigns values to them, and then evaluates to
`x + y`, all in one go. The value of this expression is i`55`.
