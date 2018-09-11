from setuptools import setup, find_packages

packages = find_packages()
print(packages)

setup(name = 'sbnd-cege', version = '0.0', packages = packages,
      entry_points = {
          'console_scripts': [
              'build = build.main:main',
              'test_sbnd = build.tester:main',
          ],
      },
)



