from setuptools import setup

try:
    import pypandoc # type: ignore
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError) as ex:
    print("Pandoc failed", ex)
    long_description = open('README.md').read()

setup(
    name='git_secrets_ahoy',
    version='0.1.0',
    description='Secret scanning git commits',
    long_description=long_description,
    url='http://github.com/ministryofjustice/get-secrets-ahoy',
    author='Ministry of Justice',
    author_email='noms-studio-webops@digital.justice.gov.uk',
    license='GPLv2',
    packages=['git_secrets_ahoy'],
    python_requires='>=3.5',
    install_requires=[
        'GitPython ~= 2.1.8',
        'dataclasses ~= 0.5.0'
    ],
    zip_safe=False,
    entry_points = {
        'console_scripts': ['git-secrets-ahoy=git_secrets_ahoy:main'],
    }
)
