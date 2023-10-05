from sshcheckers import ssh_checkout, upload_files, ssh_getout
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
        assert all(res), 'test_step1 Fail'

    def test_step2_deploy(self, make_folders, clear_folders, make_files):
        res1 = ssh_checkout(data["host"], data["user"], data["passwd"],
                            f'cd {data["PATH_IN"]}; 7z a {data["PATH_OUT"]}/arh1', 'Everything is Ok')
        res2 = ssh_checkout(data["host"], data["user"], data["passwd"], f'ls {data["PATH_OUT"]}', 'arh1.7z')
        assert res1 and res2, 'test_step2 Fail'

    def test_step3_deploy(self, clear_folders, make_files):
        res = []
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                f'cd {data["PATH_IN"]}; 7z a {data["PATH_OUT"]}/arh1', 'Everything is Ok'))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                f'cd {data["PATH_OUT"]}; 7z e arh1.7z -o{data["PATH_EXIT"]}', 'Everything is Ok'))
        for item in make_files:
            res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                    f'ls {data["PATH_EXIT"]}', item))
        assert all(res), 'test_step3 FAIL'

    def test_step4_deploy(self):
        assert ssh_checkout(data["host"], data["user"], data["passwd"],
                                         f'cd {data["PATH_OUT"]}; 7z t arh1.7z',
                            'Everything is Ok'), 'test_step4 FAIL'

    def test_step5_deploy(self):
        assert ssh_checkout(data["host"], data["user"], data["passwd"],
                            f'cd {data["PATH_IN"]}; 7z u {data["PATH_OUT"]}/arh1',
                            'Everything is Ok'), 'test_step5 Fail'

    def test_step6_deploy(self, clear_folders, make_folders, make_files):
        res = []
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                f'cd {data["PATH_IN"]}; 7z a {data["PATH_OUT"]}/arh1', 'Everything is Ok'))
        for item in make_files:
            res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                    f"cd {data['PATH_OUT']}; 7z l arh1.7z", item))
        assert all(res), 'test_step6 Fail'

    def test_step7_deploy(self, clear_folders, make_files, make_subfolder):
        res = []
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                f'cd {data["PATH_IN"]}; 7z a {data["PATH_OUT"]}/arh1', 'Everything is Ok'))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                f'cd {data["PATH_OUT"]}; 7z x arh1.7z -o{data["PATH_EXIT2"]} -y',
                                'Everything is Ok'))
        for item in make_files:
            res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                    f'ls {data["PATH_EXIT2"]}', item))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                f'ls {data["PATH_EXIT2"]}', make_subfolder[0]))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                f'ls {data["PATH_EXIT2"]}/{make_subfolder[0]}', make_subfolder[1]))
        assert all(res), 'test_step7 FAIL'

    def test_step8_deploy(self):
        assert ssh_checkout(data["host"], data["user"], data["passwd"],
                            f'cd {data["PATH_OUT"]}; 7z d arh1.7z', 'Everything is Ok'), 'test_step8 Fail'

    def test_step9_deploy(self, clear_folders, make_files):
        res = []
        for item in make_files:
            res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                    f'cd {data["PATH_IN"]}; 7z h {item}', 'Everything is Ok'))
            hash = ssh_getout(data["host"], data["user"], data["passwd"], f'cd {data["PATH_IN"]}; crc32 {item}').upper()
            res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                    f'cd {data["PATH_IN"]}; 7z h {item}', hash))
        assert all(res), 'test_step9 FAIL'


if __name__ == '__main__':
    pytest.main(['-v'])
