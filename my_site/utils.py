from django.db.models import ForeignKey
from django.db.models.fields.related import OneToOneField


def getDictionary(object, exclude=[], rename={}, deepth=0):
    """
    Get dictionary from model
    Args:
         :param object (django.db.models.Model): - model or iterable of models
         :param exclude (list): list of keys to exclude from dictionary
         :param rename (dict): dict of keys to rename in dictionary from key: to value:
         :param deepth (int): how deep recursively go to related objects
         Note:
             Be careful choosing name of keys, you can replays existent ones
    Returns:
        dict: return dictionary with all fields of model except those, that was excluded
        """
    # exclude += ["_state"]
    if "_state" in object.__dict__:
        data = renameKeys(deleteKey(object, exclude, deepth), rename)
    else:
        data = [renameKeys(deleteKey(o, exclude, deepth), rename) for o in object]
    return data


def deleteKey(object, keys, deepth):
    data = object.__dict__
    getForingObjects(object, data, deepth)
    for key in keys:
        if key in data: del data[key]
    return deleteGeneratedKeys(data)


def getForingObjects(object, data, deepth):
    if deepth > 0:
        for value in object._meta.fields:
            if isinstance(value, ForeignKey) and value.column in data:
                o = getattr(object, value.name)
                if isinstance(value, OneToOneField):
                    id = data["id"]
                    data.update(deleteGeneratedKeys(
                        getForingObjects(o, o.__dict__, deepth - 1)))
                    data["id"] = id
                else:
                    data[value.name] = deleteGeneratedKeys(
                        getForingObjects(o, o.__dict__, deepth - 1))
                    del data[value.column]
    return data


def deleteGeneratedKeys(data):
    for key in list(data.keys()):
        if key.startswith("_"):
            del data[key]
    return data


def renameKeys(data, keys):
    for oldKey, newKey in keys.items():
        if oldKey in data:
            data[newKey] = data[oldKey]
            del data[oldKey]
    return data
