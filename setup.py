# from distutils.core import setup, find_packages
from setuptools import setup, find_packages

from pathlib import Path

long_description = (Path(__file__).parent / "README.md").read_text()

# for item in find_packages(exclude=['graphgen.graph', 'graphgen.test', '*.old*', '*.tests', 'graphgen.extractor.parser.*']):
#     print(item)

##
## TODO: Rename the package names (and the name of the whole library)
##
setup(
    name='dockerfileGen',
    version='1.0.0',
    py_modules=['graphgen.util',
                'graphgen.cli'],
    packages=find_packages(
        exclude=['graphgen.test', '*.old*', '*.tests',
                 'graphgen.extractor.parser.*', 'output', 'experiment', 'template'],
    ),
    include_package_data=True,
    ## Necessary for the markdown to be properly rendered
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.8',
    install_requires=['dockerfile', 'neo4j==5.27.0'],
    entry_points={
        'console_scripts': [
            'dockerfileGen=graphgen.cli:main']
    },
)
