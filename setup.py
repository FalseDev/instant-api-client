import setuptools

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

with open("requirements.txt", "r", encoding="utf-8") as req_file:
    requirements = req_file.readlines()

setuptools.setup(
    name="instant-api-client",
    version="0.1.0",
    author="FalseDev",
    license="MIT",
    description="Create API wrappers/clients in minutes, enjoying both blocking and async interfaces from one codebase!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FalseDev/instant-api-client",
    packages=["apiclient"],
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',

    ],
    python_requires='>=3.6',
)
