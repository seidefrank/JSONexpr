# JSOX—JSON with eXpressions for config files

Variables, expressions, and comments in your JSON config files. Finally.

JSON is increasingly used for configuration files written by humans. However,
originally intended for machine-to-machine communication, JSON is not very well
suited. For example, it cannot express how different values in a configuration
depend on each other, and it is not even allowed to state that in a comment.

Enter JSOX, or JavaScript Object eXpressions. JSOX extends the expressiveness
of JSON by allowing full JavaScript syntax—variables, expressions, comments—in
your JSON files. All valid JSON is valid JSOX.

The `jsox` module contains two functions, `jsox.load()` and `jsox.loads()`,
which are drop-in replacements for their JSON equivalents `json.load()` and
`json.loads()`. If your code uses a different JSON reader, you can convert a
JSOX string to valid JSON via `jsox.to_json()`.

Example JSOX:
```
// define variables, comma-separated (not: semicolon)
greeting = "Hello",  // line-end comment
addressee = "World",
{ 
  // JSON follows, but it allows expressions in these variables
  // (and you can omit the quotes for the key names as well)
  text: greeting + " " + addressee + "!",  // JavaScript expression
}
```
The functions in the `jsox` module will invoke a JavaScript interpreter to
convert this into the following proper JSON:
```
{
  "text": "Hello World!"
}
```
Notice how the expression, `greeting + " " + addressee + "!"`, was replaced by
its actual value, and how all variables and comments were removed. The result
is fully compliant JSON, acceptable to any and all JSON parsers, for example
JSON-based configuration-file readers.

### How to make your code accept JSOX instead of JSON

Assume you currently read your configuration file as follows:
```
import json
args = json.loads(open(CONFIGPATH, "r"))
```
Just change it to this:
```
import jsox  # instead of json
args = jsox.load(open(CONFIGPATH, "r"))
```
Under the hood, it is equivalent to this:
```
import json, jsox
config_ex = open(CONFIGPATH, "r").read()
config = jsox.to_json(config_ex)
args = json.loads(config)
```

### Useful tricks

You can also define functions in JSOX. Here is a collection of useful functions:
```
// Helper to repeat a list
repeat = ((n,a) => [].concat(...new Array(n).fill(a))),
// Helper to generate range [0..n-1], for use with .map()
range = (n) => [...Array(n).keys()],
```

### Prerequisites

Your system must have _node.js_ installed. You are set up correctly when the
command `node --help` responds with node.js' help screen.

For example, using the `yum` package manager, the command is:
```
sudo yum install nodejs
```
On Windows, you can use Chocolatey:
```
choco install nodejs
```
Instructions for other systems or package managers can easily be found on the Internet.

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

Variables can be defined courtesy of JavaScript's _comma operator_, which allows to
assign variables _inside_ expressions, if separated by commas.
For example, `(x = 42, y = 13, x + y)` is a valid JavaScript expression that
defines variables `x` and `y`, assigns values to them, and then evaluates to
`x + y`, all in one go. The value of this expression is `55`.

The JavaScript is interpreted using the node.js interpreter, which you must have
installed on your system.
