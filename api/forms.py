import os
from django import forms
from .models import InfrastructureRequest

# Dynamically find the home directory of the current user
dynamic_key_path = os.path.expanduser('~/.ssh/web_key.pub')

class InfrastructureForm(forms.ModelForm):
    user_data_script = forms.CharField(
        initial='#!/bin/bash\n', 
        widget=forms.Textarea(attrs={
            'style': 'width: 100%; padding: 10px; height: 120px; font-family: monospace;',
            'placeholder': 'Enter your bash script here...'
        })
    )

    class Meta:
        model = InfrastructureRequest
        fields = '__all__'
        exclude = ['created_at']
        
        widgets = {
            'project_name': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px;'}),
            'instance_type': forms.Select(attrs={'style': 'width: 100%; padding: 10px;'}),
            'ami_id': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px;'}),
            'environment': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px;'}),
            'aws_region': forms.Select(attrs={'style': 'width: 100%; padding: 10px;'}),
            
           
            'public_key_path': forms.TextInput(attrs={
                
                # --- SSH Key Path (UNLOCKED) ---
            'public_key_path': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px;'}),
            }),
            
            'sec_group_name': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px;'}),
            'sec_group_desc': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px;'}),
            'ingress_from_port': forms.NumberInput(attrs={'style': 'width: 100%; padding: 10px;'}),
            'ingress_to_port': forms.NumberInput(attrs={'style': 'width: 100%; padding: 10px;'}),
            'ingress_protocol': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px;'}),
            'ingress_cidr': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px;'}),
        }