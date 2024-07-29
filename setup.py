from setuptools import setup, find_packages
setup(
    name='Kuberastat',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib'
    ],
    author='AMIT KUMAR UPADHYAY',
    description='A library for statistical finance calculations.',
    url='https://github.com/Amitkupadhyay0/KUBERASTAT',
    license='AMIT',  # Consider using a standard license
)
