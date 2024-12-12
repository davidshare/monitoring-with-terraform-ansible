module "ec2_instance" {
  source                      = "github.com/davidshare/terraform-aws-modules//ec2?ref=ec2-v1.0.0"

  ami                         = "ami-0453ec754f44f9a4a"
  instance_type               = "t3a.medium"
  key_name                    = "monitoring"
  subnet_id                   = module.subnets.id
  vpc_security_group_ids      = [module.security_group.id]
  associate_public_ip_address = true

  tags = {
    Name = "monitoring instance"
  }
}