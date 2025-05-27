import sys
from setuptools import setup, find_packages
import sys, shutil
# Common metadata
NAME        = "spellcast-solver"
VERSION     = "0.1.0"
DESCRIPTION = "Automate SpellCast puzzles: region‑select, OCR, solve & overlay"
REQUIRES    = [
    "pillow",
    "screeninfo",
    "pynput",
    "torch",
    "torchvision",
    "tqdm",
    # …etc
]

# If we're doing a py2app build, add that configuration
if "py2app" in sys.argv:
    APP = ["main/app.py"]
    OPTIONS = {
        "argv_emulation": True,
        "packages": [
            "PIL",
            "screeninfo",
            "pynput",
            # any other non‑standard libs you need
        ],
        # you can add iconfile, resources, plist entries, etc. here
    }

    setup(
        app=APP,
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        options={"py2app": OPTIONS},
        setup_requires=["py2app"],
        install_requires=REQUIRES,
        packages=find_packages(),
    )

else:
    # Standard pip install / development
    setup(
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        packages=find_packages(),
        install_requires=REQUIRES,
        entry_points={
            "console_scripts": [
                "spellcast-solver = main.app:main",
            ],
        },
    )

if 'clean' in sys.argv:
    shutil.rmtree('build', ignore_errors=True)
    shutil.rmtree('dist',  ignore_errors=True)
