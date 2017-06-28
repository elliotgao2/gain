from setuptools import find_packages, setup

setup(
    name="gain",
    version="0.1.4",
    description="Web crawling framework for everyone.",
    author="Gaojiuli",
    author_email="gaojiuli@gmail.com",
    url='https://github.com/gaojiuli/gain',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'aiohttp',
        'pyquery',
        'aiofiles',
    ],
    license='GNU GPL 3',
    packages=find_packages(),
    py_modules=['gain'],
    include_package_data=True,
    zip_safe=False
)
