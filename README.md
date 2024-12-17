# Axinite
A powerful open-source engine for advanced celestial mechanics.

![axinite-1](https://github.com/user-attachments/assets/bcd7bc7e-627e-44e5-bfc6-d2ddd787a208)

## Overview
**Axinite** is an engine for calculating celestial motion. 
You can use it to design your own solar systems, predict trajectories of rockets, simulate gravitational interactions and more.

Check out the docs [here](https://jewels86.gitbook.io/axinite/axinite/getting-started).
### What is `axtools`?
`axtools` is a library to help abstract and simplify Axinite. With `axtools`, Developers can deploy Axinite powered applications with ease. 
You can find the docs [here](https://jewels86.gitbook.io/axinite/axtools/quickstart).

## Usage
The `axinite` module can be downloaded from the [latest release](https://github.com/jewels86/Axinite/releases) and used in python code. 
`axinite` uses the `Body` class to condense planet data so it can be processed. Once the bodies have been initialized, they can then be passed into the `load` function along with simulation parameters.

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
    "bodies": [...]
}
```
These files can be used through the module like this:
```python
import axtools
args = axtools.read("example-system.tmpl.ax")
bodies = axtools.load(args, "example-system.ax")
```
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
![axinite-4](https://github.com/user-attachments/assets/af13ee05-f6ef-4d24-8446-39e6544df2ca)
![axinite-5](https://github.com/user-attachments/assets/c16db758-2ad2-47d8-9f1d-190727f9e881)


## Todos
- Create `ax-cli` executable
- Create `ax-gui` executable
- ~~Add live mode~~
