import json

string = '{"name": "John", "age": "true"}'
json_obj = json.loads(string)
print(json_obj)