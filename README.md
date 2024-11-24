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
 * admin - full access to all routers
 * user - can only get all available applications, view all versions of the applicatiuon and deploy/update/delete its own application



2. Delete user `DELETE /v1/users/{user_id}`
3. Get user `GET /v1/users/{user_id}`
4. Update user partially `PATCH /v1/users/{user_id}`


#### Login

1. Login and get a token `POST /v1/token`
2. Refresh the roken `POST /v1/refresh_token`
3. Logout `POST /v1/logout`



## DEBUG

#### How to connect to mongodb:
```shell
docker exec -ti master_work-mongosh-1 mongosh mongodb://backend:backend-pass@master_work-mongodb-1:27017/backend --authenticationDatabase=admin
```