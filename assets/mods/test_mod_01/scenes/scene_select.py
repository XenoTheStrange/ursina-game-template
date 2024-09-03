from scripts.mod_utils import after_hook

@after_hook("scenes.scene_select.loader")
def stacking_wrappers_oh_my(entities_list, *args, **kwargs):
    print("AAAAAAAAAA This should happen first")
    return entities_list
