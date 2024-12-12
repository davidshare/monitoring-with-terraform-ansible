module "subnets" {
  source = "github.com/davidshare/terraform-aws-modules//subnet?ref=subnet-v1.0.0"

  vpc_id                  = "vpc-03657981779d35a20"
  cidr_block              = "172.31.0.0/20"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
  tags = {
    Name = "monitoring subnet"
  }
}