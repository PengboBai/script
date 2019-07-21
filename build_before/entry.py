# -*-coding:utf-8 -*-
# !/usr/bin/env python3
import sys
from differential import Differential
sys.path.append('../')
from logs import logs
import argparse

"""
feedback to phabricator start build message
record data to database
"""

class Entry:
    def __init__(self, revision, diff, repo_uri, stage_uri):
        self.revision = revision
        self.diff = diff
        self.repo_uri = repo_uri
        self.stage_uri = stage_uri
        self.differential = Differential(self.diff, self.revision)
    
    def __record_data(self):
        logs.info("Record data to database")

    def __feedback(self):
        msg = "NOTE: Trigger build success, please wait build result."
        self.differential.feedback(msg)

    def exec_entry(self):
        self.__record_data()
        self.__feedback()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build entry')
    parser.add_argument('revision', help='revision id')
    parser.add_argument('diff', help='diff id')
    parser.add_argument('repo_uri', help='repo uri')
    parser.add_argument('stage_uri', help='stage uri')
    args = parser.parse_args()
    logs.info(args)
    entry = Entry(args.revision, args.diff, args.repo_uri, args.stage_uri)
    entry.exec_entry()
