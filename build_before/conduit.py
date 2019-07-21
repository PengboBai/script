# -*-coding:utf-8 -*-
# !/usr/bin/env python3
import sys
import time
import requests
import config
sys.path.append("../")
from logs import logs

class Conduit:
    def __init__(self, api_token=config.PHA_CONFIG["BOT_API_TOKEN"], pha_url=config.PHA_CONFIG["PHA_URL"]):
        self.api_token = api_token
        self.pha_url = pha_url + 'api/'

    def call_api(self, method, params):
        for i in range(5):
            try:
                return self.__call_api(method, params)
            except Exception as e:
                logs.error(e)
                logs.error("Call pha conduit api exception!")
                time.sleep(3)
                if 4 == i:
                    raise Exception(e)

    def __call_api(self, method, params):
        data = self.__format_params(params)
        response = requests.post(self.pha_url + method, data=data, proxies={}, headers={'Connection': 'close'}).json()
        if response["error_code"]:
            logs.error("[Conduit api [%s] response msg: %s" % (method, response))
            raise Exception(response["error_code"])
        return response

    def __format_params(self, params):
        # params = {
        #     "objectIdentifier": self.revision,
        #     "transactions": [{"type": "reviewers.remove", "value": [reviewer_phid]}]
        # }
        data = {'api.token': self.api_token}
        for name, value in params.items():
            if isinstance(value, list):
                for i in range(len(value)):
                    if isinstance(value[i], dict):
                        for key, info in value[i].items():
                            if isinstance(info, list):
                                for info_index, info_value in enumerate(info):
                                    data["{name}[{index}][{key}][{info_index}]".format(
                                        name=name, index=i, key=key, info_index=info_index)] = info_value
                            else:
                                data["{name}[{index}][{key}]".format(name=name, index=i, key=key)] = info
                    else:
                        data["{name}[{index}]".format(name=name, index=i)] = value[i]
            else:
                data[name] = value
        logs.debug("Format conduit data: %s" % data)
        return data


if __name__ == "__main__":
    conduit = Conduit()
    # conduit.call_api("differential.revision.edit", {"objectIdentifier": 1,
    #                                                 "transactions": [{"type": "title", "value": "test title"},
    #                                                                  {"type": "testPlan", "value": "no"}]})
    # conduit.call_api("differential.close", {"revisionID": 1})
    result = conduit.call_api("differential.querydiffs", {"ids[0]": 1})
    logs.info(result)
