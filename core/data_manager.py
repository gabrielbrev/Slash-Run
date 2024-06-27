import json

class DataManager:
    def __init__(self) -> None:
        try:
            with open("data.json", "r") as json_file:
                self._data: dict = json.load(json_file)
        except:
            print("Could not instantiate object")

    def write(self, key, data):
        if key in self._data.keys():
            self._data[key] = data
            try:
                with open("data.json", "w") as json_file:
                    json.dump(self._data, json_file, indent=4)
                    return 0
            except:
                print("Could not read file")
        return -1
        
    def read(self, key):
        try:
            with open("data.json", "r") as json_file:
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
    
    def get_current_level(self):
        return self.read("current_level")
    
    def update_current_level(self, level):
        if level >= self.get_current_level():
            self.write("current_level", level + 1)
    
    def set_accessed_editor(self, b: bool):
        self.write("accessed_editor", b)

    def has_accessed_editor(self):
        return self.read("accessed_editor")