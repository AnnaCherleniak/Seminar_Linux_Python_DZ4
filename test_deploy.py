from sshcheckers import ssh_checkout, upload_files
import yaml
import pytest

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestDeployPositive:

    def test_step1_deploy(self):
        res = []
        upload_files(data["host"], data["user"], data["passwd"], data["local_path"], data["remote_path"])
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                f"echo {data['passwd']} | sudo -S dpkg -i {data['remote_path']}", "Настраивается пакет"))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                f"echo {data['passwd']} | sudo -S dpkg -s p7zip-full", "Status: install ok installed"))
        assert all(res)

    def test_step2_deploy(self, make_folders, clear_folders, make_files):
        res1 = ssh_checkout(data["host"], data["user"], data["passwd"],
                            f'cd {data["PATH_IN"]}; 7z a {data["PATH_OUT"]}/arh1', 'Everything is Ok')
        res2 = ssh_checkout(data["host"], data["user"], data["passwd"], f'ls {data["PATH_OUT"]}', 'arh1.7z')
        assert res1 and res2, 'test_step1 Fail'

    def test_step3_deploy(self, clear_folders, make_files):
        res = []
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                f'cd {data["PATH_IN"]}; 7z a {data["PATH_OUT"]}/arh1', 'Everything is Ok'))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                f'cd {data["PATH_OUT"]}; 7z e arh1.7z -o{data["PATH_EXIT"]}', 'Everything is Ok'))
        for item in make_files:
            res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                    f'ls {data["PATH_EXIT"]}', item))
        assert all(res), 'test_step2 FAIL'

    def test_step4_deploy(self):
        assert ssh_checkout(data["host"], data["user"], data["passwd"],
                                         f'cd {data["PATH_OUT"]}; 7z t arh1.7z',
                            'Everything is Ok'), 'test_step3 FAIL'

    def test_step5_deploy(self):
        assert ssh_checkout(data["host"], data["user"], data["passwd"],
                            f'cd {data["PATH_IN"]}; 7z u {data["PATH_OUT"]}/arh1',
                            'Everything is Ok'), 'test_step3 Fail'


if __name__ == '__main__':
    pytest.main(['-v'])
