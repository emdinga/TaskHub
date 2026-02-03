### TaskHub Kubernetes Project — Stages Breakdown
TaskHub is a team task management application that allows users to create, view, and manage tasks for their teams.
The project is intentionally built and deployed on an on-prem Kubernetes cluster to demonstrate how a real business application is containerized, 
deployed, networked, and operated without cloud-managed services.

The project focuses on containerization, Kubernetes internals, networking, reliability, and operational debugging, all running on an on-prem MicroK8s cluster.

**Project Goals**
Is to create an application that will allow users to do the following:
- Users can:
  - View team tasks
  - Create new tasks
  - Track task status
- The backend exposes REST APIs for task management
- Authentication headers are required (simulating secured access)

**Architecture Overview**
- Frontend – Static UI (planned)
- API – FastAPI backend (containerized)
- Kubernetes Cluster – MicroK8s (on-prem)
- Namespace – taskhub
- Service Type – ClusterIP (internal networking)
- Ingress – NGINX (next stage)

### STAGE 1: Containerization & Basic Kubernetes Deployment
**Goal**: containerize my TaskHub application ,create core Kubernetes primitives and run workloads on an on-prem Kubernetes cluster.

**Achivement:**
- Built a FastAPI backend (taskhub-api)
- Wrote a Dockerfile
- Built the image locally and loaded it into MicroK8s containerd
- Created Kubernetes resources:
  - Namespace (taskhub)
  - Deployment
  - ClusterIP Service
- Successfully ran the pod in the cluster

**Key Kubernetes concepts practiced**
- Pods & Deployments
- Image pull policies (Never, IfNotPresent)
- On-prem container registries
- Namespace isolation
- Service discovery via ClusterIP

### STAGE 2: Internal Networking & Service Communication
**Goal**: confirm Pods can talk to services , Kubernetes DNS works and to debug networking without exposing services externally

**Achived**
- Verified pod health and scheduling
- Confirmed ClusterIP service creation
- Used Kubernetes DNS:
  - api.taskhub.svc.cluster.local
- Attempted to curl the service from inside the cluster
- Learned why production containers don’t have debugging tools
- Used a debug pod to test connectivity (best practice)

**Key Kubernetes concepts practiced**
- ClusterIP services
- Internal DNS resolution
- Pod-to-service traffic flow
- Debugging with ephemeral pods
- Immutable container philosophy

### STAGE 3: External Access & Ingress (On-Prem Kubernetes)
**Goal:** Expose the TaskHub API externally in an on-prem Kubernetes environment using an Ingress Controller, and understand how HTTP traffic flows from outside the cluster to application pods.
**Achievements**
- Created an NGINX Ingress resource for the TaskHub API
- Configured host-based routing using:
  - api.taskhub.local
- Routed external HTTP traffic to the backend via:
  - Ingress → ClusterIP Service → Pod
- Verified Ingress creation and binding to the NGINX Ingress Controller
- Exposed the application without using NodePort or cloud load balancers

**Key Kubernetes Concepts Practiced**
- Ingress vs Service responsibilities
- L7 (HTTP) routing in Kubernetes
- On-prem traffic exposure patterns
- NGINX Ingress Controller behavior
- Host-based routing and DNS concepts
- Traffic flow:
  - Client → Ingress Controller → Service → Pod

### STAGE 4: Configuration Management & Application Validation
**Goal**:Externalize application configuration, securely manage sensitive data, and validate that the TaskHub API runs correctly in Kubernetes before introducing performance and reliability enhancements such as caching and health probes. This stage focuses on making the application configuration-ready and state-aware, rather than feature-complete.

**What Was Implemented**
**Configuration Management**
- Created a ConfigMap to store non-sensitive application configuration:
    - Application name
    - Runtime environment
- Created Secrets to securely store sensitive values:
    - Authentication token
    - Database connection details
    -Injected configuration and secrets into the API container using environment variables

**Deployment Updates**
- Updated the taskhub-api Deployment to:
    - Consume configuration from ConfigMaps
    - Consume sensitive values from Secrets
    - Run without any hardcoded configuration inside the container image
    - Ensured configuration changes can be applied without rebuilding Docker images
  
**Application Validation with Stateful Database**
- Deployed PostgreSQL as a StatefulSet with persistent storage
- Provisioned storage using PersistentVolumeClaims backed by on-prem hostPath
- Exposed PostgreSQL internally via a ClusterIP Service
- Connected the TaskHub API to PostgreSQL using:
- Kubernetes DNS (postgres.taskhub.svc.cluster.local)
- Secrets for credentials
- Validated end-to-end data persistence:
    - Created tasks via the API
    - Retrieved tasks from the database
    - Confirmed data survives pod restarts

**Kubernetes Best Practices Applied**
- Separation of code and configuration
- Secure secret management (no secrets in source code or images)
- Immutable container image pattern
- Stateful workload management using StatefulSets
- Persistent storage handling in an on-prem environment
- Internal service discovery using Kubernetes DNS

## STAGE 5: Application Health & Dependency Management

**Overview**

In this stage, the focus was on stabilizing the TaskHub API running in Kubernetes by correctly handling application health checks and external dependencies (PostgreSQL and Redis). The goal was to eliminate pod restarts, probe failures, and startup race conditions, resulting in a production-ready microservice.

**Problem Statement**

Initially, the API pods experienced:

- **CrashLoopBackOff** due to database connections being initialized at import time
- **Failing liveness/readiness probes** returning `404` errors
- Unstable startup behavior when PostgreSQL or Redis were not yet ready

**Solution Implemented**

**1. Proper Health Endpoint**

- Implemented a dedicated `/health` endpoint in FastAPI
- Ensured the endpoint responds immediately without blocking on external dependencies

**2. Safe Application Startup**

- Moved database and Redis initialization out of import time
- Ensured the application can start even if dependencies are temporarily unavailable

**3. Kubernetes Probe Alignment**

- Configured **liveness** and **readiness** probes to target the correct health endpoint
- Prevented premature restarts and traffic routing before the app was ready

**4. Container Validation**

* Verified the container image directly using `kubectl run` and Python REPL
* Confirmed registered routes and FastAPI application state inside the running container

**Final State**

- API pod reaches **READY 1/1** consistently
- No CrashLoopBackOff or unexpected restarts
- PostgreSQL and Redis run independently as stable services
- TaskHub API behaves as a stateless, resilient microservice


**Key Kubernetes Concepts covered**

- Difference between **liveness** and **readiness** probes
- Why external dependencies should not be initialized at import time
- How Kubernetes reacts to probe failures
- Debugging pods using `kubectl logs`, `kubectl exec`, and ephemeral containers

### Stage 7: Monitoring with Prometheus & Grafana
**Overview**: In this stage, we integrated Prometheus and Grafana into the TaskHub Kubernetes cluster to provide real-time monitoring, metrics visualization, and alerting capabilities. The goal is to ensure observability for the API, frontend, and dependent services (PostgreSQL, Redis) and to track application performance in production.

**Components & Architecture**

- Prometheus: Collects metrics from Kubernetes pods and services.

- Grafana: Visualizes metrics through dashboards and provides alerting capabilities.

- Kubernetes Cluster: TaskHub services (API, frontend, auth, worker) run in their dedicated namespace.

- Ingress / External Access: Grafana and Prometheus dashboards are accessible externally via port-forwarding or Ingress.

- Ingress / Port-forward --> Access dashboards externally

**Implementation Details**
1. Prometheus Deployment
- Installed using Helm from the prometheus-community chart:
    - helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
      helm repo update
      kubectl create namespace monitoring
      helm install prometheus prometheus-community/prometheus -n monitoring \
      --set alertmanager.enabled=false \
      --set pushgateway.enabled=false

Configured to scrape metrics from:
- TaskHub API
- Frontend (if exposing metrics)
- Kubernetes node metrics
- Redis and PostgreSQL exporters (optional)

**2. Grafana Deployment**
Installed using Helm from the grafana chart:

    helm repo add grafana https://grafana.github.io/helm-charts
    helm repo update
    helm install grafana grafana/grafana -n monitoring \
    --set adminPassword=<secure_password> \
    --set service.type=ClusterIP
configured Prometheus as a data source.
- Created dashboards for:
  - API request rates, latencies, errors
  - Task creation/consumption metrics
  - Redis and PostgreSQL metrics

**3. Accessing Dashboards**
- Port-forwarding for local access:

  kubectl port-forward -n monitoring svc/grafana 3000:80
  kubectl port-forward -n monitoring svc/prometheus-server 9090:80

- Dashboards are available at:
  - Grafana: http://localhost:3000
  - Prometheus: http://localhost:9090

**4. Key Benefits**
- Real-time monitoring: Track application performance, API latency, and task processing.
- Alerting (future): Configure alerts for downtime, high error rates, or slow response times.
- Operational visibility: Helps detect service degradation before impacting users.
