import unittest
import logging
import sleekxmpp
import kestrel.plugins.kestrel_executor
import pprint
log = logging.getLogger(__name__)

logging.basicConfig()
log.setLevel(1)

class TestXmpp:
    def add_event_handler(a,b,c) :
        print("test")

    def __getitem__(self, index):
        print("get item")

    def __get_item__() :
        print("get item")

    def ___get_item___() :
        print("get item")

class HelloworldTestCase(unittest.TestCase):

    def test_create_plugin(self):
        xmpp = TestXmpp()
        config ={}
        executor = kestrel.plugins.kestrel_executor.kestrel_executor(xmpp,config)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint (executor)
        executor.plugin_init()
        print "init"
        executor.post_init()
        print "post init"

        event ={} 
#        executor.start(event)
#calls    self.xmpp['xep_0050'].add_command(self.xmpp.boundjid,
#AttributeError: 'NoneType' object has no attribute 'add_command'

        print "start"
        
        iq = {} 
        session = {}
#        executor._handle_task_command(iq, session)
# form = self.xmpp['xep_0004'].makeForm(ftype='form')

        name = "test"
        command = "ls -latr"
        executor._execute(name, command)

        command = "bash -x ./run_rendering.sh"
        cleanup = "bash -x ./cleanup_rendering.sh"
        executor._execute(name, command, cleanup)

        command = "./run_rendering.sh"
        cleanup = "./cleanup_rendering.sh"
        executor._execute(name, command, cleanup)

        command = "./run_rendering_fail.sh"
        cleanup = "./cleanup_rendering.sh"
        executor._execute(name, command, cleanup)


def suite():
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        suite.addTest(loader.loadTestsFromTestCase(HelloworldTestCase))
        return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
