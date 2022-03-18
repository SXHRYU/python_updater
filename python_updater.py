import requests
from subprocess import run


def get_latest_version(r):
    # First we find a trigger in HTML for Python version.
    find_trigger = r.text.find('Latest Python 3 Release')
    length_of_trigger = len('Latest Python 3 Release')
    # mathematical operation to find something along the line of
    # [' ', '-', ' ', 'P', 'y', 't', 'h', 'o', 'n', ' ', '3', '.', '1', '0', '.', '2', '<']
    search_trigger = find_trigger + length_of_trigger
    python_version_raw = r.text[search_trigger: search_trigger+17] # -> string
    output = list(python_version_raw) # -> list (to manipulate further)
    return output


def formatting(latest_python_version_raw):
    # removing trailing and leading characters
    # the desired list should be like ['P', 'y', 't', 'h', 'o', 'n', ' ', '3', '.', '1', '0', '.', '2']
    while latest_python_version_raw[0].upper() != 'P':
        latest_python_version_raw.pop(0)
        if not latest_python_version_raw[len(latest_python_version_raw)-1].isdigit():
            latest_python_version_raw.pop(len(latest_python_version_raw)-1)
    # turn list into a string. We should have ex. 'Python 3.10.2'
    latest_python_version = ''.join(latest_python_version_raw)
    return latest_python_version


def get_current_version():
    # run command in console to find python version and format it to string.
    current_python_version_raw = run("python --version", capture_output=True).stdout
    current_python_version = str(current_python_version_raw).lstrip("b'").rstrip("\\r\\n'")
    return current_python_version


def current_vs_latest(current_python_version, latest_python_version):
    return current_python_version >= latest_python_version
    

def download_latest(latest_python_version):
    # Needed for dynamic URL lookup
    python_number = latest_python_version.replace('Python ', '')
    python_url = f'https://www.python.org/ftp/python/{python_number}/python-{python_number}-amd64.exe'
    # Begin downloading
    d = requests.get(python_url)

    with open(f'C:/{%path_to_file%}/python-{python_number}-amd64.exe', 'wb') as f:
        f.write(d.content)
    print('Download complete!')
    
    # Another way of saving
    # filename = python_url.split('/')[-1]
    # with open(filename, 'wb') as f:
    #     f.write(d.content)

print("Connecting to 'https://www.python.org/downloads/windows/'")
r = requests.get('https://www.python.org/downloads/windows/')
latest_python_version_raw = get_latest_version(r)
latest_python_version = formatting(latest_python_version_raw)
current_python_version = get_current_version()

if current_vs_latest(current_python_version, latest_python_version):
    print(f'You are up-to-date: {current_python_version}.')
else:
    print(f'Latest Release: {latest_python_version}.\nYour version is: {current_python_version}.')
    print(f'Downloading {latest_python_version}...')
    download_latest(latest_python_version)

