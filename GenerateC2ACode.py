# coding: UTF-8
"""
python 3.7以上を要求
"""

import json
import sys

import my_mod.load_db
import my_mod.cmd_def
import my_mod.tlm_def
import my_mod.tlm_buffer

# 必要に応じてここを変える
SETTING_FILE_PATH = "../tlm_cmd_gen_config.json"


def main():
    with open(SETTING_FILE_PATH, mode="r") as fh:
        settings = json.load(fh)
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
