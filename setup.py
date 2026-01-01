from setuptools import setup

with open('README.md', 'r', encoding='utf8') as f:
    long_description = f.read()

setup(
    name="chrometomato",
    version="1.0.7",
    author="Edanick",
    description = "A selenium wrapper with easy use, configuration and shorter code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.10',
    install_requires=[
        'selenium',
        'PyYAML'
    ]
)