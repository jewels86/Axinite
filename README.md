# Axinite
A celestial physics simulation.
## File Types
### Template Files
`*.tmpl.ax`
```json
{
    "limit": float (seconds),
    "delta": float (seconds),
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
