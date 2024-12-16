import unittest

from dockdepend.shell_parse.parse import parse_shell_cmd_to_instruct_feature


# Test: Parse the shell command into initial instruction feature structure
class TestASTCmdParse(unittest.TestCase):
    def test_parse_cmd1(self):
        cmd = "curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose"
        print(parse_shell_cmd_to_instruct_feature(cmd))

    def test_parse_cmd2(self):
        cmd = '''set -ex && \
        apk add --no-cache --virtual .build-deps \
                                    autoconf \
                                    build-base \
                                    curl \
                                    libev-dev \
                                    linux-headers \
                                    libsodium-dev \
                                    mbedtls-dev \
                                    pcre-dev \
                                    tar \
                                    tzdata \
                                    c-ares-dev \
                                    git \
                                    gcc \
                                    make \
                                    libtool \
                                    zlib-dev \
                                    automake \
                                    openssl \
                                    asciidoc \
                                    xmlto \
                                    wget \
                                    libpcre32 \
                                    g++ && \
        cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
        cd /tmp && \
        curl -sSL $KCP_URL | tar xz server_linux_amd64 && \
        mv server_linux_amd64 /usr/bin/ && \
        mkdir ss && \
        cd ss && \
        curl -sSL $SS_URL | tar xz --strip 1 && \
        ./configure --prefix=/usr --disable-documentation && \
        make install && \
        cd /tmp && \
        runDeps="$( \
            scanelf --needed --nobanner /usr/bin/ss-* \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | xargs -r apk info --installed \
                | sort -u \
        )" && \
        apk add --no-cache --virtual .run-deps $runDeps && \
        apk del .build-deps && \
        rm -rf /tmp/*'''
        print(parse_shell_cmd_to_instruct_feature(cmd))

    def test_parse_cmd3(self):
        cmd = '''
        SUPERCRONIC="asciidoc" &&
        curl -fsSLO "$SUPERCRONIC_URL" \
        && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
        && chmod +x "$SUPERCRONIC" \
        && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
        && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic'''
        print(parse_shell_cmd_to_instruct_feature(cmd))

    def test_parse_cmd4(self):
        cmd = '''ARGTABLE_VER1="${ARGTABLE_VER//./-}"'''
        print(parse_shell_cmd_to_instruct_feature(cmd))

    def test_parse_cmd5(self):
        cmd = '''tar --strip-components=1 -xaf perl-5.8.9.tar.bz2 -C /usr/src/perl'''
        print(parse_shell_cmd_to_instruct_feature(cmd))

    def test_parse_cmd6(self):
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
        print(parse_shell_cmd_to_instruct_feature(cmd))
