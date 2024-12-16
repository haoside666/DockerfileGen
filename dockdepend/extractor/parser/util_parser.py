import json
import pkgutil
from typing import Tuple, Any


def get_json_data(cmd_name) -> Tuple[Any, bool]:
    command_json_fn = f'{cmd_name}.json'
    # get man page data for command as dict
    try:
        json_data_bytes = pkgutil.get_data(__name__, 'command_flag_option_info/data/' + command_json_fn)
        flags = False
    except FileNotFoundError:
        try:
            json_data_bytes = pkgutil.get_data(__name__,
                                               'command_flag_option_info/data/_default_data_for_commands.json')
            flags = True
        except FileNotFoundError:
            raise Exception(f'json-File for default values not found.')
    json_data = json.loads(json_data_bytes)
    return json_data, flags
