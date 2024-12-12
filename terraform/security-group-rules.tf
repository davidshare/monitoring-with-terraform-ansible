module "vpc_security_group_ingress_rule_http" {
  source = "github.com/davidshare/terraform-aws-modules//vpc_security_group_ingress_rule?ref=vpc_security_group_ingress_rule-v1.0.0"

  security_group_id = module.security_group.id
  from_port         = 80
  to_port           = 80
  ip_protocol       = "tcp"
  description       = "Allow HTTP traffic to Traefik"
  tags              = {}
  cidr_ipv4         = "0.0.0.0/0"  # Open to all IPv4

  depends_on = [module.security_group]
}

module "vpc_security_group_ingress_rule_https" {
  source = "github.com/davidshare/terraform-aws-modules//vpc_security_group_ingress_rule?ref=vpc_security_group_ingress_rule-v1.0.0"

  security_group_id = module.security_group.id
  from_port         = 443
  to_port           = 443
  ip_protocol       = "tcp"
  description       = "Allow HTTPS traffic to Traefik"
  tags              = {}
  cidr_ipv4         = "0.0.0.0/0"  # Open to all IPv4

  depends_on = [module.security_group]
}

module "vpc_security_group_ingress_rule_ssh" {
  source = "github.com/davidshare/terraform-aws-modules//vpc_security_group_ingress_rule?ref=vpc_security_group_ingress_rule-v1.0.0"

  security_group_id = module.security_group.id
  from_port         = 22
  to_port           = 22
  ip_protocol       = "tcp"
  description       = "Allow SSH access"
  tags              = {}
  cidr_ipv4         = "0.0.0.0/0"  # Open to all IPv4

  depends_on = [module.security_group]
}

module "vpc_security_group_egress_rule_all" {
  source = "github.com/davidshare/terraform-aws-modules//vpc_security_group_egress_rule?ref=vpc_security_group_egress_rule-v1.0.0"

  security_group_id = module.security_group.id
  from_port         = 0
  to_port           = 65535
  ip_protocol       = "-1"   # -1 means all protocols
  description       = "Allow all outbound traffic"
  tags              = {}
  cidr_ipv4         = "0.0.0.0/0"  # Open to all IPv4

  depends_on = [module.security_group]
}

