# Axinite
A powerful open-source engine for advanced celestial mechanics.

![axinite-1](https://github.com/user-attachments/assets/bcd7bc7e-627e-44e5-bfc6-d2ddd787a208)

## Overview
**Axinite** is an engine for calculating celestial motion. 
You can use it to design your own solar systems, predict trajectories of rockets, simulate gravitational interactions and more.
### What is `axtools`?
`axtools` is a library to help abstract and simplify Axinite. With `axtools`, Developers can deploy Axinite powered applications with ease.

## Usage
The `axinite` module can be downloaded from the [latest release](https://github.com/jewels86/Axinite/releases) and used in python code. 
For using `axtools`, head over to the [`axtools` usage](#axtools-usage) section.
For using Axinite as an executable, see [executable usage](#executable).

`axinite` uses the `Body` class to condense planet data so it can be processed. Once the bodies have been initialized, they can then be passed into the `load` function along with simulation parameters.

Here's an example of the `axinite` module:
```python
import axinite as ax
import astropy.units as u

earth = ax.Body("Earth", 5.972e24 * u.kg, ax.to_vector({"x": 0, "y": 0, "z": 0}, u.m), ax.to_vector({"x": 0, "y": 0, "z": 0}, u.m/u.s), 6.371e6 * u.m)
moon = ax.Body("Moon", 7.342e22 * u.kg, ax.to_vector({"x": 3.844e8, "y": 0, "z": 0}, u.m), ax.to_vector({"x": 0, "y": 1.022e3, "z": 0}, u.m/u.s), 1.737e6 * u.m)

delta = ax.functions.interpret_time("1hr")
limit = ax.functions.interpret_time("30d")

bodies = ax.load(delta, limit, lambda x: pass, earth, moon)
```

## `axtools` Usage
The `axtools` module can be used to significantly abstract `axinite`'s usage. 
`axtools` uses `.ax` files to load and show simulations.
Files that are used to load and compute new simulations are marked as `.tmpl.ax` files.

Here's an example template file:
```json
{
    "name": "example-system",
    "limit": "365d",
    "delta": "1hr",
    "t": 0,
    "radius_multiplier": 2,
    "bodies": [
        {
            "name": "Earth",
            "mass": 5.972e24,
            "radius": 6.371e6,
            "r": {
                "x": 0,
                "y": 0,
                "z": 0
            },
            "v": {
                "x": 0,
                "y": 0,
                "z": 0
            }
        },
        {
            "name": "Moon",
            "mass": 7.342e22,
            "radius": 1.737e6,
            "r": {
                "x": 3.844e8,
                "y": 0,
                "z": 0
            },
            "v": {
                "x": 0,
                "y": 1.022e3,
                "z": 0
            }
        }
    ]
}
```
Additional simulation parameters, such as `radius_multiplier` and `rate` can be added to further customize simulations.

These files can be used through the module like this:
```python
import axtools
args = axtools.read("example-system.tmpl.ax")
bodies = axtools.load(args, "example-system.ax")
```

Once the template has been read, we load it using the `axtools.load` function, which computes the simulation and dumps it to file (unless `path == ""`)

Now we can show it with:
```python
import axtools
args = axtools.read("example-system.ax")
axtools.show(args.limit.value, args.delta.value, *args.bodies)
```
The additional parameters can also be entered in here.

## Executable
Axinite will soon be coming to executable format! 

Development is still in progress.

## Gallery
![axinite-2](https://github.com/user-attachments/assets/2e952d41-5585-484d-bc3b-05c92aeefe2d)
![axinite-3](https://github.com/user-attachments/assets/ba434ce4-79a3-4a04-a7c4-45232d9fa11a)

## Todos
- Create executable
    - Add GUI?
- ~~Add live mode~~
