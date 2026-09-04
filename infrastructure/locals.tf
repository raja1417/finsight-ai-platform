locals {
  name_prefix = "finsight-${var.environment}"
  common_tags = {
    Application = "finsight"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}
