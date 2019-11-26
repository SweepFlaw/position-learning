from setuptools import setup, find_packages

setup(
  name='position-learning',
  version='1.0',
  author='Jisung Hong',
  author_email='rhfktj@gmail.com',
  description='',
  long_description='./README.md',
  long_description_content_type='text/markdown',
  url='https://github.com/SweepFlaw/position-learning',
  install_requires=['torch>=1.3.0',
                    ],
  packages=find_packages(),
  python_requires='>=3',
  classifier=[
    'Programming Language :: Python :: 3'
  ]
)