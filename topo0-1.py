import logging
from mininet.log import setLogLevel
from emuvim.dcemulator.net import DCNetwork
from emuvim.api.openstack.openstack_api_endpoint import OpenstackApiEndpoint
from emuvim.api.rest.rest_api_endpoint import RestApiEndpoint

logging.basicConfig(level=logging.INFO)
setLogLevel('info')  # set Mininet loglevel
logging.getLogger('werkzeug').setLevel(logging.DEBUG)

logging.getLogger('api.openstack.base').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.compute').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.keystone').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.nova').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.neutron').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.heat').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.heat.parser').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.glance').setLevel(logging.DEBUG)

class DemoTopology(DCNetwork):
    """
    This is a 2x2 PoP topology used for the emulator MANO integration demo.
    """

    def __init__(self):
        """
        Initialize multi PoP emulator network.
        """
        super(DemoTopology, self).__init__(
            monitor=True,
            enable_learning=True
        )

        # define members for later use
        self.pop1 = None
        self.pop2 = None

        self.sw1 = None

    def setup(self):
        self._create_switches()
        self._create_pops()
        self._create_links()
        self._create_rest_api_endpoints()
        self._create_openstack_api_endpoints()

    def _create_switches(self):
        self.sw1 = self.addSwitch("s1")

    def _create_pops(self):
        self.pop1 = self.addDatacenter("osm-pop1")
        self.pop2 = self.addDatacenter("osm-pop2")

    def _create_links(self):
        # OSM island
        self.addLink(self.pop1, self.sw1, delay="10ms")
        self.addLink(self.pop2, self.sw1, delay="10ms")


    def _create_openstack_api_endpoints(self):
        # create
        api1 = OpenstackApiEndpoint("172.0.0.101", 6001)
        api2 = OpenstackApiEndpoint("172.0.0.101", 6002)

        # connect PoPs
        api1.connect_datacenter(self.pop1)
        api2.connect_datacenter(self.pop2)

        # connect network
        api1.connect_dc_network(self)
        api2.connect_dc_network(self)

        # start
        api1.start()
        api2.start()

    def _create_rest_api_endpoints(self):
        # create
        apiR = RestApiEndpoint("0.0.0.0", 5001)

        # connect PoPs
        apiR.connectDatacenter(self.pop1)
        apiR.connectDatacenter(self.pop2)

        # connect network
        apiR.connectDCNetwork(self)

        # start
        apiR.start()

def main():
    t = DemoTopology()
    t.start()
    t.CLI()
    t.stop()


if __name__ == '__main__':
    main()
