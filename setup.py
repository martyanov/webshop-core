from setuptools import setup, find_packages

version = '0.1a1'

requires = []

setup(name='webshop.core',
      version=version,
      description='Bob is selling various physical and digital goods over http/https',
      author='Andrey Martyanov',
      author_email='andrey@martyanov.com',
      url='https://www.epointsystem.org/trac/vending_machine/wiki/WebShop',
      license='GNU GPL',
      packages=find_packages(),
      namespace_packages=['webshop'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      test_suite = "tests",
)