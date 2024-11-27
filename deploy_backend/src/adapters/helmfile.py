from config import settings
from adapters.shell import Shell, ShellExecutionResult


class Helmfile:
    def __init__(self, deployment_id: str):
        self.deployment_id = deployment_id
        self.shell = Shell()

    def apply(self) -> ShellExecutionResult:
        return self.shell.call_in_shell(
            command="helmfile apply",
            cwd=f"{settings.deployments_dir}/{self.deployment_id}",
            timeout=settings.deployment_timeout,
        )

    # def lint(self) -> ShellExecutionResult:
    #    return self.shell.call_in_shell(
    #        command="helmfile lint",
    #        cwd=f"{settings.deployments_dir}/{self.deployment_id}",
    #        timeout=settings.deployment_timeout,
    #    )
