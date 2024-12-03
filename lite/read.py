import axinite as ax
from lite import AxiniteArgs
import json

def read_template(path: str):
    with open(path, 'r') as f:
        data = json.load(f)
        
        args = AxiniteArgs()