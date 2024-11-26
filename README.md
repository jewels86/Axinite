# Axinite
A celestial physics simulation.
## Installation
Download the (Axinite source code)[https://github.com/jewels86/Axinite/releases/tag/stable] and extract it.
For now, you will need to install `python` and all the packages Axinite needs to function.
You can install the packages using `pip install -r requirements.txt` after opening the command line in the folder with Axinite.
## Command Line Interface
Commands:
- `main.py load <TEMPLATE-FILE>`
- `main.py show <SIMULATION-FILE>`
## Interpretable Strings
Axinite can interpret other units through interpretable string. By defalt, axinite accepts floats as the **standard SI units** for the type of unit needed. Supported suffixes:
- `d`: day (value * 86400 to convert to seconds)
- `h`: hour (value * 3600 to convert to seconds)
- `m`: minute (value * 60 to convert to seconds)
These suffixes can be used to increase readability and make it easier to plot out templates.
## Contributing
Create an (issue)[https://github.com/jewels86/Axinite/issues] or a (pull request)[https://github.com/jewels86/Axinite/pulls] to contribute to the project.
Issues and pull requests will be reviewed within the week.
## File Types
All files ending in `.ax` use JSON format to serialize ddata.
### Template Files
`*.tmpl.ax`
```json
{
    "name": "string",
    "limit": "interpretable string",
    "delta": "interpretable string",
    "bodies": {
        "name": {
            "mass": "float (kilograms)",
            "radius": "float (meters)",
            "initial_position": {
                "x": "float (meters)",
                "y": "float (meters)",
                "z": "float (meters)"
            },
            "initial_velocity": {
                "x": "float (meter / second)",
                "y": "float (meter / second)",
                "z": "float (meters / seconds)"
            }
        }
    }
}
```
## Simulation Files
`*.ax`
```json
{
    "name": "string",
    "bodies": {
        "name": {
            "name": "string",
            "r": {
                "x": "float (meters)",
                "y": "float (meters)",
                "z": "float (meters)"
            },
            "v": {
                "x": "float (meter / second)",
                "y": "float (meter / second)",
                "z": "float (meter / second)"
            },
         }
    }
}
```
