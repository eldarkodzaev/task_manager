import json


class CheckJson:
    
    def __init__(self, file: str):
        self.file = file
        
    def check_decode(self):
        with open(self.file, "r", encoding="utf-8") as json_file:
            try:
                _ = json.load(json_file)
            except json.JSONDecodeError:
                print("Структура JSON нарушена")