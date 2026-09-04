terraform {
  required_version = ">= 1.9.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = local.common_tags
  }
}

provider "azurerm" {
  features {}
}

module "vpc" {
  source = "git::https://github.com/raja1417/terraform-modules.git//aws/vpc?ref=v1.0.0"

  name       = local.name_prefix
  cidr_block = var.vpc_cidr
  subnets = {
    private_a = { cidr_block = cidrsubnet(var.vpc_cidr, 4, 1), availability_zone = "${var.aws_region}a" }
    private_b = { cidr_block = cidrsubnet(var.vpc_cidr, 4, 2), availability_zone = "${var.aws_region}b" }
    public_a  = { cidr_block = cidrsubnet(var.vpc_cidr, 4, 3), availability_zone = "${var.aws_region}a", public = true }
    public_b  = { cidr_block = cidrsubnet(var.vpc_cidr, 4, 4), availability_zone = "${var.aws_region}b", public = true }
  }
  create_nat_gateway = true
  tags               = local.common_tags
}

module "application_security_group" {
  source = "git::https://github.com/raja1417/terraform-modules.git//aws/security-group?ref=v1.0.0"

  name        = "${local.name_prefix}-app"
  description = "Security group for FinSight application workloads"
  vpc_id      = module.vpc.vpc_id
  ingress_rules = [
    {
      description = "HTTPS from the VPC"
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = [var.vpc_cidr]
    },
  ]
  tags = local.common_tags
}

module "eks" {
  source = "git::https://github.com/raja1417/terraform-modules.git//aws/eks?ref=v1.0.0"

  name               = local.name_prefix
  cluster_role_arn   = var.cluster_role_arn
  node_role_arn      = var.node_role_arn
  subnet_ids         = module.vpc.private_subnet_ids
  security_group_ids = [module.application_security_group.id]
  node_groups = {
    application = {
      desired_size   = var.node_desired_size
      min_size       = var.node_min_size
      max_size       = var.node_max_size
      instance_types = var.node_instance_types
    }
  }
  tags = local.common_tags
}

module "application_bucket" {
  source = "git::https://github.com/raja1417/terraform-modules.git//aws/s3?ref=v1.0.0"

  name = "${local.name_prefix}-documents"
  tags = local.common_tags
}

module "database" {
  source = "git::https://github.com/raja1417/terraform-modules.git//aws/rds?ref=v1.0.0"

  name                   = "${local.name_prefix}-database"
  db_name                = "finsight"
  username               = var.rds_master_username
  instance_class         = var.rds_instance_class
  subnet_ids             = module.vpc.private_subnet_ids
  vpc_security_group_ids = [module.application_security_group.id]
  tags                   = local.common_tags
}
