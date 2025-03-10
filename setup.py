import setuptools

setuptools.setup(
    name="dikidi",
    version="1.0.1",
    description="Dikidi API wrapper",
    url="https://github.com/ixtora/dikidi-api",
    install_requires=[
                  'requests',
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
