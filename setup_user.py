import subprocess
import sys

def run_ssh_command(cmd):
    # This is a bit hacky but should work in PS if ssh is in path
    full_cmd = f"ssh rabah@192.168.70.25 \"{cmd}\""
    print(f"Running: {full_cmd}")
    # Using input to pass password if prompted (though it might hang if not handled)
    # Better to assume ssh key or simple command
    subprocess.run(full_cmd, shell=True)

py_script = """
from django.contrib.auth.models import User
u, created = User.objects.get_or_create(username='rabah', defaults={'is_superuser': True, 'is_staff': True})
u.set_password('rabah')
u.save()
print('DONE')
"""

# Write to local file first
with open("remote_setup.py", "w") as f:
    f.write(py_script)

# SCP it
subprocess.run("scp remote_setup.py rabah@192.168.70.25:/tmp/remote_setup.py", shell=True)

# Run it
subprocess.run("ssh rabah@192.168.70.25 \"cd /home/rabah/Elif-LABO/elif_universe; /home/rabah/Elif-LABO/venv/bin/python3 manage.py shell < /tmp/remote_setup.py\"", shell=True)
