import axinite as ax
import sys

args = sys.argv

if len(args) < 3:
    print("Usage: python main.py <command> <file>")
    sys.exit(1)
    
if args[1] == "load":
    ax.load(args[2])
elif args[1] == "show":
    ax.show(args[2])