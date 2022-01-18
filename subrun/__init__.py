import sys
import shlex
import subprocess
import tempfile
from subrun import error
from collections import namedtuple


def run(command, input=None, cwd=None, stdin=None,
        stdout=None, stderr=None, timeout=None):
    """
    Run a command

    [parameters]
    - command: String or list of a command with arguments. Example: "python -m this"
    - input: String to send in the stdin of the new process
    - cwd: Current Working Directory
    - stdin: stdin
    - stdout: stdout
    - stderr: stderr
    - timeout: in seconds

    [return value]
    An instance of the Info namedtuple
    """
    process = create(command, input=input, cwd=cwd, stdin=stdin, stdout=stdout, stderr=stderr)
    return wait(process, timeout)


def ghostrun(command, input=None, cwd=None, timeout=None):
    """
    Run a command in ghost mode, i.e. redirect output and error to DEVNULL

    [parameters]
    - command: String or list of a command with arguments. Example: "python -m this"
    - input: String to send in the stdin of the new process
    - cwd: Current Working Directory
    - timeout: in seconds

    [return value]
    An instance of the Info namedtuple
    """
    process = create(command, input=input, cwd=cwd,
                     stdin=subprocess.DEVNULL,
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)
    return wait(process, timeout=timeout)


def capture(command, input=None, cwd=None, timeout=None):
    """
    Run a command and capture its output and error

    [parameters]
    - command: String or list of a command with arguments. Example: "python -m this"
    - input: String to send in the stdin of the new process
    - cwd: Current Working Directory
    - timeout: in seconds

    [return value]
    An instance of the Info namedtuple
    """
    process = create(command, cwd=cwd, stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return communicate(process, input=input, timeout=timeout)


# ========= Base Functions ==========


def create(command, input=None, cwd=None, stdin=None,
           stdout=None, stderr=None, **popen_kwargs):
    """
    Run a command and return a process object

    [parameters]
    - command: String or list of a command with arguments. Example: "python -m this"
    - input: String to send in the stdin of the new process
    - cwd: Current Working Directory
    - stdin: stdin
    - stdout: stdout
    - stderr: stderr
    - **popen_kwargs: other popen kwargs

    [return value]
    A process object, i.e. an instance of subprocess.Popen
    """
    command = _prepare_command(command)
    #if input and stdin:
    #    raise Error("You can't set both 'input' and 'stdin' at the same time")
    tf = None
    if input:
        tf = tempfile.TemporaryFile()
        tf.write(_encode_string(input))
        tf.seek(0)
        stdin = tf
    try:
        process = subprocess.Popen(command, stdin=stdin, stdout=stdout,
                                   stderr=stderr, cwd=cwd, **popen_kwargs)
    finally:
        if tf:
            tf.close()
    return process


def wait(process, timeout=None):
    """
    Wait for process to terminate

    [parameters]
    - process: process object
    - timeout: in seconds

    [return value]
    An instance of the Info namedtuple
    """
    timeout_expired = False
    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        timeout_expired = True
        process.kill()
        process.wait()
    success = True if process.returncode == 0 else False
    info = _create_info(process, success=success, return_code=process.returncode,
                        timeout_expired=timeout_expired)
    return info


def communicate(process, input=None, timeout=None):
    """
    Interact with the process

    [parameters]
    - process: process object
    - input: String to send in the stdin of the new process
    - timeout: in seconds

    [return value]
    An instance of the Info namedtuple
    """
    input = _encode_string(input)
    timeout_expired = False
    try:
        output, error = process.communicate(input=input, timeout=timeout)
    except subprocess.TimeoutExpired:
        timeout_expired = True
        process.kill()
        output, error = process.communicate()
    success = True if process.returncode == 0 else False
    info = _create_info(process, success=success, return_code=process.returncode,
                        output=output, error=error,
                        timeout_expired=timeout_expired)
    return info


# =========== Internals ============


def _create_info(process, success=None, return_code=None, output=None, error=None,
                 timeout_expired=None):
    Info = namedtuple("Info", ["process", "success", "return_code",
                               "output", "error", "timeout_expired"])
    token = Info(process, success, return_code, output, error, timeout_expired)
    return token


def _prepare_command(command):
    if not command:
        raise error.Error("Missing command")
    if isinstance(command, str):
        command = shlex.split(command, comments=False, posix=True)
    head = command[0]
    if head == "python" and sys.executable:
        command[0] = sys.executable
    return command


def _encode_string(data):
    if data and not isinstance(data, (bytes, bytearray)):
        try:
            data = data.encode("utf-8")
        except Exception as e:
            msg = "Failed to encode data"
            raise error.Error(msg) from None
    return data


def _join_command(command):
    """ Inverse the operation made by shlex.split """
    try:
        " ".join(shlex.quote(item) for item in command)
    except Exception as e:
        msg = "Failed to join the command"
        raise error.Error(msg) from None
