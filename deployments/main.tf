
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.82.2"
    }
  }
}                 
provider "aws" {
  region = "us-east-1"
}

resource "aws_key_pair" "web" {
  key_name   = "test-key"
  public_key = file("/home/abhinav_007/.ssh/web_key.pub")
}

resource "aws_security_group" "ssh_access" {
  name        = "web-access-sg"
  description = "Allow standard web traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "test" {
  ami                    = "ami-0c55b159cbfafe1f0"
  instance_type          = "t2.micro"
  key_name               = aws_key_pair.web.key_name
  vpc_security_group_ids = [aws_security_group.ssh_access.id]

  tags = {
    Name        = "test"
    Environment = "Dev"
    CreatedBy   = "DemoUser"
  }

  user_data = <<-EOF
#!/bin/bash
EOF
}
