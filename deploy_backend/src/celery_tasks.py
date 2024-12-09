from celery_app import app
from adapters.helmfile import Helmfile
from adapters.backend import Backend
from schemas import DeploymentStatus, DeploymentResult, DeploymentID
import logging


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


@app.task(queue="deployments")
def deploy(deployment_id: str) -> DeploymentResult:
    helmfile = Helmfile(deployment_id=deployment_id)
    backend = Backend(deployment_id=deployment_id)

    if not backend.update_status(
        deploy_result=DeploymentResult(
            status=DeploymentStatus.in_process,
            msg=None,
            stderr=None,
        )
    ):
        msg = "Can't connect to the backend to update the status"
        logger.error(msg)
        return DeploymentResult(
            status=DeploymentStatus.failed,
            msg=msg,
            stderr=None,
        )

    apply_result = helmfile.apply()

    if apply_result.exit_code != 0:
        msg = "helmfile apply command failed"
        deploy_result = DeploymentResult(
            status=DeploymentStatus.failed,
            msg=msg,
            stderr=apply_result.stderr,
        )
        backend.update_status(deploy_result=deploy_result)
        logger.error(msg=msg, extra={"details": apply_result.stderr})
        return deploy_result
    deploy_result = DeploymentResult(
        status=DeploymentStatus.success,
        msg="Deployed",
        stderr=None,
    )
    backend.update_status(deploy_result=deploy_result)
    logger.info(f"Deployment {deployment_id} was successfull")
    return deploy_result


@app.task(queue="deployments")
def uninstall(deployment_id: str) -> DeploymentID:
    helmfile = Helmfile(deployment_id=deployment_id)
    destroy_result = helmfile.destroy()

    if destroy_result.exit_code != 0:
        logger.error(
            msg="helmfile destroy command failed",
            extra={"details": destroy_result.stderr},
        )
        raise Exception(destroy_result.stderr)
    logger.info(f"Deployment {deployment_id} uninstalled successfully")
    return DeploymentID(deployment_id=deployment_id)
