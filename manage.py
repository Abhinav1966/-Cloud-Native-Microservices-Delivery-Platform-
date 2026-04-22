#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    
    # --- STEP 1: LOAD THE CONFIGURATION ---
    # This line tells Django exactly where to find the 'Settings' file.
    # Think of it as telling the program: "Read the instructions in the 'core' folder before you start."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    
    try:
        # --- STEP 2: START THE ENGINE ---
        # We try to import the core Django tools. 
        # If Django isn't installed on this computer, this step will fail.
        from django.core.management import execute_from_command_line
        
    except ImportError as exc:
        # --- STEP 3: ERROR HANDLING ---
        # If the 'import' above failed, we show a clear error message to the user.
        # It usually means they forgot to install Django or activate their virtual environment.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # --- STEP 4: EXECUTE THE COMMAND ---
    # This acts on whatever the user typed in the terminal.
    # If they typed "python manage.py runserver", this line actually starts the server.
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()