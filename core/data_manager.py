import json

class DataManager:
    def __init__(self) -> None:
        try:
            with open("game_data.json", "r") as json_file:
                self._data: dict = json.load(json_file)
        except:
            print("Could not access game data")

    def write(self, key, data):
        if key in self._data.keys():
            self._data[key] = data
            try:
                with open("game_data.json", "w") as json_file:
                    json.dump(self._data, json_file, indent=4)
                    return 0
            except:
                print("Could not read file")
        return -1
        
    def read(self, key):
        try:
            with open("game_data.json", "r") as json_file:
                self._data: dict = json.load(json_file)
        except:
            print("Could not read file")
            return
        if key in self._data.keys():
            return self._data[key]
        
    def get_data_dict(self):
        return self._data
    
    def reset_data(self):
        self.write("current_level", 1)
        self.write("accessed_editor", False)
        self.write("music_volume", 50)
        self.write("sfx_volume", 50)
        self.write("first_boot", True)
    
    def get_current_level(self):
        return self.read("current_level")
    
    def update_current_level(self, level):
        if level >= self.get_current_level():
            self.write("current_level", level + 1)
    
    def set_accessed_editor(self, b: bool):
        self.write("accessed_editor", b)

    def has_accessed_editor(self):
        return self.read("accessed_editor")
    
    def set_music_volume(self, v):
        self.write("music_volume", v)

    def get_music_volume(self):
        return self.read("music_volume")
    
    def set_sfx_volume(self, v):
        self.write("sfx_volume", v)

    def get_sfx_volume(self):
        return self.read("sfx_volume")
    
    def set_fisrt_boot(self, b: bool):
        self.write("first_boot", b)

    def is_first_boot(self):
        return self.read("first_boot")
    
    def verify_game_files(self):
        def create_if_not_exists(path, data):
            try:
                open(path, "r")
            except FileNotFoundError:
                with open(path, "w") as json_file:
                    json.dump(data, json_file)

        create_if_not_exists("game_data.json", {
            "first_boot": True,
            "current_level": 1,
            "accessed_editor": False,
            "music_volume": 50,
            "sfx_volume": 50
        })
        for i in range(4):
            create_if_not_exists(f"levels/{i}/back.json", {})
            create_if_not_exists(f"levels/{i}/front.json", {})