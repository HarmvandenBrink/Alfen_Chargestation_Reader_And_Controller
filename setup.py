from setuptools import setup

setup(
    name='alfencharger',
    version='5.42',    
    description='Python package to read and control Alfen chargers',
    url='https://github.com/HarmvandenBrink/Alfen_Chargestation_Reader_And_Controller',
    author='Harm van den Brink',
    author_email='harmvandenbrink@gmail.com',
    license='MIT License',
    packages=['alfenchargestation'],
    install_requires=['pymodbus==2.5.3'],

    classifiers=[
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
    ]
)