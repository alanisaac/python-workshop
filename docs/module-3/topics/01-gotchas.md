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

One of the early concepts many developers encounter in Python is the idea of "**truthiness**".  In Python, `if` and `while` operators evaluate according to the rules of [truth value testing](https://docs.python.org/3/library/stdtypes.html#truth-value-testing).  Not only are the boolean values `True` and `False` _truthy_ and _falsy_ respectively, but Python considers "empty" values like `[]`, `{}`, `None`, `''`, and `0` _falsy_ as well.  An easy way to know if something is truthy or falsy is to use the built-in `bool()` function:

```py
>>> bool([])
False
>>> bool(["a"])
True
```

Simple enough!  But it can be easy to forget how this affects complex boolean conditions.  For example, say we have a function to save user data to a file if that user data is valid:

```py
def save_user_to_file(user: User) -> None:
    ...

def save_user_if_valid(self, user: Optional[User]) -> None
    if user and user.has_first_name:
        save_user_to_file(user)
```

Now maybe we want to refactor this function to return whether the user was valid.  Is this correct?

```py
def save_user_to_file(user: User) -> None:
    ...

def save_user_if_valid(self, user: Optional[User]) -> bool
    user_is_valid = user and user.has_first_name
    if user_is_valid:
        save_user_to_file(user)

    return user_is_valid
```

What's wrong with this function?  Coming from other languages, it might be easy to forget that the expression after an `if` statement _does not necessarily evaluate to a boolean_.  It is the `if` statement itself that checks the truthiness of the expression, which may be any value.  (Fortunately, using type hints can help us avoid these kinds of mistakes!)

## Multiple Inheritance, super(), and MRO

Python supports the concept of **multiple inheritance**: that is, a class may inherit features from more than one parent class.

But multiple inheritance has what's known as the "diamond dependency problem".  Take the situation below, where class dependencies form a diamond:

```py
class A:
    def do_thing(self):
        print('From A')


class B(A):
    def do_thing(self):
        print('From B')


class C(A):
    def do_thing(self):
        print('From C')


class D(B, C):
    pass


d = D()
d.do_thing()
```

What will happen when this module is run?  To see for yourself, you can run:

```sh
python docs/module-3/diamond.py
```

The simple solution here is that Python chooses the first implementation of the method that is in the list of inherited classes.  In this case, since we define `class D(B, C)`, `B`'s function is chosen.  You can test this out by swapping the order of `B` and `C`.

Now, let's introduce **super**.  You might be familiar already with the `super` keyword in simple cases.  In languages with single inheritance, the `super` (or similar keyword like `base`) calls the implementation of the parent class, allowing you to, for example, initialize attributes of a parent class and the derived class:

```py
class Location:
    def __init__(self, coordinates: Coordinates) -> None:
        self.coordinates = coordinates

class Site(Location):
    def __init__(
        self, 
        coordinates: Coordinates,
        inventory: float
    ) -> None:
        super().__init__(coordinates)

        self.inventory = inventory
```

Let's go back to our diamond dependency.  With the original order of `B, C`, what happens if add in `super` to `B`'s implementation:

```py
class B(A):
    def do_thing(self):
        print('From B')
        super().do_thing()
```

Run it again, and you might notice something peculiar.  Although `B` does not inherit from `C`, `super` is still calling `C`'s function.  Try instantiating `B` on its own, and running the same thing.  Why does it now call `A`?

```py
b = B()
b.do_thing()
```

This behavior because Python uses a specific algorithm for it's **method resolution order** (MRO) that looks at the entire dependency graph of a class before deciding on the correct order.  You can view a class's MRO with the `__mro__` attribute like so:

```py
d = D()
print(d.__mro__)
```

> Try guessing what happens when you print the `__mro__` for `B`.  Then try it out!  Did it match your expectation?

The consequence of this are that the behavior of `super` can _change_ without changing a classes direct ancestors.  There is some agreement that it is misnamed, and should have a name indicating it's calling the "next method" in the MRO.

The takes on this in the ecosystem range from: 

- Considering this a "superpower" of Python ([article](https://rhettinger.wordpress.com/2011/05/26/super-considered-super/), [paired PyCon talk](https://www.youtube.com/watch?v=xKgELVmrqfs))
- Considering it "harmful": difficult to understand and use, and arguing for special rules around it ([article](https://www.youtube.com/watch?v=xKgELVmrqfs))
- Considering it a reason why you should [avoid multiple inheritance](https://stackoverflow.com/a/1259665) in the first place, or even [avoid inheritance altogether](https://news.ycombinator.com/item?id=2045304)

## Exceptions

Python exception handling is similar to many C-style programming languages, offering basic `try` / `except` / `finally` functionality.  But there are a couple usage patterns that may be different:

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

One common issue with exception handling (and _more_ exception handling introduced with the EAFP pattern) is when a `try` block can potentially catch exceptions you did not mean for it to.  For example, suppose we are trying to open a file:

```py
def print_line_count(file_path: str) -> None:
    try:
        f = open(file_path, 'r')
    except OSError:
        print('cannot open', file_path)
    else:
        print(file_path, 'has', len(f.readlines()), 'lines')
        f.close()
```

The `close` function can conceivably also throw an `OSError`.  Compare this implementation to:

- Putting that logic in `try`: if `close` throws an `OSError`, it might seem like we can't _open_ the file.
- Putting that logic outside the `try` / `catch` entirely: we might not have a file at that point, and cannot continue on.

## Imports

The import system in Python is _complicated_, and developers often struggle with getting imports right.  We could spend an entire workshop on this subject, but there are other topics to cover.

In lieu of explaining the entire system, I'll highlight important excerpts from the excellent blog post: [How the Python import system works](https://tenthousandmeters.com/blog/python-behind-the-scenes-11-how-the-python-import-system-works/).

### Modules

In order to talk about how the import system works, let's start by looking at the `import` statement itself.  Take a simple statement like:

```py
import sys
```

The `import` statement does three things:

1. Searches for a module
2. Creates a module object
3. Assigns the object to a variable

Let's see how this works.  In Python we can use the `type` built-in to get the type of an object.  We can, for example, do this:

```py
>>> l = list([1, 2, 3])
>>> ListType = type(l)
>>> ListType([1, 2, 3])
[1, 2, 3]
```

Note how we assign the `list` type to a `ListType` variable, then use that variable just like we would use `list` itself.  That example is trivial, but we can do the exact same thing with modules:

```py
>>> import sys
>>> ModuleType = type(sys)
>>> ModuleType
<class 'module'>
```

And now that we have a `ModuleType`, we can create our own:

```py
>>> m = ModuleType('m')
>>> m
<module 'm'>
```

We can check what the module looks like with `__dict__`:

```py
>>> m.__dict__
{'__name__': 'm', '__doc__': None, '__package__': None, '__loader__': None, '__spec__': None}
```

That dictionary may not look special, but a module's dictionary is incredibly important.  It's actually the same dictionary that holds global variables (`globals()`).

When Python imports a Python file, it creates a new module object and then executes the contents of the file using the dictionary of the module object as the dictionary of global variables.  That's how global attributes like `__name__` work: they're ultimately the attributes of the currently executing module object.

### Packages

Let's try importing a real package, and looking at some of its attributes:

```py
>>> import collections.abc
>>> collections.__path__
['C:\\Python38\\lib\\collections']
>>> collections.abc.__package__
'collections'
>>> [key for key in collections.__dict__.keys() if not key.startswith("_")]
['deque', 'defaultdict', 'OrderedDict', 'namedtuple', 'Counter', 'ChainMap', 'UserDict', 'UserList', 'UserString', 'abc']
```

Notice how `abc` (along with other classes and functions) are simply attributes of the `collections` module.

The important thing to understand about modules and packages is that they are not special or magic: they're just objects with attributes.

### Finding Modules

_TODO: sys.path_

See also: [Python docs on `import`](https://docs.python.org/3/reference/import.html)