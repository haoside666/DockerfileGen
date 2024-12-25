import os
import unittest

from graphgen.shell_parse.parse import parse_shell_cmd_to_primitive_feature

CURRENT_DIR = os.path.dirname(__file__)


# Test: Parse the shell command into initial instruction feature structure
class TestASTCmdParse(unittest.TestCase):
    def test_parse_cmd1(self):
        cmd = "curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose"
        print(parse_shell_cmd_to_primitive_feature(cmd))

    def test_parse_cmd2(self):
        cmd = '''echo "123">1.txt'''
        print(parse_shell_cmd_to_primitive_feature(cmd))

    def test_parse_cmd3(self):
        cmd = '''grep "pattern" < input.txt'''
        print(parse_shell_cmd_to_primitive_feature(cmd))

    def test_parse_cmd4(self):
        cmd = '''append_nl_if_not(){
                  if [ -z "$1" ]; then
                    echo "No file argument given!"
                    exit 1
                  else
                    if [ ! -f "$1" ]; then
                      echo "File $1 doesn't exist!"
                      exit 1
                    else
                      tail -c 1 "$1" | od -ta | grep -q nl
                      if [ $? -eq 1 ]; then
                        echo >> "$1"
                      fi
                    fi
                  fi
                }'''
        print(parse_shell_cmd_to_primitive_feature(cmd))

    def test_parse_cmd5(self):
        cmd = '''ARGTABLE_VER1="${ARGTABLE_VER//./-}"'''
        print(parse_shell_cmd_to_primitive_feature(cmd))

    def test_parse_cmd6(self):
        cmd = '''
            for key in 48F8E69F6390C9F25CFEDCD268248959359E722B A9C5DF4D22E99998D9875A5110C01C5A2F6059E7 DCFD35E0BF8CA7344752DE8B6FB21E8933C60243
            do
                gpg --batch --keyserver keyserver.ubuntu.com --recv-keys "$key";
            done
        '''
        print(parse_shell_cmd_to_primitive_feature(cmd))

    def test_parse_cmd7(self):
        cmd = '''apk add --no-cache gcc make musl-dev && wget http://ftp.gnu.org/gnu/gawk/gawk-5.1.0.tar.xz && tar -xJvf gawk-5.1.0.tar.xz && rm gawk-5.1.0.tar.xz'''
        print(parse_shell_cmd_to_primitive_feature(cmd))

    def test_parse_cmd8(self):
        cmd = '''echo "$RPI_KERNEL_CHECKSUM qemu-rpi-kernel.zip" | sha256sum -c'''
        print(parse_shell_cmd_to_primitive_feature(cmd))

    def test_parse_cmd9(self):
        cmd = '''aaa="123"'''
        print(parse_shell_cmd_to_primitive_feature(cmd))

    def test_parse_cmd10(self):
        cmd = '''unzip -qd ${APPS_BASE} /tmp/wildfly.zip && ln -s ${APPS_BASE}/wildfly-${WILDFLY_VERSION} ${WILDFLY_HOME}'''
        print(parse_shell_cmd_to_primitive_feature(cmd))

    def test_parse_cmd11(self):
        cmd = '''curl -s https://api.github.com/repos/arvidn/libtorrent/releases/latest | grep "lib*.*gz" | cut -d : -f 2,3 | wget -qi - tar xf *gz rm *gz cd lib* ./configure --enable-debug=no --enable-python-binding --with-libiconv make make -j$(nproc) checkinstall ldconfig'''
        print(parse_shell_cmd_to_primitive_feature(cmd))

    def test_parse_cmd_list(self):
        command_list = [
            "curl -sSL https://raw.githubusercontent.com/sgerrand/alpine-pkg-glibc/master/sgerrand.rsa.pub > /etc/apk/keys/sgerrand.rsa.pub",
            "curl -sSL https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.29-r0/glibc-2.29-r0.apk > /tmp/glibc.apk",
            "apk add --no-cache /tmp/glibc.apk",
            "apk add --no-cache gcc make musl-dev",
            "wget http://ftp.gnu.org/gnu/gawk/gawk-5.1.0.tar.xz",
            "tar -xJvf gawk-5.1.0.tar.xz",
            "grep pattern < input.txt",
            "echo \"123\">>1.txt",
        ]

        for cmd in command_list:
            print(parse_shell_cmd_to_primitive_feature(cmd, "123456"))
