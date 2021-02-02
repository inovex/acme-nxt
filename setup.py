from setuptools import setup, find_packages

setup(
    name="acme_nxt",
    author="Holger Mueller",
    author_email="holger.mueller@inovex.de",
    version="0.1",
    license="MIT",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'acme-nxt = acme_nxt.nxt:main'
        ],
    },
    install_requires=[
        'sh',
    ],
)
