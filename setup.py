"""
Build configuration
"""
import setuptools

VERSION=(0, 2, 2)

with open("README.md", "r") as handler:
    LONG_DESC = handler.read()

setuptools.setup(
    name="helmix",
    version=".".join(str(f) for f in VERSION),
    description="Simple templating for K8S deployments",
    long_description=LONG_DESC,
    long_description_content_type='text/markdown',
    author="Tomasz bla Fortuna",
    author_email="bla@thera.be",
    url="https://github.com/exatel/helmix",
    keywords="k8s k3s templating deployment iaac gitops",
    scripts=['helmix'],
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=[
        'PyYAML>=5.3.1',
        'Jinja2>=2.10',
    ],
    extras_require={
        'gpg': ["gpg >= 1.10"],
    },
    license="GPL3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Software Development :: Build Tools",
    ],
)
