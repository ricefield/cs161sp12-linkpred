import setuptools

setuptools.setup(
    name='perceptron',
    version='1.0',
    py_modules=['perceptron'],
    install_requires=['numpy'],

    author='Leif Johnson',
    author_email='leif@leifjohnson.net',
    description='A small library of perceptron variants.',
    long_description=open('README').read(),
    license='MIT',
    keywords='perceptron discriminative classifier machine-learning',
    url='http://code.google.com/p/python-perceptron/',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        ],
    )
