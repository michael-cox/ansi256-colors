from setuptools import setup, find_packages
import pathlib

repo_root = pathlib.Path(__file__).parent.resolve()

long_description = (repo_root / "README.md").read_text(encoding='utf-8')

setup(
        name='ansi256colors',
        version='1.0.0',
        description='A tool to print and demo ansi color codes for a 256 color terminal',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/michael-cox/ansi256-colors",
        author="Michael Cox",

        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Topic :: System :: Console Fonts",
            "License :: OSI Approved :: GNU General Public License v3",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3 :: Only",
        ],
        keywords="ansi, ansi256, color, codes, color codes, console, terminal,"
        "emulator, color, 256",
        
        package_dir={"": "src"},
        packages=find_packages(where="src"),

        install_requires=["tabulate"],
        python_requires=">=3.7, <4",

        entry_points={
            "console_scripts": [
                "ansi256=ansi256:main",
            ],
        },
)


            
