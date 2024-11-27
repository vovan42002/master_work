import yaml
import os
from config import settings


def generate_values_file_and_save(
    parameters: dict,
    deployment_id: str,
):
    file = f"{settings.deployments_dir}/{deployment_id}/values.yaml"
    os.makedirs(f"{settings.deployments_dir}/{deployment_id}", exist_ok=True)
    with open(file, "w+") as yaml_file:
        yaml.dump(
            parameters,
            yaml_file,
            sort_keys=False,
            default_flow_style=False,
        )

    return True


def generate_helmfile_and_save(
    helm_registry: str,
    username: str,
    password: str,
    deployment_id: str,
    namespace: str,
    installed: bool,
    application_name: str,
    version: str,
    values_file: str,
):
    is_oci = "https" not in helm_registry
    structure = {
        "helmDefaults": {
            "wait": True,
            "historyMax": 3,
            "atomic": True,
            "timeout": 120,
            "createNamespace": False,
        },
        "repositories": [
            {
                "name": "common",
                "url": helm_registry,
                "oci": is_oci,
                "username": username,
                "password": password,
            }
        ],
        "releases": [
            {
                "name": deployment_id,
                "namespace": namespace,
                "installed": installed,
                "chart": f"common/{application_name}",
                "version": version,
                "values": [values_file],
            }
        ],
    }

    file = f"{settings.deployments_dir}/{deployment_id}/helmfile.yaml"
    os.makedirs(f"{settings.deployments_dir}/{deployment_id}", exist_ok=True)
    with open(file, "w+") as yaml_file:
        yaml.dump(
            structure,
            yaml_file,
            sort_keys=False,
            default_flow_style=False,
        )

    return True


def save_templated_files(
    deployment_id: str,
    installed: bool,
    application_name: str,
    version: str,
    parameters: dict,
):
    generate_helmfile_and_save(
        helm_registry=settings.helm_registry_url,
        username=settings.helm_registry_username,
        password=settings.helm_registry_username_password,
        deployment_id=deployment_id,
        namespace=settings.kubernetes_namespace,
        installed=installed,
        application_name=application_name,
        version=version,
        values_file="values.yaml",
    )
    generate_values_file_and_save(
        parameters=parameters,
        deployment_id=deployment_id,
    )
