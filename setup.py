from setuptools import setup, find_packages

setup(
    name='binary',
    version='0.1.0',    
    description='A Python package to represent and manipulate binary numbers',
    url='https://github.com/LeSasse/binary',
    author='Leonard Sasse',
    packages=find_packages(),
    install_requires=[],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    python_requires='>=3.6',
    include_package_data=True,
    package_data={'':['data/*']}
)
