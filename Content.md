### 1. Welcome to course
### 2. Materials: Delete/destroy all the AWS resources every time you do not use them
### 3. How to start kubernetes cluster on AWS

* **install** binaries:
   - kops
   - terraform v12
   - awscli
* create **S3 bucket** (unique across entire AWS)
* generate **SSH key** pair
* make sure you got your **own domain name**

```bash
SSH_KEYS=~/.ssh/udemy_devopsinuse

if [ ! -f "$SSH_KEYS" ]
then
   echo -e "\nCreating SSH keys ..."
   ssh-keygen -t rsa -C "udemy.course" -N '' -f $SSH_KEYS
else
   echo -e "\nSSH keys are already in place!"
fi

export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY="..."
export AWS_DEFAULT_REGION="eu-central-1"

echo -e "\nCreating kubernetes cluster ...\n"
 
kops create cluster \
--cloud=aws \
--name=course.devopsinuse.com \
--state=s3://course.devopsinuse.com \
--authorization RBAC \
--zones=eu-central-1a \
--node-count=2 \
--node-size=t2.micro \
--master-size=t2.micro \
--master-count=1 \
--dns-zone=course.devopsinuse.com \
--out=terraform_code \
--target=terraform \
--ssh-public-key=~/.ssh/udemy_devopsinuse.pub

cd devopsinuse_terraform
terraform init
terraform validate                  # -> thrown me some errors
terraform 0.12upgrade         # <- this command fix some of the errors
terraform validate      
sed -i 's/0-0-0-0--0/kops/g' kubernetes.tf

terrafrom validate       # -> this time it passed with no errors
terraform plan
```
### 4. How to create Hosted Zone on AWS
### 5. How to setup communication kops to AWS via aws
### 6. Materials: How to install KOPS binary
### 7. How to install kops
### 8. How to create S3 bucket in AWS
### 9. Materials: How to install TERRAFORM binary
### 10. How to install Terraform binary
### 11. Materials: How to install KUBECTL binary
### How to install Kubectl binary
### Materials: How to start Kubernetes cluster
### How to lunch kubernetes cluster on AWS by using kops and terraform
### Materials: How to run Jupyter Notebooks locally as Docker image
### How to Jupyter Notebook in Docker on local
### How to deploy Jupyter Notebooks to Kubernetes AWS (Part 1)
### Materials: How to deploy Juypyter Notebooks to Kubernetes via YAML file
### How to deploy Jupyter Notebooks to Kubernetes AWS (Part 2)
### How to deploy Jupyter Notebooks to Kubernetes AWS (Part 3)
### Materials: How to SSH to the physical servers in AWS
### How to deploy Jupyter Notebooks to Kubernetes AWS (Part 4)
### How to deploy Jupyter Notebooks to Kubernetes AWS (Part 5)
### Comparison between Jupyter Notebooks running as Docker Conatainer with Kubernete
### Materials: Install HELM binary and activate HELM user account in your cluster
### Introduction to Helm charts
### Materials: Run GOGS helm deployment for the first time
### How to use Helm for the first time
### How to understand helm Gogs deployment
### Materials: How to use HELM to deploy GOGS from locally downloaded HELM CHARTS
### How to deploy Gogs from local repository
### Materials: How to understand persistentVolumeClaim and persistentVolumes
### How to make you data persistent
### Lets summarize on Gogs helm chart deployment
### Materials: How to install HELMFILE binary to your machine
### Introduction to Helmfile
### How to deploy Jenkins by using Helmfile (Part 1)
### How to deploy Jenkins by using Helmfile (Part 2)
### Materials: Create HELMFILE specification for Jenkins deployment
### How to use helmfile to deploy Jenkins helm chart for the first time (Part 1)
### Materials: Useful commands Jenkins deployment
### How to use helmfile to deploy Jenkins helm chart for the first time (Part 2)
### Introduction to Prometheus and Grafana deployment by using helmfile (Grafana)
### Prometheus and Grafana deployment by using helmfile (Prometheus part)
### Prepare Helm charts for Grafana deployment by using helmfile
### Prepare Helm charts for Prometheus deployment by using helmfile
### Prepare Helm charts for Prometheus Node Exporter deployment by using helmfile
### Copy Prometheus and Grafana Helm Charts specifications to server
### Materials: Helmfile specification for Grafana and Prometheus deployment
### Process Grafana and Prometheus helmfile deployment
### Exploring Prometheus Node Exporter
### Explore Promethus Web User Interface
### Explore Grafana Web User Interface
### LoadBalancer Grafana Service
### Materials: Helmfile specification to add DokuWiki deployment
### Single LoadBalancer service type for all instances in your K8s (DokuWiki)
### Materials: Helmfile specification to add nginx-ingress Helm Chart deployment
### Nginx Ingress Controller Pod
### Configure Ingress Kubernetes Objects for Grafana, Prometheus and DokuWiki
### Important: Clean up Kubernetes cluster and all the AWS resources
### Congratulations
