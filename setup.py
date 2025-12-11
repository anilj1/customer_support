# setup.py

from setuptools import setup, find_packages
# Import the 'codecs' library to control file encoding
import codecs
import os  # Import os for path joining

# Define the root directory
HERE = os.path.abspath(os.path.dirname(__file__))


# Function to read files with UTF-8 encoding
def read_file(filepath):
    # Use codecs.open with 'utf-8' explicitly
    with codecs.open(os.path.join(HERE, filepath), 'r', 'utf-8') as f:
        return f.read()


setup(
    # --- CRITICAL CHANGE 1: New Package Name ---
    name='customer-support-agent',  # Name used on PyPI and for 'pip install'
    version='0.1.0',
    description='A LangGraph orchestrator workflow for automated customer support inquiry processing.',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='http://github.com/your-repo/customer-support-agent',

    # Automatically finds all directories with __init__.py, now named 'customer_support'
    packages=find_packages(),

    install_requires=[
        'langgraph',
        'openai',
        'python-dotenv',
        'dataclasses',
    ],

    # --- CRITICAL CHANGE 2: New Entry Point ---
    # The 'console_scripts' defines the command ('run-support') and
    # points it to the function 'main' inside the file 'orchestrator'
    # within the package 'customer_support'.
    entry_points={
        'console_scripts': [
            'run-support = customer_support.orchestrator:main',
        ],
    },

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
