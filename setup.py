from setuptools import setup


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
        return long_description


setup(
    name='gemini_chat_app',
    version='1',
    packages=['gemini_chat_app'],
    url='https://github.com/SoftwareApkDev/gemini_chat_app',
    license='MIT',
    author='SoftwareApkDev',
    author_email='softwareapkdev2022@gmail.com',
    description='This package contains implementation of an application where the user can chat with Google Gemini AI.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    entry_points={
        "console_scripts": [
            "main=main:main",
        ]
    }
)