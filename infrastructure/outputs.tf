output "eks_cluster_name" {
  description = "EKS cluster name."
  value       = module.eks.cluster_name
}

output "eks_cluster_endpoint" {
  description = "EKS API endpoint."
  value       = module.eks.endpoint
  sensitive   = true
}

output "rds_endpoint" {
  description = "RDS database endpoint."
  value       = module.database.endpoint
  sensitive   = true
}

output "application_bucket_name" {
  description = "S3 bucket for application documents."
  value       = module.application_bucket.id
}
