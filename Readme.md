## Application deployment - manual
This section describe how to manually deploy the app into GKE or minikube clusters,

### GKE deployment
### Set variables
```sh
PROJECT_ID=gopara-tf-sandbox-gke
CLUSTER_NAME=gopara-tf-sandbox
```

### Set environment 
```sh
gcloud config set project $PROJECT_ID
gcloud container clusters get-credentials $CLUSTER_NAME
```
### Create secret
#### app connection string, root password and prometheus-exporter connection string
```sh
kubectl create secret generic db-secret \ 
--from-literal=POSTGRES_CONN_STRING='postgresql://<db app user name>:<db app user password>@db/appdb' \ 
--from-literal=POSTGRES_PASSWORD='<postgres root password>' \
--from-literal=POSTGRES_EXPORTER_CONN_STRING='postgresql://postrges:<postgres root password>@db/appdb?sslmode=disable' 
```
## Database deployment
### Label one of the nodes with 'app=db' for db pod node affinity
```sh
node_name=$(kubectl get nodes -o jsonpath={.items[0].metadata.name})
kubectl label nodes $node_name app=db
```
### Deploy config map for db
```sh
kubectl apply -f ./k8s/db-cm.yaml
```
### Deploy persistent volume for db (minikube only!)
#### GKE
```sh
kubectl apply -f ./k8s/db-pv-minikube.yaml
```

### Deploy persistent volume claim for db
#### GKE
```sh
kubectl apply -f ./k8s/db-pvc-gke.yaml
```
#### minikube
```sh
kubectl apply -f ./k8s/db-pvc-minikube.yaml
```
### Deploy service for db
```sh
kubectl apply -f ./k8s/db-svc.yaml
```
### Deploy stateful set for db
```sh
kubectl apply -f ./k8s/db-sts.yaml
```

### Deploy database appdb
```sh
kubectl exec -it db-statefulset-0 -- /bin/bash
psql -U postgres
```
```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
ALTER SYSTEM SET shared_preload_libraries='pg_stat_statements';

CREATE DATABASE appdb;
CREATE USER appuser WITH PASSWORD '<put the appuser password here>';
GRANT ALL PRIVILEGES ON DATABASE appdb to appuser;
\c appdb
GRANT USAGE, CREATE ON SCHEMA public TO appuser;
GRANT ALL ON SCHEMA public TO appuser
\q
```
```sh
exit
exit
```
### Redeploy db after configuration change
```sh
kubectl delete pod $(kubectl get pods -l app=postgres -o jsonpath="{.items[0].metadata.name}")
```

## Application deployment
### Deploy config map for app
```sh
kubectl apply -f ./k8s/app-cm.yaml
```
### Deploy service for app
```sh
kubectl apply -f ./k8s/app-svc.yaml
```
### Deploy deployment for app
```sh
kubectl apply -f ./k8s/app-deploy.yaml
```

## Application deployment - automated

### Bucket to store unit / integration test results
#### 1. GCS Bucket to store tf state file: 

  ```sh
  PROJECT_ID=$(gcloud config get-value project)
  REGION=europe-west1

  gcloud storage buckets create gs://$PROJECT_ID-gcs-cb-logs --project $PROJECT_ID --location $REGION --uniform-bucket-level-access
  ```
#### 2. Grant permissions 
Grant permissions to Cloud Build Service Account to access GCS Bucket with state file (https://cloud.google.com/docs/terraform/resource-management/store-state#before_you_begin)

```sh
PROJECT_ID=$(gcloud config get-value project)
CLOUDBUILD_SA="$(gcloud projects describe $PROJECT_ID --format 'value(projectNumber)')@cloudbuild.gserviceaccount.com"

gcloud iam roles create cb_gcs_mgt --project=$PROJECT_ID --file=./misc/cb_gcs_role.yaml

gcloud projects add-iam-policy-binding $PROJECT_ID --member=serviceAccount:$CLOUDBUILD_SA --role=projects/$PROJECT_ID/roles/cb_gcs_mgt 
```

#### 3. Deploy Cloud Build Trigger

```sh
gcloud builds triggers create github \
  --region europe-west1 \
  --repo-name="k8s-sample-app" \
  --tag-pattern='^\d+\.\d+\.\d+$' \
  --build-config=cloudbuild.yaml \
  --repo-owner=GrzegorzOpara \
  --name="app-release-pipeline" \
  --description="application release pipeline" \
  --substitutions=_APP_NAME=k8s-sample-app,_ARTIFACT_REGISTRY_REGION=europe-west1,_ARTIFACT_REGISTRY_REPO=dragon-ar,_BUCKET_NAME=gopara-tf-sandbox-gcs-cb-logs
```