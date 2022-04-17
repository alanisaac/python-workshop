# General Patterns & Gotchas

## Mutable Default Arguments

One surprising behavior in Python is mutable default arguments in Python functions.  Let's try this out in the interpreter:

```py
>>> def add_one(values = []):
...     values.append(1)
...     return values
...
>>> add_one()
[1]
>>> add_one()
[1, 1]
```

Note how even though the default is defined as an empty list, calling the function multiple times results in multiple values in the list.  That's because the list instance is created _when the function is defined_.  It might make more sense why to consider this equivalent:

```py
>>> DEFAULT_VALUES = []
>>> def add_one(values = DEFAULT_VALUES):
...     values.append(1)
...     return values
...
```

So be careful when defining function defaults.  A common pattern in Python is to use `None` instead:

```py
>>> def add_one(values = None):
...     if values is None:
...         values = []
...     values.append(1)
...     return values
...
```

You can also use the **sentinel object** pattern, where instead of `None`, an object value is used for comparison.  This can be useful in situations where `None` is a valid input to a function, and you need a different value representing "nothing was passed".

> Using `None` is itself a type of sentinel pattern, where the sentinel value is `None` rather than an object.

```py
>>> sentinel = object()
>>> def add_one(values = sentinel):
...     if values is sentinel:
...         values = []
...     values.append(1)
...     return values
...
```

Note that the sentinel object pattern (as opposed to `None`) can be tricky to do well in Python (especially with type hints and copying).  There is a draft PEP that proposes making sentinels a first-class citizen in the Python ecosystem.  See [PEP-661](https://peps.python.org/pep-0661/) for more info on the challenges and the proposal.

See also: 
- [Common Gotchas - Mutable Default Arguments](https://docs.python-guide.org/writing/gotchas/#mutable-default-arguments)
- [The Sentinel Object Pattern](https://python-patterns.guide/python/sentinel-object/)

## Truthiness and Falsiness

_TODO_

## Multiple Inheritance, super(), and MRO

See also: 
- [Super Considered Super (the article)](https://rhettinger.wordpress.com/2011/05/26/super-considered-super/)
- [Super Considered Super (the talk from PyCon 2015)](https://www.youtube.com/watch?v=xKgELVmrqfs)

_TODO_

## Exceptions

_TODO_

### EAFP vs LBYL 

Several programming languages, like [C#](https://docs.microsoft.com/en-us/visualstudio/profiling/da0007-avoid-using-exceptions-for-control-flow?view=vs-2017), [Java](https://dzone.com/articles/exceptions-as-controlflow-in-java), and [Ruby](https://www.honeybadger.io/blog/benchmarking-exceptions-in-ruby-yep-theyre-slow/), discourage the use of exceptions for control flow primarily because exceptions are expensive.

These languages often encourage a pattern of checking or validating conditions before calling an exception-throwing function like this:

```py
d = {"darth vader": 0}

...

if "darth vader" in d:
    d["darth vader"] += 1
else:
    d["darth vader"] = 0
```

This pattern is known as **look before you leap** (LBYL), because we are checking for an exceptional condition before we execute code that could trigger it.

In Python, exceptions are less expensive, and sometimes used for flow control.  Some argue that if we expect the key `"darth vader"` to be in the dictionary, then the code above makes it look like we don't, as we're checking for it.  A different way to implement it would be:

```py
d = {"darth vader": 0}

...

try:
    d["darth vader"] += 1
except KeyError:
    d["darth vader"] = 0
```

Now, the code explicitly says what we think is the "exceptional" case.  This pattern is called **easier to ask forgiveness than permission** (EAFP), because we execute potentially exception-throwing code and catch it later.

Does this mean you should use exceptions or `try` / `catch` everywhere?  Exception handling patterns can still have [tradeoffs in readability and understandability](https://softwareengineering.stackexchange.com/a/351121).  But if you're coming from a language that discourages exceptions, you can view the EAFP pattern as another tool in your toolbox to use when it makes sense.

> Tip: if you _actually_ want a dictionary where non-existent keys automatically default to a certain value, check out `collections.defaultdict` ([docs](https://docs.python.org/3/library/collections.html#collections.defaultdict)).

See also: [Idiomatic Python: EAFP vs LBYL](https://devblogs.microsoft.com/python/idiomatic-python-eafp-versus-lbyl/)

### try / except else

_TODO_

## imports

_TODO_