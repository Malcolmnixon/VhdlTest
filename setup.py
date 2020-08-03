import setuptools

# Read README.md for the long description
with open('README.md', 'r') as fh:
    long_description = fh.read()

# Setup information
setuptools.setup(
    name='VHDLTest',
    version='0.0.1',
    author='Malcolm Nixon',
    description='VHDL Testbench Runner',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Malcolmnixon/VhdlTest',
    packages=setuptools.find_packages(
        exclude=('tests', 'docs')
    ),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.7'
)