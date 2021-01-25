import os
import yaml

class Config:

    def __init__(self):
        with open("config/config.yml", "r") as yml_config_file:
            cfg = yaml.load(yml_config_file, Loader=yaml.FullLoader)
        config_keys = cfg.keys()
        for k in config_keys:
            setattr(self, k, cfg.get(k))
        # if (os.path.isfile(self.path+"/conf/config-override.yaml") ):
        #     stream = open(self.path+"/conf/config-override.yaml", 'r')
        #     data = yaml.load(stream)
        #     config_keys = data.keys()
        #     for k in config_keys:
        #         setattr(self, k, data.get(k))

config = Config()