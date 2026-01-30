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

