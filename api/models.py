from django.db import models

# This model acts like a simple "Inventory List" in our database.
# It stores small tracking items, but isn't the main part of the infrastructure creator.
class Resource(models.Model):
    name = models.CharField(max_length=100)       # The name of the resource
    type = models.CharField(max_length=50)        # What category it belongs to
    status = models.CharField(max_length=50)      # Is it Active? Pending? Failed?
    icon_name = models.CharField(max_length=100, blank=True, null=True) # Optional icon for the UI

    def __str__(self):
        return self.name

# -------------------------------------------------------------------------

# This is the MAIN model. 
# Think of this as the "Order Form" where we save everything the user typed.
class InfrastructureRequest(models.Model):
    
    # --- 1. PRE-DEFINED MENUS ---
    # These lists define the specific options available in the dropdown menus.
    # By listing them here, we ensure users can't type random values.
    
    INSTANCE_TYPES = [
        ('t2.micro', 't2.micro (Free Tier)'),           # Option 1: Smallest/Free
        ('t3.medium', 't3.medium (General Purpose)'),   # Option 2: Medium power
        ('c5.large', 'c5.large (Compute Optimized)'),   # Option 3: High power
    ]

    AWS_REGIONS = [
        ('us-east-1', 'US East (N. Virginia)'),         # The default AWS location
        ('us-east-2', 'US East (Ohio)'),
        ('us-west-1', 'US West (N. California)'),
        ('us-west-2', 'US West (Oregon)'),
        ('ap-south-1', 'Asia Pacific (Mumbai)'),
        ('ap-southeast-1', 'Asia Pacific (Singapore)'),
        ('eu-central-1', 'Europe (Frankfurt)'),
        ('eu-west-1', 'Europe (Ireland)'),
        ('eu-west-2', 'Europe (London)'),
    ]

    # --- 2. BASIC PROJECT DETAILS ---
    # Simple text fields to identify who is asking for what.
    
    project_name = models.CharField(max_length=100) # User gives their project a name
    
    # Here we attach the "INSTANCE_TYPES" list from above to this field.
    # It forces the database to only accept valid server sizes.
    instance_type = models.CharField(max_length=20, choices=INSTANCE_TYPES, default='t2.micro')
    
    # The ID of the Operating System image (e.g., Ubuntu). Defaults to a known working ID.
    ami_id = models.CharField(max_length=50, default='ami-0c55b159cbfafe1f0')
    
    # Tagging the environment (Dev, Test, Prod) helps us organize resources later.
    environment = models.CharField(max_length=50, default='Dev')
    
    # Automatically records the exact date and time the "Create" button was clicked.
    created_at = models.DateTimeField(auto_now_add=True)

    # --- 3. LOCATION ---
    # This field uses the long list of "AWS_REGIONS" to create a location dropdown.
    aws_region = models.CharField(
        max_length=50, 
        choices=AWS_REGIONS,  
        default='us-east-1'
    )

    # --- 4. SECURITY & ACCESS ---
    # This points to where the digital "Key" is stored on the server.
    # Without this key, we wouldn't be able to log into the new server.
    public_key_path = models.CharField(max_length=200, default='/root/.ssh/web.pub')

    # --- 5. FIREWALL SETTINGS (Security Groups) ---
    # These fields define the "virtual fence" around the server.
    sec_group_name = models.CharField(max_length=100, default='web-access-sg')
    sec_group_desc = models.CharField(max_length=200, default='Allow standard web traffic')
    
    # --- 6. NETWORK RULES (Ports) ---
    # These rules decide which doors are open. 
    # Default is Port 22 (SSH), which lets admins control the server.
    ingress_from_port = models.IntegerField(default=22)
    ingress_to_port = models.IntegerField(default=22)
    ingress_protocol = models.CharField(max_length=10, default='tcp')
    ingress_cidr = models.CharField(max_length=50, default='0.0.0.0/0') # "0.0.0.0/0" means "Allow anyone"

    # --- 7. AUTOMATION SCRIPT ---
    # This is a special text area where users can paste code (Bash script).
    # This code runs automatically the moment the server turns on.
    user_data_script = models.TextField(default="#!/bin/bash\n", help_text="Shell script to run on startup")

    def __str__(self):
        return self.project_name