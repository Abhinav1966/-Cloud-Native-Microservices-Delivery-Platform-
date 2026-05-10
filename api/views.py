import os
import subprocess
import json
import shlex
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

from .models import Resource, InfrastructureRequest
from .forms import InfrastructureForm

# ==========================================
# 1. WEBSITE PAGES (The "Front Desk")
# ==========================================
def loadDashboard(request):
    return render(request, 'index.html')

def resource_api(request):
    resources = list(Resource.objects.values('name', 'type', 'status', 'icon_name'))
    for res in resources:
        res['icon_url'] = f"/static/icons/{res['icon_name']}" if res['icon_name'] else "https://img.icons8.com/color/96/amazon-web-services.png"
    return JsonResponse(resources, safe=False)

# ==========================================
# 2. USER SECURITY (Login & Signup)
# ==========================================
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'login_form': form})

# ==========================================
# 3. THE INFRASTRUCTURE BUILDER (The Core Logic)
# ==========================================
def create_server(request):
    if request.method == 'POST':
        form = InfrastructureForm(request.POST)
        if form.is_valid():
            req = form.save() 
            user_name = request.user.username if request.user.is_authenticated else "DemoUser"

            terraform_code = f"""
terraform {{
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "5.82.2"
    }}
  }}
}}                 
provider "aws" {{
  region = "{req.aws_region}"
}}

resource "aws_key_pair" "web" {{
  key_name   = "{req.project_name}-key"
  public_key = file("/home/abhinav_007/.ssh/web_key.pub")
}}

resource "aws_security_group" "ssh_access" {{
  name        = "{req.sec_group_name}"
  description = "{req.sec_group_desc}"

  ingress {{
    from_port   = {req.ingress_from_port}
    to_port     = {req.ingress_to_port}
    protocol    = "{req.ingress_protocol}"
    cidr_blocks = ["{req.ingress_cidr}"]
  }}

  egress {{
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }}
}}

resource "aws_instance" "{req.project_name}" {{
  ami                    = "{req.ami_id}"
  instance_type          = "{req.instance_type}"
  key_name               = aws_key_pair.web.key_name
  vpc_security_group_ids = [aws_security_group.ssh_access.id]

  tags = {{
    Name        = "{req.project_name}"
    Environment = "{req.environment}"
    CreatedBy   = "{user_name}"
  }}

  user_data = <<-EOF
{req.user_data_script}
EOF
}}
"""
            deploy_dir = os.path.join(settings.BASE_DIR, 'deployments')
            os.makedirs(deploy_dir, exist_ok=True)
            
            with open(os.path.join(deploy_dir, 'main.tf'), 'w') as f:
                f.write(terraform_code)

            context = {
                'tf_code': terraform_code,
                'project_name': req.project_name
            }
            return render(request, 'review_deployment.html', context)
    else:
        # We grab the dynamic key path from the form class dynamically
        form = InfrastructureForm(initial={
            'user_data_script': '#!/bin/bash\n',
            'aws_region': 'us-east-1'
        })
    return render(request, 'create_server.html', {'form': form})

# ==========================================
# 4. THE SECURE WEB TERMINAL
# ==========================================
@csrf_exempt
def terminal_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            command = data.get('command', '').strip()

            base_dir = settings.BASE_DIR
            deploy_dir = os.path.join(base_dir, 'deployments')
            plugin_dir = os.path.join(base_dir, 'terraform-plugins')
            creds_file = os.path.join(base_dir, 'aws_credentials')

            if not os.path.exists(deploy_dir):
                os.makedirs(deploy_dir, exist_ok=True)

            allowed_commands = [
                'terraform init', 'terraform plan', 
                'terraform apply', 'terraform apply -auto-approve', 
                'terraform destroy', 'terraform destroy -auto-approve', 
                'ls', 'pwd', 'whoami', 'terraform --version',
                'ls', 'pwd', 'whoami', 'terraform --version', 'ssh'
            ]
            
            is_allowed = False
            for safe_cmd in allowed_commands:
                if command.startswith(safe_cmd):
                    is_allowed = True
                    break
            
            if not is_allowed and not command.startswith('echo'):
                return JsonResponse({'output': f"Command '{command}' is not allowed for security reasons."})

            

            if command == 'terraform apply': command = 'terraform apply -auto-approve'
            if command == 'terraform destroy': command = 'terraform destroy -auto-approve'

            env = os.environ.copy()
            if os.path.exists(creds_file):
                env['AWS_SHARED_CREDENTIALS_FILE'] = creds_file
                env['AWS_REGION'] = 'us-east-1'

            safe_command_list = shlex.split(command)

            process = subprocess.run(
                safe_command_list, 
                shell=False, 
                cwd=deploy_dir, 
                capture_output=True, 
                text=True,
                env=env
            )
            
            full_output = process.stdout + process.stderr
            if not full_output:
                full_output = "Command executed (No output returned)."

            return JsonResponse({'output': full_output})

        except Exception as e:
            return JsonResponse({'output': f"PYTHON SERVER ERROR: {str(e)}"})
            
    return JsonResponse({'output': 'Invalid request'})