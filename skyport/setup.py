
from setuptools import setup, find_packages

setup(
    name="skyport_engine",
    # version format: major version . minor version . patch version
    version="0.1.25",
    include_package_data=True,
    package_data={"skyport": ["*.json", "**/*.json", "*.png", "**/*.png", "*.mp3", "**/*.mp3"]},
    install_requires=[
        'pygame-ce>=2.5.5',
        'numpy>=2.3.2'
        ]
    )
#C:\Users\matth\OneDrive\Desktop\skyport
#C:\Users\matth\OneDrive\Desktop\skyport\dist\skyport-0.1.0-py3-none-any.whl

#compile with:
# cd "C:\Users\matth\OneDrive\Desktop\skyport" && python setup.py sdist bdist_wheel
#pip install dist\skyport_engine-0.1.25-py3-none-any.whl

#twine upload dist/*