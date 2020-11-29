import json
import jsonschema
from pathlib import Path


p = Path('.')
schema_path = p / 'task_folder' / 'schema'
event_path = p / 'task_folder' / 'event'

schemas_filenames = [filename for filename in schema_path.glob('*.schema')]
events_filenames = list(event_path.glob('*.json'))
events_valid = [False] * len(events_filenames)


def is_valid(json_data, json_schema):
    try:
        jsonschema.validate(instance=json_data, schema=json_schema)
    except jsonschema.exceptions.ValidationError as err:
        return False, err
    else:
        return True


for schema_name in schemas_filenames:
    with open(schema_name, 'r') as file:
        s = file.read()
        schema = json.loads(s)
    for i in range(len(events_filenames)):
        if events_valid[i] != True:
            event_name = events_filenames[i]
            with open(event_name, 'r') as file:
                e = file.read()
                event = json.loads(e)
            events_valid[i] = is_valid(event, schema)
        
print(events_valid)   

