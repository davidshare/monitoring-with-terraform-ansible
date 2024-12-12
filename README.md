# Monitoring with Terraform, Ansible, and Docker

## **Overview**

This project automates the deployment and monitoring of a scalable To-Do application using modern tools such as **Terraform**, **Ansible**, **Docker**, and a monitoring stack that includes **Prometheus**, **Grafana**, **Loki**, and **Traefik**.

The project includes:

1. **Infrastructure as Code (IaC)** using Terraform to provision cloud resources (EC2, Security Groups, etc.).
2. **Configuration Management** with Ansible for setting up Docker and related services.
3. **Backend (API)** and **Frontend** To-Do application deployment in containers.
4. A full-fledged **Monitoring Stack** with Traefik as the reverse proxy.

---

## **Project Structure**

```
.
├── ansible/ # Configuration Management
│ ├── files/ # Static files for configurations
│ │ ├── config/
│ │ │ ├── loki-config.yml # Loki configuration
│ │ │ ├── prometheus.yml # Prometheus configuration
│ │ │ ├── promtail-config.yml # Promtail configuration
│ │ │ └── traefik-config.yml # Traefik configuration
│ │ └── docker-compose/
│ │ ├── db.compose.yaml # Database services
│ │ ├── monitoring.compose.yaml # Monitoring stack services
│ │ ├── traefik.compose.yaml # Traefik services
│ ├── main.yaml # Entry point for Ansible playbooks
│ └── roles/ # Modular Ansible roles
│ ├── docker/ # Install Docker
│ ├── docker_compose/ # Manage Docker Compose
│ ├── letsencrypt/ # Certbot automation
│ └── services/ # Start services with Docker
│
├── terraform/ # Infrastructure provisioning
│ ├── ec2.tf # EC2 instance setup
│ ├── security-group.tf # Security groups for access control
│ ├── scripts/
│ │ └── user_data.sh # Script to initialize machines
│ └── terraform.tfstate # State file for Terraform
│
├── todo-api/ # Backend To-Do application
│ ├── app/ # Source code for API
│ ├── main.py # Entry point for the FastAPI server
│ ├── requirements.txt # Python dependencies
│ ├── Dockerfile # Docker build for backend
│ └── tests/ # Backend test suite
│
├── todo-frontend/ # Frontend To-Do application
│ ├── src/ # Next.js frontend source
│ ├── Dockerfile # Dockerfile for frontend app
│ ├── tailwind.config.ts # TailwindCSS configuration
│ └── package.json # Node.js project dependencies

```

---

## **Prerequisites**

Ensure you have the following tools installed:

1. **Terraform** (>= 1.0)
2. **Ansible** (>= 2.12)
3. **Docker** and **Docker Compose** (>= 2.0)
4. **AWS CLI** (configured with your credentials)
5. **Python 3.10+** (for the API)
6. **Node.js 18+** (for the frontend)

---

## **Deployment Instructions**

### **Step 1: Provision Cloud Infrastructure with Terraform**

1. Navigate to the `terraform` directory:
   ```bash
   cd terraform
   ```

````

2. Initialize Terraform:

 ```bash
 terraform init
````

3. Apply Terraform to provision resources:
   ```bash
   terraform apply
   ```
   - Terraform provisions EC2 instances, security groups, and network configurations.
   - Outputs the EC2 public IPs.

---

### **Step 2: Configure Servers with Ansible**

1. Navigate to the `ansible` directory:

   ```bash
   cd ../ansible
   ```

2. Update your inventory file to include the EC2 IPs (from Terraform output).

3. Run the Ansible playbook:
   ```bash
   ansible-playbook main.yaml -i inventory.ini
   ```
   - Installs Docker, sets up Docker Compose, and deploys the monitoring stack with the To-Do app.

---

### **Step 3: Verify the Deployment**

1. **Backend API**:

   - The backend should be accessible at `http://<PUBLIC_IP>:8000/docs`.

2. **Frontend**:

   - Access the frontend at `http://<PUBLIC_IP>`.

3. **Monitoring Stack**:

   - **Prometheus**: `http://<PUBLIC_IP>:9090`
   - **Grafana**: `http://<PUBLIC_IP>:3000` (default login: `admin/admin`)
   - **Loki** (logs): Integrated into Grafana.

4. **Traefik Dashboard**:
   - `http://<PUBLIC_IP>:8080/dashboard/`

---

## **Monitoring and Observability**

### **Prometheus**

- Monitors application metrics such as API request rates, response times, and resource usage.

### **Grafana**

- Visualize metrics through dashboards (configured via `grafana.ini`).

### **Loki and Promtail**

- Centralized logging solution for backend services.

### **Traefik**

- Reverse proxy and load balancer for routing requests to frontend/backend services.

---

## **To-Do Application**

### **Backend API**

- **Framework**: FastAPI
- **Features**:
  - User Authentication (JWT)
  - CRUD operations for managing To-Dos
  - SQLAlchemy for database interaction
  - Alembic for migrations
- **Endpoints**:
  - `/auth/login`
  - `/auth/register`
  - `/todos`

### **Frontend**

- **Framework**: Next.js
- **Features**:
  - Authentication pages (login/register)
  - Dashboard with To-Do management
  - Responsive UI with TailwindCSS
  - State management with React hooks

---

## **Testing**

### **Backend Tests**

Navigate to the `todo-api` folder:

```bash
cd todo-api
pytest
```

### **Frontend Tests**

Use the following command:

```bash
npm run test
```

---

## **Future Improvements**

- Add CI/CD pipelines using GitHub Actions.
- Integrate alerts with Prometheus Alertmanager.
- Enable auto-scaling for EC2 instances.

---

## **Contributing**

Contributions are welcome! Please submit a pull request with a clear description.

---

## **License**

This project is licensed under the MIT License.

---

## **Author**

David Essien ([@davidessienshare](mailto:davidessienshare@gmail.com)).
