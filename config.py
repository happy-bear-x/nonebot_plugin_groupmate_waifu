from pydantic import BaseModel, Extra

class Config(BaseModel, extra=Extra.ignore):
    waifu_cd_bye :int = 3600
    waifu_save:bool = True
    waifu_reset:bool = False
    waifu_he :int = 10
    waifu_be :int = 20
    waifu_ntr :int = 10
    yinpa_he :int = 50
    yinpa_be :int = 0
    yinpa_cp :int = 65
