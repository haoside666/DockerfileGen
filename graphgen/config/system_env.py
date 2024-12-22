GO_ENV = {
    "GO111MODULE",
    "GOARCH",
    "GOBIN",
    "GOENV",
    "GOPATH",
    "GOROOT"
}

PYTHON_ENV = {
    "PYTHONPATH",
    "PYTHONHOME",
    "PYTHONUTF8",
    "PYTHONIOENCODING",
    "PYTHONHASHSEED",
    "PYTHONBREAKPOINT",
    "PYTHONDEVMODE"
}

NODE_ENV = {
    "NODE_NO_WARNINGS",
    "NODE_PATH",
    "TZ"
}

JAVA_ENV = {
    "JAVA_HOME"
}

APT_ENV = {
    "DEBIAN_FRONTEND"
}

SYSTEM_ENV_DICT = {
    "go": GO_ENV,
    "python": PYTHON_ENV,
    "python2": PYTHON_ENV,
    "python3": PYTHON_ENV,
    "node": NODE_ENV,
    "java": JAVA_ENV,
    "apt": APT_ENV,
    "apt-get": APT_ENV,
}
