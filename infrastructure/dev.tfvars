# Replace the example account IDs and role names before applying this configuration.
environment         = "dev"
aws_region          = "us-east-1"
azure_location      = "eastus"
vpc_cidr            = "10.10.0.0/16"
cluster_role_arn    = "arn:aws:iam::123456789012:role/finsight-dev-eks-cluster"
node_role_arn       = "arn:aws:iam::123456789012:role/finsight-dev-eks-node"
node_instance_types = ["t3.medium"]
node_desired_size   = 2
node_min_size       = 2
node_max_size       = 4
rds_instance_class  = "db.t3.micro"
rds_master_username = "finsight_admin"
