# Kubernetes Deployment Files

This directory contains Kubernetes manifests for deploying the Nepali Dating Python application.

## Files

- **deployment.yml** - Main Django app deployment with ConfigMap and Secrets
- **ingress.yml** - Ingress configuration for routing traffic
- **postgres.yml** - PostgreSQL StatefulSet for the database

## Prerequisites

1. Kubernetes cluster (v1.19+)
2. kubectl configured to access your cluster
3. NGINX Ingress Controller installed
4. Cert-manager installed (for SSL certificates)

## Before Deploying

### 1. Update Configuration Values

Edit `deployment.yml` and replace:
- `yourdomain.com` - Your actual domain name
- `SECRET_KEY` - Generate a secure key:
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- `DB_PASSWORD` - Set a strong database password
- `DB_USER` - Set your database username

### 2. Update Ingress

Edit `ingress.yml` and replace:
- `yourdomain.com` - Your actual domain names
- `letsencrypt-prod` - If using cert-manager (or remove TLS section)

### 3. Build and Push Docker Image

```bash
docker build -t prabeshdevops/nepali_dating_python:latest .
docker push prabeshdevops/nepali_dating_python:latest
```

## Deployment Instructions

### 1. Deploy Everything

```bash
# Deploy in order
kubectl apply -f deployment.yml
kubectl apply -f postgres.yml
kubectl apply -f ingress.yml
```

### 2. Verify Deployment

```bash
# Check pods
kubectl get pods -n nepali-dating

# Check services
kubectl get svc -n nepali-dating

# Check ingress
kubectl get ingress -n nepali-dating

# View logs
kubectl logs -n nepali-dating -l app=nepali-dating -f
```

### 3. Run Database Migrations

```bash
# Get the pod name
kubectl get pods -n nepali-dating -l app=nepali-dating

# Run migrations
kubectl exec -it <pod-name> -n nepali-dating -- python manage.py migrate

# Create superuser
kubectl exec -it <pod-name> -n nepali-dating -- python manage.py createsuperuser
```

### 4. Create Admin User

```bash
kubectl exec -it <pod-name> -n nepali-dating -- python manage.py createsuperuser
```

## Scaling

The deployment includes a Horizontal Pod Autoscaler (HPA) that automatically scales based on CPU and memory usage:
- Minimum replicas: 2
- Maximum replicas: 5
- Scales up when CPU > 70% or Memory > 80%

## Troubleshooting

### Pod not starting

```bash
kubectl describe pod <pod-name> -n nepali-dating
kubectl logs <pod-name> -n nepali-dating
```

### Database connection issues

```bash
# Check if postgres is running
kubectl get pods -n nepali-dating -l app=postgres

# Check postgres logs
kubectl logs postgres-0 -n nepali-dating
```

### Ingress not working

```bash
# Check ingress status
kubectl describe ingress nepali-dating-ingress -n nepali-dating

# Check ingress controller logs
kubectl logs -n ingress-nginx
```

## Resource Limits

- **Django App**: 256Mi-512Mi RAM, 250m-500m CPU
- **PostgreSQL**: 256Mi-512Mi RAM, 250m-500m CPU

Adjust in the YAML files based on your needs.

## Production Recommendations

1. Use external managed databases (AWS RDS, Google Cloud SQL)
2. Enable HTTPS/TLS encryption
3. Configure backup policies for databases
4. Use private container registries
5. Implement network policies for security
6. Use GitOps (ArgoCD, Flux) for deployments
7. Monitor with Prometheus/Grafana
8. Set up log aggregation (ELK, Loki)
