# Axinite Changelog
Axinite uses a derivative of the **semantic versioning system** to record changes to the library. 
- Major increments represent a rework or a revamp of the module.
- Minor increments represent new functionality or a milestone/accumulation of patch increments.
- Patch increments represent bug fixes, modifications that don't directly affect users, progress towards a milestone/goal, or other small changes.

Although releases are only created for every minor or major increment, patch increments are still uploaded to PyPI.
# 1.22.1 (1/29/25)
- Added `can_see` methods for line of sight checks
# 1.22 (1/26/35)
- Created RK2-4 backends
# 1.21 (1/25/25)
- Added approximation, collisions, energy, intersections, and momentum to `axana`
- Added aliases to the `__init__.py` file of `axinite` to allow for faster imports
# 1.20.5 (1/22/25)
- Fixed VPython live so it isn't as slow
# 1.20 (1/18/25)
- Added `time_to`, `mass_to`, and `distance_to` methods
# 1.19.1 (1/16/25)
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