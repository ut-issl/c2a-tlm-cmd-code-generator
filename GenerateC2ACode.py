# coding: UTF-8
"""
python 3.7以上を要求
"""

import json
import sys
import argparse

import my_mod.load_db
import my_mod.cmd_def
import my_mod.tlm_def
import my_mod.tlm_buffer

# 必要に応じてここを変える
SETTING_FILE_PATH = "../tlm_cmd_gen_config.json"


def load_settings(setting_file_path):
    if setting_file_path.endswith(".json"):
        with open(setting_file_path, mode="r") as fh:
            settings = json.load(fh)
    elif setting_file_path.endswith(".toml"):
        import toml
        settings = toml.load(setting_file_path)
        if "wings" in settings:
            del settings["wings"]
        selected_key = select_key(settings)
        if selected_key is None:
            raise ValueError("No key selected.")
        settings = settings[selected_key]["tlm_cmd_code_gen"]
    else:
        raise ValueError("Unsupported file format.")
    return settings


def select_key(data):
    while True:
        print("Select a key from the following options:")
        keys = list(data.keys())
        for i, key in enumerate(keys, start=1):
            print(f"{i}. {key}")
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(keys):
                return keys[choice - 1]
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    parser = argparse.ArgumentParser(description="Load settings from a configuration file.")
    parser.add_argument("setting_file_path", nargs="?", default=SETTING_FILE_PATH,
                        help="Path to the configuration file.")
    args = parser.parse_args()

    setting_file_path = args.setting_file_path
    settings = load_settings(setting_file_path)

    # print(settings["path_to_src"]);

    cmd_db = my_mod.load_db.LoadCmdDb(settings)
    tlm_db = my_mod.load_db.LoadTlmDb(settings)
    # pprint.pprint(cmd_db)
    # pprint.pprint(tlm_db)
    # print(tlm_db)

    my_mod.cmd_def.GenerateCmdDef(settings, cmd_db["sgc"])
    my_mod.cmd_def.GenerateBctDef(settings, cmd_db["bct"])
    my_mod.tlm_def.GenerateTlmDef(settings, tlm_db["tlm"])

    if settings["is_main_obc"]:
        my_mod.cmd_def.GenerateOtherObcCmdDef(settings, cmd_db["other_obc"])
        my_mod.tlm_def.GenerateOtherObcTlmDef(settings, tlm_db["other_obc"])
        my_mod.tlm_buffer.GenerateTlmBuffer(settings, tlm_db["other_obc"])

    print("Completed!")
    sys.exit(0)


if __name__ == "__main__":
    main()
