NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = ""
NEO4J_PWD = ""

DATABASES = {
    # 连接mysql数据库
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '192.168.239.128',
        'PORT': '3306',
        'NAME': 'dockerfile_gen',
        'USER': 'root',
        'PASSWORD': '123456'
    },
    'local': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '172.0.0.1',
        'PORT': '3306',
        'NAME': 'dockerfile_gen',
        'USER': 'root',
        'PASSWORD': '123456'
    }
}
