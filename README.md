# Axinite
A celestial physics simulation.
## Interpretable Strings
Axinite can interpret other units through interpretable string. By defalt, axinite accepts floats as the **standard SI units** for the type of unit needed. Supported suffixes:
- `d`: day (value * 86400 to convert to seconds)
- `h`: hour (value * 3600 to convert to seconds)
- `m`: minute (value * 60 to convert to seconds)
These suffixes can be used to increase readability and make it easier to plot out templates.
## File Types
### Template Files
`*.tmpl.ax`
```json
{
    "name": string,
    "limit": interpretable string,
    "delta": interpretable string,
    "bodies": {
        "name": {
            "mass": float (kilograms),
            "radius": float (meters),
            "initial_position": {
                "x": float (meters),
                "y": float (meters),
                "z": float (meters)
            },
            "initial_velocity": {
                "x": float (meters / seconds),
                "y": float (meters / seconds),
                "z": float (meters / seconds)
            }
        }
    }
}
```
## Simulation Files
`*.ax`
