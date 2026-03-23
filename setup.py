from setuptools import find_packages, setup

long_description = '''\
The Vobiz Python SDK makes it simpler to integrate communications into your
Python applications using the Vobiz REST API. Using the SDK, you will be able
to make voice calls, manage trunks, phone numbers, endpoints, and generate Vobiz XML
to control your call flows.

See https://github.com/vobiz/vobiz-python for more information.
'''

setup(
    name="vobiz",
    version='0.1.0',
    description='Vobiz Python SDK for voice, trunks, phone numbers, endpoints, and XML.',
    long_description=long_description,
    url='https://github.com/vobiz/vobiz-python',
    author='Vobiz',
    author_email='support@vobiz.ai',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Telephony',
    ],
    install_requires=[
        'requests >= 2, < 3',
        'decorator >= 5',
        'lxml >= 3',
        'PyJWT'
    ],
    keywords=['vobiz', 'vobiz xml', 'voice calls', 'sip trunking', 'telephony'],
    include_package_data=True,
    packages=find_packages(exclude=['tests', 'tests.*']), )
