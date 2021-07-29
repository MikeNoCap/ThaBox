import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='thabox',
    version='0.0.3',
    author='The Jazzed Jerboas',
    author_email='thorvaldsenmikkel@gmail.com',
    description="""ThaBox is an open-source, terminal-based, retro-modern chat application where clients can connect to chatrooms and talk anonymously.""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/MikeNoCap/ThaBox',
    project_urls = {
        "Bug Tracker": "https://github.com/MikeNoCap/ThaBox/issues"
    },
    license='MIT',
    packages=['thabox'],
    install_requires=["python-socketio-client~=1.1", "keyboard~=0.13", "rich~=10.6", "playsound"]
)