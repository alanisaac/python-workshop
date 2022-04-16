# General Patterns & Gotchas

## Mutable Default Arguments

_TODO_

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