import os

from settings import PRESET_PATH


def get_preset_dir_names():
    return [f.name for f in os.scandir(PRESET_PATH) if f.is_dir()]


def get_presets_dict():
    dirs = get_preset_dir_names()
    presets = {}

    for dir_ in dirs:
        try:
            presets[dir_] = os.path.join(PRESET_PATH,
                                         dir_,
                                         os.listdir(os.path.join(PRESET_PATH, dir_))[0])
        except IndexError:
            print(f"Directory: '{dir_}' is empty and will not be loaded as preset tab.")
            pass
    return presets
