# Remote state, same pattern as the cloud-resume project: S3 bucket +
# DynamoDB lock table. Values are supplied at init time so the config
# stays account-agnostic:
#
#   terraform init \
#     -backend-config="bucket=<your-state-bucket>" \
#     -backend-config="key=k8s-devops-capstone/terraform.tfstate" \
#     -backend-config="region=<region>" \
#     -backend-config="dynamodb_table=<your-lock-table>"
terraform {
  backend "s3" {}
}
