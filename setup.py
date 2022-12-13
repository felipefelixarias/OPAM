from setuptools import setup, find_packages

setup(
    name='opam', 
    version='0.1',
    url='https://github.com/felipefelixarias/OPAM',
    author='Felipe Felix Arias',
    description='A system for learning and analyzing motion patterns in environments with traversability maps.',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3'
    ],
    project_urls={
        'Homepage': 'https://felipefelixarias.github.io/OPAM',
        'Source': 'https://github.com/felipefelixarias/OPAM',
        'Bug Reports': 'https://github.com/felipefelixarias/OPAM/issues'
    },
    packages=find_packages(exclude=('test*',)),
    include_package_data=True,
    dependency_links=[
        'https://github.com/felipefelixarias/Python-RVO2/archive/main.zip#egg=pyrvo2'
    ],
    install_requires=[
        'numpy>=1.19.5',
        'Cython==0.21.1',
        'jupyter>=1.0.0',
        'jupytext>=1.2.0',
        'Pillow>=5.4.0',
        'pyrvo2'
    ],
    pyrhon_requires='>=3.6',
    keywords='robotics self-supervision motion-patterns'
    )
