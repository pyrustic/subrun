"""Module to handle Pipeline commands"""
import sys
import shlex
import subprocess
import tempfile
import subrun
from subrun.error import Error
from subrun import dto


def run(*commands, input=None, cwd=None, stdin=None, stdout=None, stderr=None,
        timeout=None):
    """
    Create a pipeline of commands then run it

    [parameters]
    - *commands: Strings or lists of commands with arguments.
    Example: "python -m this", "program arg1 arg2", ...
    - input: String to send in the stdin of the new process
    - cwd: Current Working Directory
    - stdin: stdin
    - stdout: stdout
    - stderr: stderr
    - timeout: in seconds

    [return]
    An instance of the Info namedtuple
    """
    generator = create(*commands, input=input, cwd=cwd,
                       stdin=stdin, stdout=stdout, stderr=stderr)
    return wait(generator, timeout)


def ghostrun(*commands, input=None, cwd=None, timeout=None):
    """
    Create a pipeline of commands then run it in ghost mode,
    i.e. redirect output and error to DEVNULL

    [parameters]
    - *commands: Strings or lists of commands with arguments.
    Example: "python -m this", "program arg1 arg2", ...
    - input: String to send in the stdin of the new process
    - cwd: Current Working Directory
    - timeout: in seconds

    [return]
    An instance of the Info namedtuple
    """
    generator = create(*commands, input=input, cwd=cwd,
                       stdin=subprocess.DEVNULL,
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
    return wait(generator, timeout)


def capture(*commands, input=None, cwd=None, timeout=None):
    """
    Create a pipeline of commands then capture its output and error

    [parameters]
    - *commands: Strings or lists of commands with arguments.
    Example: "python -m this", "program arg1 arg2", ...
    - input: String to send in the stdin of the new process
    - cwd: Current Working Directory
    - timeout: in seconds

    [return]
    An instance of the Info namedtuple
    """
    generator = create(*commands, input=input, cwd=cwd,
                       stdin=subprocess.PIPE,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    return communicate(generator, timeout)


# ========= Base Functions ==========


def create(*commands, input=None, cwd=None,
           stdin=None, stdout=None, stderr=None,
           **popen_kwargs):
    """
    Run a pipeline of commands and return a generator to iterate over the processes created

    [parameters]
    - *commands: Strings or lists of commands with arguments.
    - input: String to send in the stdin of the new process
    - cwd: Current Working Directory
    - stdin: stdin
    - stdout: stdout
    - stderr: stderr
    - **popen_kwargs: other popen kwargs

    [return]
    A generator to iterate over the processes created
    """
    if len(commands) < 2:
        raise Error("Missing commands !")
    cached_stdout = stdout
    tf = None
    last_index = len(commands) - 1
    for i, command in enumerate(commands):
        if i == 0:
            stdout = subprocess.PIPE
            if input:
                tf = tempfile.TemporaryFile()
                tf.write(_encode_string(input))
                tf.seek(0)
                stdin = tf
        elif i == last_index:
            stdout = cached_stdout
        try:
            process = subrun.create(command, cwd=cwd, stdin=stdin,
                                    stdout=stdout, stderr=stderr,
                                    **popen_kwargs)
        finally:
            if tf:
                tf.close()
                tf = None
        stdin = process.stdout
        yield process


def wait(generator, timeout=None):
    """
    Iterate over a pipeline generator and wait for processes to terminate

    [parameters]
    - generator: the pipeline as returned by the 'create' function
    - timeout: in seconds

    [return]
    An instance of the Info namedtuple
    """
    process = None
    processes = list(generator)
    if not processes:
        raise Error("This pipeline is empty")
    return_codes = []
    timeout_expired = False
    for process in processes:
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timeout_expired = True
            process.kill()
            process.wait()
        return_codes.append(process.returncode)
    success = _pipepline_success(return_codes)
    return _create_info(process, success=success,
                        return_code=process.returncode,
                        return_codes=return_codes,
                        timeout_expired=timeout_expired)


def communicate(generator, timeout=None):
    """
    Interact with a pipeline generator

    [parameters]
    - generator: the pipeline as returned by the 'create' function
    - timeout: in seconds

    [return]
    An instance of the Info namedtuple
    """
    process = None
    processes = list(generator)
    if not processes:
        raise Error("This pipeline is empty")
    last_index = len(processes) - 1
    return_codes = []
    timeout_expired = False
    for i, process in enumerate(processes):
        if i == last_index:
            break
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timeout_expired = True
            process.kill()
            process.wait()
        return_codes.append(process.returncode)
    output, error = process.communicate()
    return_codes.append(process.returncode)
    success = _pipepline_success(return_codes)
    info = _create_info(process, success=success,
                        return_code=process.returncode,
                        output=output, error=error,
                        return_codes=return_codes,
                        timeout_expired=timeout_expired)
    return info


# =========== Internals ============


def _create_info(process, success=None, return_code=None,
                 output=None, error=None, return_codes=None,
                 timeout_expired=None):
    info = dto.PipelineInfo(process, success, return_code,
                            output, error, return_codes,
                            timeout_expired)
    return info


def _prepare_command(command):
    if not command:
        raise Error("Missing command")
    if isinstance(command, str):
        command = shlex.split(command, comments=False, posix=True)
    head = command[0]
    if head == "python" and sys.executable:
        command[0] = sys.executable
    return command


def _pipepline_success(return_codes):
    for code in return_codes:
        if code != 0:
            return False
    return True


def _encode_string(data):
    if data and not isinstance(data, (bytes, bytearray)):
        try:
            data = data.encode("utf-8")
        except Exception as e:
            msg = "Failed to encode data"
            raise Error(msg) from None
    return data
