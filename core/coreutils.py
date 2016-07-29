import json 

class JsonObject:
    '''
    Json utility class to serialize python class to json
    '''
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)