from setuptools import setup, find_packages

version = '0.0.0.dev0'

setup(
    name='cringe',
    description='Co-routines in nice GNOME environment',
    version=version,
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Classifier: License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Classifier: Topic :: Software Development :: Libraries :: Python Modules",
    ],
    author='John Carr',
    author_email='john.carr@unrouted.co.uk',
    license="GNU LGPL",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires = ['greenlet'],
)
