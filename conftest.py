import pytest
from sshcheckers import ssh_checkout, ssh_getout
import random
import string
import yaml


with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return ssh_checkout(data["host"], data["user"], data["passwd"],
                        f'mkdir {data["PATH_IN"]} {data["PATH_OUT"]} {data["PATH_EXIT"]} {data["PATH_EXIT2"]}',
                        '')


@pytest.fixture()
def clear_folders():
    return ssh_checkout(data["host"], data["user"], data["passwd"],
                        f'rm -rf {data["PATH_IN"]}/* {data["PATH_OUT"]}/* {data["PATH_EXIT"]}/* {data["PATH_EXIT2"]}/*',
                        '')


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(data["host"], data["user"], data["passwd"],
                        f'cd {data["PATH_IN"]}; dd if=/dev/urandom of={filename} bs=1M count=1 iflag=fullblock',
                        ''):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout(data["host"], data["user"], data["passwd"],
                        f'cd {data["PATH_IN"]}; mkdir {subfoldername}', ''):
        return None, None
    if not ssh_checkout(data["host"], data["user"], data["passwd"],
                        f'cd {data["PATH_IN"]}/{subfoldername}; dd if=/dev/urandom of={testfilename}'
                        f' bs=1M count=1 iflag=fullblock', ''):
        return subfoldername, None
    return subfoldername, testfilename
