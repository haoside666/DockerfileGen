set -ex && \
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
rm -rf /tmp/*