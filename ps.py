
with open('requirements.txt', 'r') as f:
    packages = f.read().splitlines()

packages = [package.split("==")[0] for package in packages]

with open('requirements.txt', 'w') as f:
    for package in packages:
        f.write(package + '\n')
