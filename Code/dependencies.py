import subprocess
import sys


# Make sure pip is installed
print("Making sure pip is installed...")
try:  # Debian and Ubuntu require pip to be installed differently because they disable ensurepip
    import distro
    linuxDistro = distro.linux_distribution()
    if linuxDistro[0] == "Debian" or linuxDistro[0] == "Ubuntu":
        try:
            subprocess.check_call(['apt', 'install', 'python3-pip', '-y'])
        except subprocess.CalledProcessError:
            print("You need to be the superuser to install pip and the dependencies")
            sys.exit(-4)
except ModuleNotFoundError: # If the system is not Linux, the module "distro" will not load, causing a ModuleNotFoundError exception and the normal "ensurepip" module will work
    subprocess.check_call([sys.executable, '-m', 'ensurepip']) # The module ensure pip check if pip is installed and installs it if it isn't
print("Pip is installed")

# Make sure that dependencies are installed
print("Installing dependencies...")
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
try:
    subprocess.check_call(['git', 'init'])
    subprocess.check_call(['git', 'submodule', 'init'])
    subprocess.check_call(['git', 'submodule', 'update'])
    print("Dependencies installed")
except subprocess.CalledProcessError:
    print("Git is not installed! Please install it!")

print("Done")
