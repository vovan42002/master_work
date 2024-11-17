# System for automating the deployment and configuration of applications in K8S

### How to run?

```shell
docker compose up --build
```

## Backend

API Description

#### Schemas Router
1. Upload new scheme `POST /v1/schema`
2. Get schema specific application version `GET /v1/schema/{application_name}/{version}`
3. Delete specific application version `DELETE /v1/schema/{application_name}/{version}`
4. Update specific application version `PUT /v1/schema/{application_name}/{version}`

#### Application Router

1. Get a list of all applications `GET /v1/applications`
2. Get a list of all application versions `GET /v1/applications/{application_name}/versions`



#### Deployment Router

1. Deploy new application `POST /v1/deployments/create`
Return unique deployment identifier
2. Uninstall/delete application `DELETE /v1/deployments/{deployment_id}`
3. Update application (update version, params) `PUT /v1/deployments/{deployment_id}`

#### Users Router

1. Create new user `POST /v1/users/`
Possible roles: 
 * devops - full access to all routers
 * developer - full access to Schemas router
 * customer - can only get all available applications, view all versions of the applicatiuon and deploy/update/delete its own application



2. Block user `DELETE /v1/user/{user_id}`


#### Login

1. Login and get a token ""


## DEBUG

#### How to connect to mongodb:
```shell
docker exec -ti master_work-mongosh-1 mongosh mongodb://backend:backend-pass@master_work-mongodb-1:27017/backend --authenticationDatabase=admin
```