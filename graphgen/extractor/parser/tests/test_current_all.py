# 测试当前目录所有测试用例
import unittest

# discover("指定搜索的目录文件","指定字母开头模块文件")
suite = unittest.defaultTestLoader.discover('.', 'test_parse_*.py')
runner = unittest.TextTestRunner()
runner.run(suite)
