import subprocess
import os

def get_docker_compose_dir():
    return os.path.dirname(os.path.abspath(__file__))

def run_on_container(cmd, container='web'):
    orig_dir = os.getcwd()
    os.chdir(get_docker_compose_dir())
    returncode = subprocess.call(['docker-compose', 'run', '--rm', container, '/bin/bash', '-c', cmd])
    os.chdir(orig_dir)
