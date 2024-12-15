import axtools
import sys

if sys.argv[1] == "load":
    args = axtools.read(sys.argv[2])
    axtools.load(args, sys.argv[3])
if sys.argv[1] == "show":
    args = axtools.read(sys.argv[2])
    axtools.show(args.limit.value, args.delta.value, *args.bodies, radius_multiplier=args.radius_multiplier, speed=args.rate, retain=args.retain)
if sys.argv[1] == "live":
    args = axtools.read(sys.argv[2])
    axtools.live(args.limit, args.delta, args.t, *args.bodies, radius_multiplier=args.radius_multiplier, rate=args.rate, retain=args.retain)