from typing import Optional
from pydantic import BaseModel
import subprocess


class ShellExecutionResult(BaseModel):
    exit_code: int
    stderr: str
    stdout: str


class Shell:
    def __init__(self) -> None:
        pass

    def call_in_shell(
        self,
        command: str,
        env: Optional[dict] = None,
        timeout: Optional[float] = None,
        cwd: Optional[str] = None,
    ) -> ShellExecutionResult:
        try:
            process_result = subprocess.run(
                command,
                shell=True,
                text=True,
                check=True,
                capture_output=True,
                env=env,
                timeout=timeout,
                cwd=cwd,
            )
        except subprocess.CalledProcessError as e:
            schell_execution_result = ShellExecutionResult(
                exit_code=e.returncode,
                stdout=e.stdout,
                stderr=e.stderr,
            )
        else:
            schell_execution_result = ShellExecutionResult(
                exit_code=process_result.returncode,
                stdout=process_result.stdout,
                stderr=process_result.stderr,
            )
        return schell_execution_result
