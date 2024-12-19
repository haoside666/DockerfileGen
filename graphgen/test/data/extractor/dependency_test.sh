# pkg-command依赖
apt install wget
wget http://ftp.gnu.org/gnu/gawk/gawk-5.1.0.tar.xz

# VarPSet-VarCSet依赖
runDeps="$( \
        scanelf --needed --nobanner /usr/bin/ss-* \
            | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
            | xargs -r apk info --installed \
            | sort -u \
    )"


apk add --no-cache --virtual .run-deps $runDeps


aaa="123"
echo $aaa > /etc/aaa.txt

# 目录依赖
wget -q -nc --no-check-certificate -P /var/tmp https://cmake.org/files/v3.11/cmake-3.11.1-Linux-x86_64.sh
/var/tmp/cmake-3.11.1-Linux-x86_64.sh --prefix=/usr/local --skip-license


mkdir -p /var/tmp && touch 1.txt
cd /var/tmp


# other依赖
groupadd -g 1000 laradock && useradd -l -u 1000 -g laradock -m laradock -G docker_env && usermod -p "*" laradock -s /bin/bash
chown laradock:laradock /home/laradock/aliases.sh
