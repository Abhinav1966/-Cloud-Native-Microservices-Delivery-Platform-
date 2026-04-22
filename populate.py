import os
import django
from django.apps import apps

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings') 
django.setup()



def run():
    # Find the model dynamically
    Resource = None
    for model in apps.get_models():
        if model.__name__ == 'Resource':
            Resource = model
            break

    if not Resource:
        print("❌ Error: Could not find 'Resource' model.")
        return

    # Add Data
    print(f"Current count: {Resource.objects.count()}")
    if Resource.objects.count() == 0:
        print("Database empty. Adding items...")
        Resource.objects.create(name="EC2", type="Compute", status="Active", icon_name="ec2.png")
        Resource.objects.create(name="S3", type="Storage", status="Active", icon_name="s3.png")
        print("✅ Added EC2 and S3.")
    else:
        print("✅ Database already has data!")

if __name__ == '__main__':
    run()
