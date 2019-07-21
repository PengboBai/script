# -*- coding:utf-8 -*-
# !/usr/bin/env python3
import sys
import config
from conduit import Conduit
sys.path.append("../")
from logs import logs


class Differential:
    def __init__(self, diff, revision, api_token=config.PHA_CONFIG["BOT_API_TOKEN"]):
        self.api_token = api_token
        self.diff = diff
        self.revision = revision
        self.method = None
        self.conduit = Conduit(api_token=self.api_token)

    def feedback(self, msg):
        """
        create comment msg to phabricator
        """
        params = {'revision_id': self.revision, 'message': msg}
        self.conduit.call_api('differential.createcomment', params)


class Query(Differential):
    def __init__(self, diff, revision):
        super().__init__(diff, revision)
        self.method = "differential.query"
        self.data = {}
        self.__init_data()

    def __init_data(self):
        res = self.conduit.call_api(self.method, {"ids[0]": self.revision})
        if res.get("result", None):
            try:
                self.data = res["result"][0]
            except Exception as e:
                logs.error(e)
                logs.error("QueryDiffs, get data fail: %s" % res)
                raise Exception(e)

    def get_revision_status(self):
        """
        0 Needs Review
        2 Accepted
        3 Closed
        4 Abandoned
        :return:
        """
        return self.data["status"]

    def get_repo_phid(self):
        return self.data["repositoryPHID"]

    def get_diffs(self):
        return self.data["diffs"]


class QueryDiffs(Differential):
    def __init__(self, diff, revision):
        super().__init__(diff, revision)
        self.method = "differential.querydiffs"
        self.data = {}
        self.__init_data()

    def __init_data(self):
        res = self.conduit.call_api(self.method, {"ids[0]": self.diff})
        if res.get("result", None):
            try:
                self.data = res["result"][str(self.diff)]
            except Exception as e:
                logs.error(e)
                logs.error("QueryDiffs, get data fail: %s" % res)
                raise Exception(e)

    def get_base_branch(self):
        try:
            return self.data['properties']['arc:onto'][0]['name']
        except:
            return "error"

    def get_user_name(self):
        return self.data.get("authorName", "error")


class RevisionEdit(Differential):
    def __init__(self, diff, revision):
        super().__init__(diff, revision)
        self.method = "differential.revision.edit"

    def remove_reviewer(self, reviewer_phid=config.PHA_CONFIG["BOT_PHID"]):
        params = {
            "objectIdentifier": self.revision,
            "transactions": [{"type": "reviewers.remove", "value": [reviewer_phid]}]
        }
        self.conduit.call_api(self.method, params)

    def add_reviewer(self, reviewer_phid=config.PHA_CONFIG["BOT_PHID"]):
        params = {
            "objectIdentifier": self.revision,
            "transactions": [{"type": "reviewers.add", "value": [reviewer_phid]}]
        }
        self.conduit.call_api(self.method, params)

    def set_revision_status(self, action):
        """
        reject: can not arc land
        """
        params = {
            "objectIdentifier": self.revision,
            "transactions": [{"type": action}]
        }
        self.conduit.call_api(self.method, params)


if __name__ == "__main__":
    query_diff = QueryDiffs('1', '1')
    logs.info(query_diff.get_user_name())
