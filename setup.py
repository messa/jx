from setuptools import setup, find_packages


setup(
    name='sample',
    version='0.0.1',
    # TODO description='A sample Python project',
    # TODO long_description=long_description,
    # TODO url='https://github.com/pypa/sampleproject',
    author='Petr Messner',
    author_email='petr.messner@gmail.com',
    # TODO license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        #'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='journal',
    packages=find_packages(exclude=['doc', 'tests']),
    install_requires=[
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'jx=jx:jx_main',
        ],
    },
)
