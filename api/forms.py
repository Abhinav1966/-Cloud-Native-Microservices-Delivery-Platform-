from django import forms
from .models import InfrastructureRequest

class InfrastructureForm(forms.ModelForm):
    # This creates a specialized text box for the user's script.
    # We pre-fill it with "#!/bin/bash" so the user knows exactly where to start.
    user_data_script = forms.CharField(
        initial='#!/bin/bash\n', 
        widget=forms.Textarea(attrs={
            'style': 'width: 100%; padding: 10px; height: 120px; font-family: monospace;',
            'placeholder': 'Enter your bash script here...'
        })
    )

    class Meta:
        # This connects the form to our database table "InfrastructureRequest".
        # It ensures that whatever the user types here gets saved correctly to the DB.
        model = InfrastructureRequest
        
        # We want to use all the fields defined in our database...
        fields = '__all__'
        
        # ...except for 'created_at', because the system captures the time automatically.
        exclude = ['created_at']
        
        # This 'widgets' section is purely for styling (CSS).
        # It ensures the input boxes look good (full width, padding) on the website.
        widgets = {
            # --- General Project Details ---
            'project_name': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px;'}),
            'instance_type': forms.Select(attrs={'style': 'width: 100%; padding: 10px;'}),
            'ami_id': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px;'}),
            'environment': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px;'}),
            
            'aws_region': forms.Select(attrs={'style': 'width: 100%; padding: 10px;'}),
            
            # --- SSH Key Path (Locked) ---
            # We set this to 'Read-Only' so users cannot accidentally change the secure key location.
            # It appears greyed out on the screen.
            'public_key_path': forms.TextInput(attrs={
                'readonly': 'readonly',
                'value': '/home/abhinav_007/.ssh/web_key.pub',
                'style': 'width: 100%; padding: 10px; background-color: #e9ecef; color: #555; cursor: not-allowed;'
            }),
            
            # --- Firewall Settings (Security Group) ---
            'sec_group_name': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px;'}),
            'sec_group_desc': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px;'}),
            
            # --- Network Rules (Ports) ---
            # These fields define what traffic is allowed (e.g., Port 22 for SSH).
            'ingress_from_port': forms.NumberInput(attrs={'style': 'width: 100%; padding: 10px;'}),
            'ingress_to_port': forms.NumberInput(attrs={'style': 'width: 100%; padding: 10px;'}),
            'ingress_protocol': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px;'}),
            'ingress_cidr': forms.TextInput(attrs={'style': 'width: 100%; padding: 10px;'}),
        }