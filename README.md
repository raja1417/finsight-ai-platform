# FinSight AI Platform

A minimal FastAPI service for portfolio, transaction, and analytics APIs, deployed
to Kubernetes and provisioned through reusable Terraform and GitHub Actions
workflows.

## Local development

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API is available at `http://localhost:8000`; OpenAPI documentation is at
`/docs`. Configuration uses environment variables: `ENVIRONMENT` and
`DATABASE_URL`. Do not commit a `.env` file.

## Container image

The release workflow publishes the private image
`ghcr.io/raja1417/finsight-container`, tagged with `latest` and the commit SHA.
Grant workload clusters pull access to this private GHCR package and configure
`imagePullSecrets` in the Helm values when required.

```bash
docker build -t finsight:local .
docker run --rm -p 8080:8080 finsight:local
```

## Infrastructure and deployment

Terraform wrappers in `infrastructure/` use version-pinned modules from
`raja1417/terraform-modules`. Copy `terraform.tfvars.example` before applying
and replace account and role placeholders. The RDS password is generated and
managed by AWS Secrets Manager, not supplied in tfvars.

Configure an S3 backend at initialization, selecting a distinct state key for
each environment:

```bash
terraform -chdir=infrastructure init \
  -backend-config="bucket=<state-bucket>" \
  -backend-config="key=finsight/dev/terraform.tfstate" \
  -backend-config="region=us-east-1"
terraform -chdir=infrastructure plan -var-file=dev.tfvars
```

Install the chart with a database URL injected only at deployment time:

```bash
helm upgrade --install finsight deploy/finsight-chart \
  --namespace finsight-dev --create-namespace \
  --values deploy/finsight-chart/values-dev.yaml \
  --set-string secrets.databaseUrl="$DATABASE_URL"
```

The `production` GitHub environment must have required reviewers configured.
Set `KUBECONFIG_DEV` and `KUBECONFIG_PROD` as environment/repository secrets;
the Helm deployment workflow uses them without writing credentials to source.

## Troubleshooting

- Run `helm lint deploy/finsight-chart --values deploy/finsight-chart/values-dev.yaml`
  to validate chart syntax.
- If Terraform cannot initialize, verify the S3 bucket, IAM access, and selected
  environment-specific backend key.
- If Kubernetes cannot pull the image, ensure the namespace has an image pull
  secret authorized for the private GHCR package.
