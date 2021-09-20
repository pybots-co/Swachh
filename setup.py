from setuptools import setup, find_packages
from pathlib import Path
import os

this_directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(this_directory, "README.md"), "r") as fh:
    long_description = fh.read()

setup(
    # options={'bdist_wheel':{'universal':True}},
    name='Swachh',
    author='Karthik Kallur',
    author_email = 'karthik@cloint.com',
    packages=find_packages(), 
    include_package_data=True,
    zip_safe=False,
    version='0.0.3',
    description="Python based PC Cleaner & Tuner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ClointFusion/Swachh',
    setup_requires=["wheel",'numpy',"setuptools"],
    keywords='ClointFusion,RPA,Python,Automation,BOT,Software BOT,ROBOT,PC Cleaner,Swachh',
    license="GNU",
    install_requires=open('requirements.txt').read().split('\n'),
    # py_modules=['ClointFusion'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: End Users/Desktop',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Natural Language :: English',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python',
  ],
    entry_points={
        'console_scripts': [
            'swachh = Swachh.Swachh:cli_launch_swachh',
        ],
    },
  python_requires='>=3.8, <4',

  project_urls={  # Optional
      'Date ❤️ with ClointFusion': 'https://lnkd.in/gh_r9YB',
      'WhatsApp Community': 'https://chat.whatsapp.com/DkY9QKmQkTZIv1CsOVrgWW',
      'Hackathon Website': 'https://tinyurl.com/ClointFusion',
      'Discord': 'https://discord.com/invite/tsMBN4PXKH',
      'Bug Reports': 'https://github.com/ClointFusion/Swachh/issues',
      'Source Code': 'https://github.com/ClointFusion/Swachh',
      'Automation/RPA': 'https://pypi.org/project/ClointFusion'
  },
    has_ext_modules=lambda: True
)

# python setup.py build bdist_wheel rotate --match=*.exe*,*.egg*,*.tar.gz*,*.whl* --keep=1

# twine upload dist/* --verbose