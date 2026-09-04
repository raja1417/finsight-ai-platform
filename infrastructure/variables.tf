variable "environment" {
  description = "Deployment environment."
  type        = string

  validation {
    condition     = contains(["dev", "prod"], var.environment)
    error_message = "environment must be dev or prod."
  }
}

variable "aws_region" {
  description = "AWS region for application infrastructure."
  type        = string
  default     = "us-east-1"
}

variable "azure_location" {
  description = "Azure location reserved for multi-cloud resources."
  type        = string
  default     = "eastus"
}

variable "vpc_cidr" {
  description = "CIDR range for the application VPC."
  type        = string
}

variable "cluster_role_arn" {
  description = "Existing IAM role ARN assumed by the EKS control plane."
  type        = string
}

variable "node_role_arn" {
  description = "Existing IAM role ARN assumed by EKS worker nodes."
  type        = string
}

variable "node_instance_types" {
  description = "EC2 instance types for EKS nodes."
  type        = list(string)
}

variable "node_desired_size" {
  description = "Desired EKS node count."
  type        = number
}

variable "node_min_size" {
  description = "Minimum EKS node count."
  type        = number
}

variable "node_max_size" {
  description = "Maximum EKS node count."
  type        = number
}

variable "rds_instance_class" {
  description = "RDS instance class."
  type        = string
}

variable "rds_master_username" {
  description = "RDS master username; the password is managed by AWS Secrets Manager."
  type        = string
  sensitive   = true
}
