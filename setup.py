from setuptools import setup, find_packages

setup(
    name="migoai",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        'requests',
        'SpeechRecognition',
        'pyttsx3'
    ],
    entry_points={
        'console_scripts': [
            'migoai=migoai.__init__:start_chat',
        ],
    },
    author="Denise",
    description="An advanced AI chat interface",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/DeniseMyName/migoai",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
