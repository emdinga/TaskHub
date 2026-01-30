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
**Goal**: Externalize application configuration, securely manage secrets, and validate that the TaskHub API runs correctly in Kubernetes before introducing stateful components such as databases and caches. 

**What Was Implemented**
**Configuration Management**
Created a ConfigMap to store non-sensitive application settings:
  - Application name
  - Runtime environment
Created a Secret to store sensitive data:
  - Authentication token
Injected both ConfigMap and Secret values into the API container using environment variables

**Deployment Update**
- Updated the taskhub-api Deployment to:
- Consume configuration from ConfigMaps
- Consume sensitive values from Secrets
- Run without hardcoded values inside the container image

**Kubernetes Best Practices Applied**
- Separation of config from application code
- Immutable container image pattern
- Secure handling of secrets

