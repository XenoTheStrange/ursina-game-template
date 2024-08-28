#The purpose of this is to see if I can import it relatively from the scene in ../scenes
# this sort of import does the following:
# 1. No more __init__.py inside of the mod folder root next to mod_info.json (this is 1 less __init__.py file per mod)
# 1.5 I was also able to remove the init file from the mods folder, so now it contains only other folders
# Change imports from this: from mods.test_mod_2.classes.import_test import Test
# to this: from ..classes.import_test import Test  , leaving out mods.mod_name and using .. instead

class Test:
    def __init__(self):
        self.yeet = "yeet"
    def speak(self):
        return self.yeet
