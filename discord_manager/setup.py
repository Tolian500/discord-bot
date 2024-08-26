from setuptools import setup, find_packages

setup(
    name='discord_manager',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'discord.py',
    ],
    description='A Discord bot manager for sending messages.',
    author='Anatolii Olenchuk',
    author_email='tolian500@gmail.com',
    url='https://your-repository-url',
)
