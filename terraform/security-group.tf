module "security_group" {
  source = "github.com/davidshare/terraform-aws-modules//security_group?ref=security_group-v1.0.0"

  name                   = "monitoring"
  description            = "Security group for monitoring services"
  vpc_id                 = "vpc-03657981779d35a20"
  revoke_rules_on_delete = true
  tags                   = {
    Name = "monitoring"
  }
}
