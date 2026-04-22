import os
import django

# 1. Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Resource

def populate_db():
    print("🧹 Clearing old data...")
    Resource.objects.all().delete()

    print("🌱 Adding services with reliable PNG icons...")

    # We are switching to PNG icons which are much more reliable than SVGs
    services = [
        # --- COMPUTE FAVORITES ---
        {
            "name": "Amazon EC2",
            "type": "Compute",
            "icon_name": "https://img.icons8.com/color/96/amazon-ec2.png"
        },
        {
            "name": "AWS Lambda",
            "type": "Compute",
            "icon_name": "https://img.icons8.com/color/96/amazon-lambda.png"
        },
        {
            "name": "Amazon EKS",
            "type": "Compute",
            "icon_name": "https://img.icons8.com/color/96/kubernetes.png"
        },

        # --- STORAGE SOLUTIONS ---
        {
            "name": "Amazon S3",
            "type": "Storage",
            "icon_name": "https://img.icons8.com/color/96/amazon-s3.png"
        },
        {
            "name": "Amazon EFS",
            "type": "Storage",
            "icon_name": "https://img.icons8.com/fluency/96/server.png" # Generic server icon often used for EFS
        },
        
        # --- DATABASE OPTIONS ---
        {
            "name": "Amazon RDS",
            "type": "Database",
            "icon_name": "https://img.icons8.com/color/96/amazon-rds.png"
        },
        {
            "name": "DynamoDB",
            "type": "Database",
            "icon_name": "https://img.icons8.com/color/96/amazon-dynamodb.png"
        }
    ]

    # Insert into Database
    for s in services:
        Resource.objects.create(
            name=s['name'],
            type=s['type'],
            status="", # Empty status as requested
            icon_name=s['icon_name']
        )

    print(f"✅ Successfully added {len(services)} services with PNG icons.")

if __name__ == '__main__':
    populate_db()