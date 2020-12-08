from setuptools import setup, find_packages
setup(
    name = "anycurve",
    version = "0.2.0",
    keywords = ["anycurve", "curve", "plot", "hwfan"],
    description = "A data visualization toolbox",
    long_description = "A python toolbox for the visualization of data series",
    license = "Apache",

    url = "http://hwfan.io",
    author = "hwfan",
    author_email = "hwnorm@outlook.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['pandas', 'numpy', 'lmdb', 'matplotlib'],
    scripts = [],

)
