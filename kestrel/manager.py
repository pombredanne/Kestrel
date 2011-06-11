"""
    Kestrel: An XMPP-based Job Scheduler
    Copyright (C) 2011 Lance Stout
    This file is part of Kestrel.

    See the file LICENSE for copying permission.
"""

import logging
#logging.basicConfig()

#


import random

import sleekxmpp
from sleekxmpp.xmlstream import JID

log = logging.getLogger(__name__)

class Manager(sleekxmpp.ComponentXMPP):

    def __init__(self, jid, password, host, port, config):
#        log = logging.getLogger(__name__)
        print ("get logger")
#        log.setLevel(logging.DEBUG)
#        print "init manager2"
        log.debug("in manager class2 ")
        log.debug("now setup the component ")
        logging.log(logging.DEBUG, "logging for debugging should work now.2")
        print (jid, password, host, port)
        log.debug("now setup the component ")
        sleekxmpp.ComponentXMPP.__init__(self, jid, password, host, port)

        self.config = config

        print ("config",self.config)
        print ("pool",self.config['pool'])
        print ("jobs",self.config['jobs'])
        print ("redis host",self.config['redis']['host'])
        print ("redis port",self.config['redis']['port'])
        print ("redis db",self.config['redis']['database'])

        self.redis_config = {
                'host': self.config['redis']['host'],
                'port': self.config['redis']['port'],
                'db': self.config['redis']['database']}

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0092')
        self.register_plugin('xep_0004',
                             module='kestrel.plugins.xep_0004')
        self.register_plugin('xep_0050', {'threaded': False})
        self.register_plugin('xep_0199',
                             {'keepalive': False})
        self.register_plugin('redis_queue',
                             self.redis_config,
                             module='kestrel.plugins.redis_queue')
        self.register_plugin('redis_id',
                             self.redis_config,
                             module='kestrel.plugins.redis_id')
        self.register_plugin('redis_adhoc',
                             self.redis_config,
                             module='kestrel.plugins.redis_adhoc')
        self.register_plugin('redis_roster',
                             self.redis_config,
                             module='kestrel.plugins.redis_roster')


        self.register_plugin(
                'kestrel_manager',
                {'pool_jid': JID(self.config['pool']),
                 'job_jid': JID(self.config['jobs'])},
                module='kestrel.plugins.kestrel_manager')

        self.add_event_handler("session_start", self.start)

        self['xep_0030'].add_identity(jid=self.boundjid.full,
                                      category='component',
                                      itype='generic',
                                      name='Kestrel',
                                      lang='en')
        print ("init finished, now waiting ")

    def start(self, event):
        print ("starting manager")
        for comp_jid in self.roster:
            for jid in self.roster[comp_jid]:
                self.send_presence(pfrom=comp_jid, pto=jid)
                self.send_presence(pfrom=comp_jid, pto=jid, ptype='probe')
