resource "aws_ecr_repository" "repos" {
  for_each = toset(["capstone-api", "capstone-frontend"])

  name                 = each.value
  image_tag_mutability = "MUTABLE"
  force_delete         = true # demo stack — let terraform destroy remove images too

  image_scanning_configuration {
    # ECR's own scan on push, in addition to the Trivy gate in CI —
    # defence in depth, and it catches images pushed outside the
    # pipeline.
    scan_on_push = true
  }
}

resource "aws_ecr_lifecycle_policy" "repos" {
  for_each   = aws_ecr_repository.repos
  repository = each.value.name

  # Keep the last 10 images; expire the rest so storage doesn't creep.
  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "keep last 10 images"
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = 10
      }
      action = { type = "expire" }
    }]
  })
}
