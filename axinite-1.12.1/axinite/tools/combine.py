import axinite.tools as axtools
import json

def combine(meta: dict, file: dict, indent=4) -> str:
    """Combines a .meta.ax file and a .ax/.tmpl.ax file

    Args:
        meta (dict): A dictionary of the .meta.ax file
        file (dict): A dictionary of the .ax/.tmpl.ax file

    Returns:
        str: A JSON string of the combined data
    """
    metadata = json.loads(meta)
    filedata = json.loads(file)
    if "name" in metadata and "name" in filedata: del filedata['name']
    if "author" in metadata and "author" in filedata: del filedata['author']
    combined = {**metadata, **filedata}
    return json.dumps(combined, indent=indent)