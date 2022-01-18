# Subrun
**An elegant API to safely start and communicate with processes in Python.**

This project is part of the [Pyrustic Open Ecosystem](https://pyrustic.github.io).
> [Installation](#installation) . [Demo](#demo) . [Latest](https://github.com/pyrustic/subrun/tags) . [Documentation](https://github.com/pyrustic/gaspium/tree/master/docs#readme)

## Table of contents
- [Overview](#overview) 
- [Operations](#operations) 
  - [Run](#run)
  - [Ghostrun](#ghostrun) 
  - [Capture](#capture) 
- [Base functions](#base-functions)
- [Pipeline](#pipeline)
- [Installation](#installation)
- [Demo](#demo)


# Overview
**Python** comes with the [subprocess](https://docs.python.org/3/library/subprocess.html) module that allows to spawn new processes. In a unified module, **subprocess** provides [enhancements](https://www.python.org/dev/peps/pep-0324/#motivation) over previous functions for the same task.

Based on the **subprocess** module, **Subrun** is a library that makes convenience and security a priority for spawning new processes. With **Subrun**, commands are provided as strings (or as a sequence of strings) that are [safely](https://stackoverflow.com/questions/3172470/actual-meaning-of-shell-true-in-subprocess) executed without involving the system [shell](https://en.wikipedia.org/wiki/Shell_(computing)) and a consistent [NamedTuple](https://stackoverflow.com/questions/2970608/what-are-named-tuples-in-python) is returned to give you useful information about what just happened (success boolean, return codes from each process of a pipeline, boolean timeout_expired, et cetera).

The library is made up of two categories of functions:
- Three functions that synthesize the operations you will need to perform: **run**, **ghostrun**, and **capture**.
- Three base functions that helped build the previous functions: **create**, **wait**, and **communicate**.

These functions, originally designed to spawn one process at a time, are **mirrored** in `subrun.pipeline`, a module dedicated to the [pipeline](https://en.wikipedia.org/wiki/Pipeline_(Unix)) mechanism.

# Operations
Let's take a look at **run**, **ghostrun**, and **capture**, three convenience functions that attempt to synthesize use cases into three eponymous operations.

## Run

Use the **run** function to spawn a new process that a user can interact with from the command line. This function returns a NamedTuple with useful information (e.g., the return code, et cetera).

```python
import subrun

command = "python -m this"
subrun.run(command)  # returns a NamedTuple
```
> **Note:** **Subrun** recognizes the `python` command and replaces it with the fully-qualified path of the executable binary for the current Python interpreter.

The **run** function also accepts these keywords-arguments: `input`, `cwd`, `stdin`, `stdout`, `stderr`, and `timeout`.

### Example
**hello.py:** Simple program that asks for your name and gender, then greets you.
```python
# hello.py
name = input()
gender = input()
msg = "Hello {} ! You are a {} !".format(name, gender)
print(msg)

```

**script.py:** Simple script that uses subrun to run hello.py and programmatically send it an arbitrary name and gender.
```python
# script.py
import subrun

command = "python -m hello"
subrun.run(command, input="Alex\nMale")
# note that you can also set the 'cwd' parameter 
# (current working directory)

# also, in this specific example,
# if you don't set the 'input' programmatically,
# it will be prompted to the user
```

**command line:** Let's run script.py !
```bash
$ python -m script
Hello Alex ! You are a Male !
```


> **Read the [modules documentation]() or play with the [demo]().**


## Ghostrun
Use the **ghostrun** function to run a command without any feedback. **Ghostrun** is like the **run** function with one twist: `stderr` and `stdout` are redirected to [devnull](https://en.wikipedia.org/wiki/Devnull). This function returns a NamedTuple with useful information (e.g., the return code of the process, the `success` boolean, et cetera).

**script.py:** This script uses subrun to ghostrun the command "python -m this". 
```python
# script.py
import subrun

command = "python -m this"
subrun.ghostrun(command)  # returns a NamedTuple instance
```

**command line:** Let's run script.py !
```bash
$ python -m script
$
```

> **Read the [modules documentation]() or play with the [demo]().**

## Capture
Use the **capture** function to run and capture the output of a command. This function returns a NamedTuple instance with useful information (e.g., the return code of the process, the `stdout` data, the `stderr` data, et cetera).

```python
# script.py
import subrun

command = "python -m this"
info = subrun.capture(command)  # returns a NamedTuple instance

# info.output contains the Zen Of Python as encoded bytes
```

> **Read the [modules documentation]() or play with the [demo]().**

# Base functions
The **run**, **ghostrun**, and **capture** functions use three base functions:
- **create:** Run a command and return a process object.
- **wait:** Wait for a process to terminate.
- **communicate:** Interact with a process.

The **run** and **ghostrun** functions use **create** and **wait** base functions. The **capture** function use **create** and **communicate** base functions.

## Example
```python
import subrun

# === Create and Wait ===
# Command
command = "python -m this"
# Create the process with the command
process = subrun.create(command)
# Wait the process to end
info = subrun.wait(process)

# === Create and Communicate ===
# Command
command = "python -m hello"
# Create the process with the command
process = subrun.create(command)
# Capture the output of the process
info = subrun.communicate(process, input="Alex\nMale")
```

> **Read the [modules documentation]() or play with the [demo]().**

# Pipeline
The `subrun.pipeline` module reproduces the same API as in `subrun` with a twist: you must provide more than one command which will be chained and executed.

## Example
The **run**, **ghostrun**, and **capture** functions are defined in the `subrun.pipeline` module to process a pipeline of commands:

```python
from subrun import pipeline

command1 = "python -m hello"
command2 = "program arg1 arg2"
command3 = "/path/to/program --arg data"

# === Run ===
# Run three commands pipeline. A NamedTuple instance is returned
pipeline.run(command1, command2, command3, input="Alex\nMale")

# === Ghostrun ===
# Ghostrun three commands pipeline. A NamedTuple instance is returned
pipeline.ghostrun(command1, command2, command3)

# === Capture ===
# Capture three commands pipeline. A NamedTuple instance is returned
info = pipeline.capture(command1, command2, command3)

```
The **create**, **wait**, and **communicate** base functions are also defined in the `subrun.pipeline` module to process a pipeline of commands:

```python
from subrun import pipeline

command1 = "python -m hello"
command2 = "program arg1 arg2"
command3 = "/path/to/program --arg data"

# === Create and Wait ===
# Create a generator so that you can iterate over created processes
generator = pipeline.create(command1, command2, command3)
# Wait the process to end
pipeline.wait(generator)

# === Create and Communicate ===
# Create a generator so that you can iterate over created processes
generator = pipeline.create(command1, command2, command3)
# Capture the output of the process
pipeline.communicate(generator)
```

> **Read the [modules documentation]() or play with the [demo]().**


# Installation
**Gaspium** is **cross platform** and versions under **1.0.0** will be considered **Beta** at best. It is built on [Ubuntu](https://ubuntu.com/download/desktop) with [Python 3.8](https://www.python.org/downloads/) and should work on **Python 3.5** or **newer**.

## For the first time

```bash
$ pip install gaspium
```

## Upgrade
```bash
$ pip install gaspium --upgrade --upgrade-strategy eager

```

# Demo
A demo is available to play with as a **Github Gist**. Feel free to give a feedback in the comments section.

**Play with the [Demo](https://gist.github.com/pyrustic/c05dc63b5e808c2695e775da5a6d0d7f).**

<br>
<br>
<br>

[Back to top](#readme)
