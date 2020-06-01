from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='dtv2',
    version='0.2',
    description='Some functions to handle color management on the Drevo Tyrfing V2',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://twitter.com/david_cobac',
    author='David COBAC',
    author_email='david.cobac@gmail.com',
    keywords=['keyboard',
              'drevo',
              'tyrfing'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    license='CC-BY-NC-SA',
    packages=find_packages()
)
