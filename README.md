# Rprint is a faster pure python print implementation.
  - fast io storage support
  - just for fun
  - like print, but better!

```python
from rprintlib import Rprint
rprint = Rprint()
```
## Main features:

  - by default Rprint prints nothing to console(stdin)
  - You can access printed data as list anytime with rprint.ret() or str(rprint) and repr(rprint)

```python
from rprintlib import rprint #predefined rprint object
>>> rprint(12, 33, None, 'String', sep=' - ')
>>>
>>> rprint(1.23)
>>> 
>>> rprint.ret() # ->list copy
>>> ['12 - 33 - None - String\n', '1.23\n']
>>> str(rprint) # ->str
>>> '12 - 33 - None - String\n1.23\n'
>>> repr(rprint) # ->repr 
>>> "<rprintlib.rpmain.Rprint('12 - 33 - None - String\\n', '1.23\\n', sep='', end='')>"
>>> iter(rprint)
>>> <list_iterator object at 0x0000013AD992D320>
```

Why rprint?
  - It's easy to use
  - 8 times faster than print with stdout output and 10.7 without it
  - It's open-source and pure-pythonized
  - Why not?
  
### Installation

requires python 3 and up

Packages required: None, you don't need any installed

```sh
$ pip install rprintlib --upgarde
```
or
```sh
$ pip install git+https://github.com/Wirtos/Rprint
```
### FAQ
> Can i print to console or file with rprint?

yes:
```python
import sys
rprint('something', file=sys.stdout)
>>> 'something'
```
> It is possible to use starred expressions?

```python
import sys
rprint(*('sure', 'why', 'not'), sep=" - ", file=sys.stdout)
>>> 'sure - why - not'
```
> I need to type file= everytime i want to use stdout or other writable file?

Well, no. You can do something like:
```python
import sys
rprint.rtdout.stdout = sys.stdout
rprint(1)
>>> 1
rprint('rtdout - default class for storing output source')
>>> 'rtdout - default class for storing output'
```
Or even better solution:
```python
from rprintlib import sprint # predefined stdout Rprint object
sprint(2)
>>> 2
```

> So, there are two base classes?

Yep. Here's the argument list for each of them:

>Rprint(self, *objects, sep=' ', end='\n', flush=False, file=None)

>Rtdout(self)

and usable methods and attributes for Rprint:

- `.flush(self)`  flushes cached output if possible (can raise AttributeError)
- `.ret(self)` returns list of cached calls **(only if rprint.rtdout.stdout is None or False)**
- `.write(self, *objs)` don't use that one directly. It was created for using Rprint object as alternative file storage:
```python
print("something", file=rprint)
print(rprint.ret())
>>> ["something\n"]
```
or
```python
import sys 
# redefine stdout to rprint storage 
sys.stdout = rprint 
print(1)
print(2)
print(3)
sys.stdout = sys.__stdout__ #redefine stdout to default console out
print(rprint.ret())
>>> ['1\n', '2\n', '3\n']
```
- `.rtdout.stdout` Rtdout instance for current rprint object, that stores default out file value. Default to None
- `.rtdout.getstdout()` Get current stdout for rprint object

You can also use rprint with context manager:
```python
with rprint:
    rprint(12)
    print(rprint.ret())
    >>> ['12\n']
# flush() on exit. Storage is empty now
print(rprint.ret())
>>> []
```
