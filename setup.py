from setuptools import setup, find_packages

setup(
    name='straights',  # Replace with your project name
    version='0.6.0',    # Project version
    packages=find_packages(),  # Automatically find packages in your project
    include_package_data=True, # Include non-code files specified in MANIFEST.in
    install_requires=[
    'cvc5',
    'CustomTKinter',
    'pillow',
    ],
    entry_points={
        'console_scripts': [
            'str8ts = straights.main:main',  # Replace with your module and main function
        ],
    },
    author='Robin Pfau',             # Your name
    author_email='r.pfau@campus.lmu.de',  # Your email
    description='A SMT Solver for the Str8ts puzzle',
    #long_description=open('README.md').read(),  # Optionally load README for PyPI
    #long_description_content_type='text/markdown',
    url='https://github.com/RobinPfau/ProjectBachelor',  # Project URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',  # List supported versions
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version
    package_data={  # Explicitly include package data if needed
        '': ['*.json'],  # Include all JSON files in the package
    },
)
