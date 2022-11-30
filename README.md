# JSONexpr—JSON with expressions for config files

Variables, expressions, and comments in your JSON config files. Finally.

This repository contains a near-trivial Python function, `jsonexpr_to_json()`,
that converts a _JSON expression_ to valid JSON. We define a JSON expression
as a JavaScript expression that evaluates to JSON. You can use variables,
JavaScript expressions, and... comments. Use this as a preprocessor
when reading JSON-based configuration files.

While JSON is meant for machine-to-machine communication, JSONexpr is for humans,
especially those who need to write JSON configuration files.

Example:
```
// define variables, comma-separated (not: semicolon)
greeting = "Hello",  // line-end comment
addressee = "World",
{ // JSON follows, but it allows expressions in these variables
  "text": greeting + " " + addressee + "!",  // JavaScript expression
}
```
If you pass this to `jsonexpr_to_json()`, the resulting string is the following
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
from jsonexpr import jsonexpr_to_json
config_ex = open(CONFIGPATH, "r").read()  # read config expression into a string
config = jsonexpr_to_json(config_ex)  # evaluate to JSON
args = json.loads(config)  # as before
```

### How does it work?

Any JSON is valid also always valid JavaScript. To be precise, it is a valid JavaScript
_expression_. Any JavaScript interpreter can ingest JSON and understand it as a valid
expression of an array or dictionary literal.

There is one difference, though, between reading JSON with a JSON parser vs. interpreting
it as JavScript: When interpreted as JavaScript, it may contain additional valid
JavaScript constructs that are not allowed in JSON. For example, basic expressions like
`1 + 1` are invalid in JSON, while a JavaScript interpreter will just compute it as `2`.
If your JSON contains comments, no problem, the interpreter will ignore them. The result
is then formatted again into JSON/

The magic lies in JavaScript's _comma operator_. It allows to assign variables
_inside_ expressions.
For example, `(x = 42, y = 13, x + y)` is a valid JavaScript expression that
defines variables `x` and `y`, assigns values to them, and then evaluates to
`x + y`, all in one go. The value of this expression is i`55`.

The JavaScript is interpreted using the node.js interpreter, which you must have
installed on your system.
