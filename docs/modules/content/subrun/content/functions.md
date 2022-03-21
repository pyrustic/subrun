Back to [All Modules](https://github.com/pyrustic/subrun/blob/master/docs/modules/README.md#readme)

# Module Overview

**subrun**
 
Main module

> **Classes:** &nbsp; None
>
> **Functions:** &nbsp; [\_create\_info](#_create_info) &nbsp;&nbsp; [\_encode\_string](#_encode_string) &nbsp;&nbsp; [\_join\_command](#_join_command) &nbsp;&nbsp; [\_prepare\_command](#_prepare_command) &nbsp;&nbsp; [capture](#capture) &nbsp;&nbsp; [communicate](#communicate) &nbsp;&nbsp; [create](#create) &nbsp;&nbsp; [ghostrun](#ghostrun) &nbsp;&nbsp; [run](#run) &nbsp;&nbsp; [wait](#wait)
>
> **Constants:** &nbsp; None

# All Functions
[\_create\_info](#_create_info) &nbsp;&nbsp; [\_encode\_string](#_encode_string) &nbsp;&nbsp; [\_join\_command](#_join_command) &nbsp;&nbsp; [\_prepare\_command](#_prepare_command) &nbsp;&nbsp; [capture](#capture) &nbsp;&nbsp; [communicate](#communicate) &nbsp;&nbsp; [create](#create) &nbsp;&nbsp; [ghostrun](#ghostrun) &nbsp;&nbsp; [run](#run) &nbsp;&nbsp; [wait](#wait)

## \_create\_info
None



**Signature:** (process, success=None, return\_code=None, output=None, error=None, timeout\_expired=None)





**Return Value:** None.

[Back to Top](#module-overview)


## \_encode\_string
None



**Signature:** (data)





**Return Value:** None.

[Back to Top](#module-overview)


## \_join\_command
Inverse the operation made by shlex.split 



**Signature:** (command)





**Return Value:** None.

[Back to Top](#module-overview)


## \_prepare\_command
None



**Signature:** (command)





**Return Value:** None.

[Back to Top](#module-overview)


## capture
Run a command and capture its output and error




**Signature:** (command, input=None, cwd=None, timeout=None)

|Parameter|Description|
|---|---|
|command|String or list of a command with arguments. Example: "python -m this"|
|input|String to send in the stdin of the new process|
|cwd|Current Working Directory|
|timeout|in seconds |





**Return Value:** ['An instance of the Info namedtuple']

[Back to Top](#module-overview)


## communicate
Interact with the process




**Signature:** (process, input=None, timeout=None)

|Parameter|Description|
|---|---|
|process|process object|
|input|String to send in the stdin of the new process|
|timeout|in seconds |





**Return Value:** ['An instance of the Info namedtuple']

[Back to Top](#module-overview)


## create
Run a command and return a process object




**Signature:** (command, input=None, cwd=None, stdin=None, stdout=None, stderr=None, \*\*popen\_kwargs)

|Parameter|Description|
|---|---|
|command|String or list of a command with arguments. Example: "python -m this"|
|input|String to send in the stdin of the new process|
|cwd|Current Working Directory|
|stdin|stdin|
|stdout|stdout|
|stderr|stderr|
|\*\*popen\_kwargs|other popen kwargs |





**Return Value:** ['A process object, i.e. an instance of subprocess.Popen']

[Back to Top](#module-overview)


## ghostrun
Run a command in ghost mode, i.e. redirect output and error to DEVNULL




**Signature:** (command, input=None, cwd=None, timeout=None)

|Parameter|Description|
|---|---|
|command|String or list of a command with arguments. Example: "python -m this"|
|input|String to send in the stdin of the new process|
|cwd|Current Working Directory|
|timeout|in seconds |





**Return Value:** ['An instance of the Info namedtuple']

[Back to Top](#module-overview)


## run
Run a command




**Signature:** (command, input=None, cwd=None, stdin=None, stdout=None, stderr=None, timeout=None)

|Parameter|Description|
|---|---|
|command|String or list of a command with arguments. Example: "python -m this"|
|input|String to send in the stdin of the new process|
|cwd|Current Working Directory|
|stdin|stdin|
|stdout|stdout|
|stderr|stderr|
|timeout|in seconds |





**Return Value:** ['An instance of the Info namedtuple']

[Back to Top](#module-overview)


## wait
Wait for process to terminate




**Signature:** (process, timeout=None)

|Parameter|Description|
|---|---|
|process|process object|
|timeout|in seconds |





**Return Value:** ['An instance of the Info namedtuple']

[Back to Top](#module-overview)


