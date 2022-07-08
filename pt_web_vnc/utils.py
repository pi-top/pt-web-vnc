from os import environ
from shlex import split
from subprocess import run


def run_command(command_str: str, timeout: int) -> str:
    def __get_env():
        env = environ.copy()
        # Print output of commands in english
        env["LANG"] = "en_US.UTF-8"
        return env

    try:
        resp = run(
            split(command_str),
            check=False,
            capture_output=True,
            timeout=timeout,
            env=__get_env(),
        )
        return str(resp.stdout, "utf8")
    except Exception:
        return ""
