# Python Workshop

This workshop is divided into three modules, each covering different topics:

- **Module 1 | Environment Setup**: how to set up your environment for Python development and packaging, including helpful tools
- **Module 2 | Coding Patterns and Practices**: a discussion of coding styles and useful language features in Python
- **Module 3 | Extensions**: additional topics in asynchronous programming and common gotchas


## Before We Get Started

### Python Version

This workshop is structured around Python 3.x and above, so make sure you're using a compatible Python version:

```py
$ python
Python 3.8.1 (tags/v3.8.1:1b293b6, Dec 18 2019, 23:11:46) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

### Tools You Will Need

- Git Bash ([install](https://git-scm.com/download/win)): _on windows only_, used as the default shell in this workshop.
- Docker ([install](https://docs.docker.com/get-docker/)): used to run a local package repository.  Note that Docker recently changed their terms of service to a subscription model for larger companies - in this workshop it is used educationally, but please make sure you're in compliance with the license if you use it beyond this workshop.

### Prompts

In some sections of the workshop, some code blocks may start with the Python interpreter prompt (`>>>`):

```py
>>> import mypy
```

Other code blocks may not.  Be on the lookout for the interpreter prompt as a signal you should enter your current Python interpreter.

### Notes on this Workshop

- The workshop is structured around components of a distance matrix calculator because:
  - It is (hopefully) reasonably familiar
  - It is simple enough to discuss in a workshop setting, but complex enough to use for examples of programming paradigms
  - It is embarassingly parallel, so we could use it for extensions on parallelization down the road
- The packaging and codebase for this workshop does not work out of the box!  We will create or fill in parts of it as we go.
- There are many tools in the Python ecosystem, and we can't cover all of them!  The workshop will try to cover categories of tools and ways of doing things but there are often alternatives.  We'll try to touch on alternatives when they come up, and there are many links to moree documentation or discussion.