import axinite.tools as axtools
import json

def combine(meta, file):
    """Combines a .meta.ax file and a .ax/.tmpl.ax file

    Args:
        meta (str): _description_
        file (_type_): _description_

    Returns:
        _type_: _description_
    """
    metadata = json.loads(meta)
    filedata = json.loads(file)
    if "name" in metadata and "name" in filedata: del filedata['name']
    if "author" in metadata and "author" in filedata: del filedata['author']
    combined = {**metadata, **filedata}
    return json.dumps(combined)