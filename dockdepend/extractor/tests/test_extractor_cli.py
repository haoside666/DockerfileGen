import unittest
from dockdepend.extractor.extractor_cli import get_command_list_feature


# Test the command list extraction function
class TestExtractorCli(unittest.TestCase):
    def test_cmd1(self):
        command_list = ["apt install -y vim"]
        attribute_user = "root"
        attribute_dir = "/tmp"
        instruct1_feature, attribute_dir = get_command_list_feature(command_list, attribute_user, attribute_dir)
        print(instruct1_feature)

    def test_cmd2(self):
        command_list = ["cd /tmp"]
        attribute_user = "root"
        attribute_dir = "/tmp"
        instruct1_feature, attribute_dir = get_command_list_feature(command_list, attribute_user, attribute_dir)
        print(instruct1_feature)

    def test_cmd3(self):
        command_list = [
            "/opt/conda/bin/conda env create -f /root/deeplearningproject_environment.yml",
            "/bin/bash ~/miniconda.sh -b -p /opt/conda",
            "/bin/bash ~/miniconda.sh -b -p /opt/conda",
            "rm ~/miniconda.sh",
            "ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh",
        ]
        attribute_user = "root"
        attribute_dir = "/tmp"
        instruct1_feature, attribute_dir = get_command_list_feature(command_list, attribute_user, attribute_dir)
        print(instruct1_feature)

    def test_pipe_cmd1(self):
        command_list = [
            ["curl -L -s https://dl.google.com/go/go1.13.1.linux-amd64.tar.gz", "tar zx"]
        ]
        attribute_user = "root"
        attribute_dir = "/tmp"
        instruct1_feature, attribute_dir = get_command_list_feature(command_list, attribute_user, attribute_dir)
        print(instruct1_feature)

    def test_pipe_cmd2(self):
        command_list = [
            ["wget -O - https://github.com/shadowsocks/shadowsocks-rust/releases/download/v1.7.0/shadowsocks-v1.7.0-nightly.x86_64-unknown-linux-musl.tar.xz",
                "tar -xJv -C /usr/local/bin sslocal"]
        ]
        attribute_user = "root"
        attribute_dir = "/tmp"
        instruct1_feature, attribute_dir = get_command_list_feature(command_list, attribute_user, attribute_dir)
        print(instruct1_feature)

    def test_mix_cmd1(self):
        command_list = ["unzip -q -o a.zip -d /usr/local bin/protoc",
                        ["wget -qO- http://www.xunsearch.com/download/xunsearch-full-dev.tar.bz2", "tar -xj"]]

        attribute_user = "root"
        attribute_dir = "/tmp"
        instruct1_feature, attribute_dir = get_command_list_feature(command_list, attribute_user, attribute_dir)
        print(instruct1_feature)

    def test_mix_cmd2(self):
        command_list = [
            "cd /opt",
            ["curl -L -s https://dl.google.com/go/go1.13.1.linux-amd64.tar.gz", "tar zx"]
        ]
        attribute_user = "root"
        attribute_dir = "/tmp"
        instruct1_feature, attribute_dir = get_command_list_feature(command_list, attribute_user, attribute_dir)
        print(instruct1_feature)

    def test_mix_cmd3(self):
        command_list = ["unzip -q -o a.zip -d /usr/local bin/protoc",
                        ["wget -qO- http://www.xunsearch.com/download/xunsearch-full-dev.tar.bz2", "tar -xj"]]

        attribute_user = "root"
        attribute_dir = "/tmp"
        instruct1_feature, attribute_dir = get_command_list_feature(command_list, attribute_user, attribute_dir)
        print(instruct1_feature)
