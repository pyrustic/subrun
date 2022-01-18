Back to [All Modules](https://github.com/pyrustic/subrun/blob/master/docs/modules/README.md#readme)

# Module Overview

> **subrun.pipeline**
> 
> No description
>
> **Classes:** &nbsp; None
>
> **Functions:** &nbsp; [\_create\_info](#_create_info) &nbsp; [\_encode\_string](#_encode_string) &nbsp; [\_pipepline\_success](#_pipepline_success) &nbsp; [\_prepare\_command](#_prepare_command) &nbsp; [capture](#capture) &nbsp; [communicate](#communicate) &nbsp; [create](#create) &nbsp; [ghostrun](#ghostrun) &nbsp; [run](#run) &nbsp; [wait](#wait)
>
> **Constants:** &nbsp; None

# All Functions
[\_create\_info](#_create_info) &nbsp; [\_encode\_string](#_encode_string) &nbsp; [\_pipepline\_success](#_pipepline_success) &nbsp; [\_prepare\_command](#_prepare_command) &nbsp; [capture](#capture) &nbsp; [communicate](#communicate) &nbsp; [create](#create) &nbsp; [ghostrun](#ghostrun) &nbsp; [run](#run) &nbsp; [wait](#wait)

## \_create\_info
No description



**Signature:** (process, success=None, return\_code=None, output=None, error=None, return\_codes=None)



**Return Value:** None

[Back to Top](#module-overview)


## \_encode\_string
No description



**Signature:** (data)



**Return Value:** None

[Back to Top](#module-overview)


## \_pipepline\_success
No description



**Signature:** (return\_codes)



**Return Value:** None

[Back to Top](#module-overview)


## \_prepare\_command
No description



**Signature:** (command)



**Return Value:** None

[Back to Top](#module-overview)


## capture
Create a pipeline of commands then capture its output and error




**Signature:** (\*commands, input=None, cwd=None)

|Parameter|Description|
|---|---|
| \*commands| Strings or lists of commands with arguments.|
|Example| "python -m this", "program arg1 arg2", ...|
| input| String to send in the stdin of the new process|
| cwd| Current Working Directory|



**Return Value:** An instance of the Info namedtuple

[Back to Top](#module-overview)


## communicate
Interact with a pipeline generator




**Signature:** (generator)

|Parameter|Description|
|---|---|
| generator| the pipeline as returned by the 'create' function|



**Return Value:** An instance of the Info namedtuple

[Back to Top](#module-overview)


## create
Run a pipeline of commands and return a generator to iterate over the processes created




**Signature:** (\*commands, input=None, cwd=None, stdin=None, stdout=None, stderr=None, \*\*popen\_kwargs)

|Parameter|Description|
|---|---|
| \*commands| Strings or lists of commands with arguments.|
| input| String to send in the stdin of the new process|
| cwd| Current Working Directory|
| stdin| stdin|
| stdout| stdout|
| stderr| stderr|
| \*\*popen\_kwargs| other popen kwargs|



**Return Value:** A generator to iterate over the processes created

[Back to Top](#module-overview)


## ghostrun
Create a pipeline of commands then run it in ghost mode,
i.e. redirect output and error to DEVNULL




**Signature:** (\*commands, input=None, cwd=None)

|Parameter|Description|
|---|---|
| \*commands| Strings or lists of commands with arguments.|
|Example| "python -m this", "program arg1 arg2", ...|
| input| String to send in the stdin of the new process|
| cwd| Current Working Directory|



**Return Value:** An instance of the Info namedtuple

[Back to Top](#module-overview)


## run
Create a pipeline of commands then run it




**Signature:** (\*commands, input=None, cwd=None, stdin=None, stdout=None, stderr=None)

|Parameter|Description|
|---|---|
| \*commands| Strings or lists of commands with arguments.|
|Example| "python -m this", "program arg1 arg2", ...|
| input| String to send in the stdin of the new process|
| cwd| Current Working Directory|
| stdin| stdin|
| stdout| stdout|
| stderr| stderr|



**Return Value:** An instance of the Info namedtuple

[Back to Top](#module-overview)


## wait
Iterate over a pipeline generator and wait for processes to terminate




**Signature:** (generator)

|Parameter|Description|
|---|---|
| generator| the pipeline as returned by the 'create' function|



**Return Value:** An instance of the Info namedtuple

[Back to Top](#module-overview)


