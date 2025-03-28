from setuptools import setup, find_packages

setup(
    name="rocket-logbook",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "rocket-logbook=rocket_logbook.main:main",
        ],
    },
    install_requires=[
        "rich",
        "appdirs",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A terminal-based logbook for tracking model rocket launches",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/rocket-logbook",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
)