# -*-coding:utf-8 -*-
# !/usr/bin/env python3
import os
import sys
import argparse
import config
import differential
sys.path.append('../')
from logs import logs
import utils

class Build:
    def __init__(self, revision, diff, repo_uri, stage_uri, jenkinks_url):
        self.revision = revision
        self.diff = diff
        self.repo_uri = repo_uri
        self.stage_uri = stage_uri
        self.jenkinks_url = jenkinks_url
        self.repo = os.path.splitext(os.path.basename(repo_uri))[0]
        self.code_path = config.CODE_PATH
        self.repo_path = os.path.join(self.code_path, self.repo)
        self.build_status = 0
    
    def __run_build(self):
        # dry run
        q = differential.Query(self.diff, self.revision)
        statust = q.get_revision_status()
        logs.info("Revision status: %s" % statust)
        if str(statust) in ["3", "4"]:
            logs.warning("Revision was Closed or Abandoned")
            sys.exit(2)
        # TODO do other build
        diffs = q.get_diffs()
        if 2 > len(diffs):
            # set build result "fail"
            self.build_status = 1
        logs.info("Build status: %s" % self.build_status)
    
    def __feedback(self):
        revision_edit = differential.RevisionEdit(self.diff, self.revision)
        revision_edit.remove_reviewer()
        if self.build_status:
            revision_edit.add_reviewer()
            revision_edit.set_revision_status("reject")
        title_msg = "IMPORTANT: build fail" if self.build_status else "NOTE: build pass"
        logs.info("Title msg: %s" % title_msg)
        table_msg = """| Build | Klockworks | Coverity | UT/FT 
                       | ----- | ----- | ----- | ----- 
                       | {iconfont} | {iconfont} | {iconfont} | {iconfont} 
                       | [[{url} | Link]] | [[{url} | Link]] | [[{url} | Link]] | [[{url} | Link]] 
                    """.format(
                        iconfont='{icon times color=red}' if self.build_status else '{icon check color=green}',
                        url=self.jenkinks_url)
        revision_edit.feedback(title_msg + "\n\n" + table_msg)
        logs.info(table_msg)


    def __update_db(self):
        # TODO update db
        pass
    
    def exec_build(self):
        self.__run_build()
        self.__feedback()
        self.__update_db()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script for build')
    parser.add_argument('revision', help='revision id')
    parser.add_argument('diff', help='diff id')
    parser.add_argument('repo_uri', help='repo uri')
    parser.add_argument('stage_uri', help='stage uri')
    parser.add_argument('jenkinks_url', help='jenkinks url')
    args = parser.parse_args()
    logs.info(args)
    build = Build(args.revision, args.diff, args.repo_uri, args.stage_uri, args.jenkinks_url)
    build.exec_build()