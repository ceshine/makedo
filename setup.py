from setuptools import setup

setup(
    name="MakeDo",
    version="0.1",
    py_modules=['makedo'],
    install_requires=[
        'click',
        'poseidon',
        'simplejson',
    ],
    entry_points='''
        [console_scripts]
        makedo=makedo:cli
    '''
)
