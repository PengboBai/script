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


class Update:
    def __init__(self, revision, diff, repo_uri, stage_uri):
        self.revision = revision
        self.diff = diff
        self.repo_uri = repo_uri
        self.stage_uri = stage_uri
        self.repo = os.path.splitext(os.path.basename(repo_uri))[0]
        self.code_path = config.CODE_PATH
        self.repo_path = os.path.join(self.code_path, self.repo)
        self.qd = differential.QueryDiffs(self.diff, self.revision)
        self.branch = self.qd.get_base_branch()
        self.user_name = self.qd.get_user_name()

    def __update_code(self):
        """
        update repo code and merge tag
        """
        logs.info("BRANCH： %s" % self.branch)
        logs.info("USRE_NAME: %s" % self.user_name)
        utils.mkdirs(self.code_path)
        utils.clone_repo(self.repo_path, self.repo_uri)
        os.chdir(self.repo_path)
        cmd_list = [
            'git clean -df', 'git reset --hard', 
            'git branch | grep "\* {branch}" || git checkout {branch}'.format(branch=self.branch),
            'git fetch', 'git reset --hard origin/{branch}'.format(branch=self.branch),
            'git remote remove STAGE || echo "del stage remote"',
            'git remote add STAGE {stage_uri}'.format(stage_uri=self.stage_uri),
            'git fetch STAGE tag phabricator/diff/{diff}'.format(diff=self.diff),
            'git merge phabricator/diff/{diff}'.format(diff=self.diff),
        ] 
        try:
            for cmd in cmd_list:
                utils.call(cmd)
        except Exception as e:
            logs.error(e)
            raise Exception("Merge tag fail" if "git merge" in str(e) else "Update code fail")

    def exec_update(self):
        try:
            self.__update_code()
        except Exception as e:
            self.qd.feedback("IMPORTANT: %s" % str(e))
            # TODO update db
            # exit code 
            # 1 set job FAILURE, env error
            # 2 set job UNSTABLE, merge fails
            sys.exit(2 if "Merge tag fail" in str(e) else 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script for update code')
    parser.add_argument('revision', help='revision id')
    parser.add_argument('diff', help='diff id')
    parser.add_argument('repo_uri', help='repo uri')
    parser.add_argument('stage_uri', help='stage uri')
    args = parser.parse_args()
    logs.info(args)
    update = Update(args.revision, args.diff, args.repo_uri, args.stage_uri)
    update.exec_update()