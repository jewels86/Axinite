# Axinite Changelog
Axinite uses a derivative of the **semantic versioning system** to record changes to the library. 
- Major increments represent a rework or a revamp of the module.
- Minor increments represent new functionality or a milestone/accumulation of patch increments.
- Patch increments represent bug fixes, modifications that don't directly affect users, progress towards a milestone/goal, or other small changes.

Although releases are only created for every minor or major increment, patch increments are still uploaded to PyPI.
## 1.24.3-1.24.8 (1/18/25)
- Implemented timestep scaling in `vpython_frontend`
## 1.24.2 (2/16/25)
- Added imperial units and time units to interpret and conversion functions
## 1.24.0-1.24.1 (2/15/25)
- `mpl_frontend` finished
## 1.23.1 - 1.23.2 (2/14/25)
- Fixed bug where changing deltas or limits caused random crashes
## 1.23.0 (2/5/25)
- Error handling in `axtools` and `axinite`
## 1.22.17 (2/5/25)
- Removed accidental mention of `astropy.units` in `load`
## 1.22.16 (2/3/25)
- Fixed combine method including the path attribute
## 1.22.11 - 1.22.15 (2/1/25)
- Made sure to include `scipy` in the dependencies
- Stopped VPython from opening on import
- Created `axtools.reads` and `axtools.saves` methods 
## 1.22.8-1.22.10 (1/30/25)
- Again, fixed VPython static frontend
## 1.22.6-1.22.7 (1/30/25)
- Added basic math to interpret functions
## 1.22.1-1.22.5 (1/29/25)
- Fixed VPython static frontend
- Created modifier utilities (normal force, magnetic force, modifier_from)
- Added `energy_of` methods for energy of specific bodies
- Added `can_see` methods for line of sight checks
## 1.22 (1/26/35)
- Created RK2-4 backends
## 1.21 (1/25/25)
- Added approximation, collisions, energy, intersections, and momentum to `axana`
- Added aliases to the `__init__.py` file of `axinite` to allow for faster imports
## 1.20.5 (1/22/25)
- Fixed VPython live so it isn't as slow
## 1.20 (1/18/25)
- Added `time_to`, `mass_to`, and `distance_to` methods
## 1.19.1 (1/16/25)
- Added `state` method
## 1.18-1.19 (1/15/25)
- `axana` includes quaternions now
- Added `axinite.analysis`/`axana`
## 1.12.3-1.17.3 (1/13/25)
- Fixed load function problem with carriage return
- Automatic type checking in bodies
- `timestep` method
- Updated all docstrings
- Added better verbosity for axtools loading
- Speed up data saving a bit
- Bug fixes for backend errors when handling outer bodies
## 1.12.0-1.12.2 (1/11/25)
- Fixed live mode problems
- Fixed VPython errors with inner bodies
- Roughly removed AstroPY
- Added inner and outer bodies to decrease overhead
## 1.11.16-1.11.19 (1/9/25)
- Fixed error in `axtools.load`'s default action method 
- Fixed some `combine` method indent problems