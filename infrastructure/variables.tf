variable "project_name" {
  description = "Name used to prefix/tag all resources."
  type        = string
  default     = "k8s-devops-capstone"
}

variable "region" {
  description = "AWS region to deploy into."
  type        = string
  default     = "ca-central-1"
}

variable "cluster_version" {
  description = "Kubernetes version for the EKS control plane."
  type        = string
  default     = "1.31"
}

variable "node_instance_type" {
  description = "EC2 instance type for worker nodes. t3.medium is the practical floor for EKS — smaller instances run out of pod IPs."
  type        = string
  default     = "t3.medium"
}

variable "node_desired_size" {
  description = "Desired number of worker nodes."
  type        = number
  default     = 2
}

variable "github_repo" {
  description = "GitHub repo (owner/name) allowed to assume the deploy role via OIDC."
  type        = string
  default     = "anoop-singh02/k8s-devops-capstone"
}
