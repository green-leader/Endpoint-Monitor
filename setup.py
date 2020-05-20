from setuptools import setup, find_packages

setup(
      name="endpoint-monitor",
      version="0.0.1",
      author="Sion Fandrick",
      url="https://github.com/green-leader/Endpoint-Monitor",

      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'monitor = monitor.cli:main'
          ],
      }
)
