#!/usr/bin/env python

import sys
import random
import logging
from cli import cli
from api import api

class margaritashotgun():

    def __init__(self):
        self.logger = logging.getLogger('margarita_shotgun')
        streamhandler = logging.StreamHandler(sys.stdout)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(aasctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        streamhandler.setFormatter(formatter)
        self.logger.addHandler(streamhandler)

    def set_config(self, config):
        a = api()
        self.config = config
        if a.invalid_config(self.config):
            self.logger.info("config_verify_fail exiting")
            return False
        else:
            return True


    def run(self):
        c = cli()
        a = api()
        self.config = c.parse_args()
        # check config is valid
        if a.invalid_config(self.config):
            self.logger.info("config_verify_fail exiting")
            quit()

        for host in self.config['hosts']:
            port   = a.select_port(host)
            auth   = a.select_auth_method(host)
            tun    = a.establish_tunnel(host, port, auth)
            remote = a.establish_remote_session(host, port, auth)
            if remote.test_conn() == False:
                self.logger.info("SSH connection failed ... exiting")
                quit()
            tun_port = random.randint(32768, 61000)
            a.install_lime(host, remote, tun_port)
            a.dump_memory(self.config, host, tun, remote, tun_port)

if __name__=="__main__":
    ms = margaritashotgun()
    ms.run()

