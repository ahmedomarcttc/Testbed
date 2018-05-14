import logging
from mininet.log import setLogLevel
from emuvim.dcemulator.net import DCNetwork
from emuvim.api.rest.rest_api_endpoint import RestApiEndpoint
from emuvim.api.openstack.openstack_api_endpoint import OpenstackApiEndpoint

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
logging.getLogger('api.openstack.helper').setLevel(logging.DEBUG)


def DemoTopology():
    net = DCNetwork(monitor=True, enable_learning=True)

    dc1 = net.addDatacenter("osm-pop1")
    dc2 = net.addDatacenter("osm-pop2")

    s1 = net.addSwitch("s1")

    net.addLink(dc1, s1)
    net.addLink(dc2, s1)

    # add OpenStack-like APIs to the emulated DC
    api1 = OpenstackApiEndpoint("127.0.0.1", 6001)
    api2 = OpenstackApiEndpoint("127.0.0.1", 6002)

    api1.connect_datacenter(dc1)
    api2.connect_datacenter(dc2)

    api1.start()
    api2.start()

    api1.connect_dc_network(net)
    api2.connect_dc_network(net)

    # add the command line interface endpoint to the emulated DC (REST API)
    Rapi = RestApiEndpoint("0.0.0.0", 5001)
    Rapi.connectDCNetwork(net)
    Rapi.connectDatacenter(dc1)
    Rapi.connectDatacenter(dc2)
    Rapi.start()

    net.start()
    net.CLI()
    # when the user types exit in the CLI, we stop the emulator
    net.stop()


def main():
    DemoTopology()


if __name__ == '__main__':
    main()
