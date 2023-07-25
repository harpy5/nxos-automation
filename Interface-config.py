from ncclient import manager
from ncclient.xml_ import new_ele, sub_ele
from cryptography.hazmat.backends import default_backend
import warnings
import os

warnings.filterwarnings("ignore", message=" Python 3.6 is no longer supported by the Python core team. Therefore, support for it is deprecated in cryptography. The next release of cryptography will remove support for Python 3.6")

# Replace these with your Nexus 9000 device details
#DEVICE_IP = "10.85.48.163"
NETCONF_PORT = 830
#USERNAME = "cisco"
#PASSWORD = "cisco"

def configure_interface():
    # NETCONF template for interface configuration

    DEVICE_IP = os.environ.get('DEVICE_IP')
    ip_address = os.environ.get('IP_ADDRESS')
    interface_name = os.environ.get('INTERFACE_NAME')
    netmask = os.environ.get('SUBNET_MASK')
    USERNAME = os.environ.get('USER_NAME')
    PASSWORD =os.environ.get('PASSWORD')

    add_ip_interface = f"""<config>
        <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
            <intf-items>
                <phys-items>
                    <PhysIf-list>
                        <id>{interface_name}</id>
                        <adminSt>up</adminSt>
                        <layer>Layer3</layer>
                        <descr>Full intf config via NETCONF</descr>
                    </PhysIf-list>
                </phys-items>
            </intf-items>
            <ipv4-items>
                <inst-items>
                    <dom-items>
                        <Dom-list>
                            <name>default</name>
                            <if-items>
                                <If-list>
                                    <id>{interface_name}</id>
                                    <addr-items>
                                        <Addr-list>
                                            <addr>{ip_address}</addr>
                                        </Addr-list>
                                    </addr-items>
                                </If-list>
                            </if-items>
                        </Dom-list>
                    </dom-items>
                </inst-items>
            </ipv4-items>
        </System>
        </config>"""

    try:
        with manager.connect(
            host=DEVICE_IP,
            port=NETCONF_PORT,
            username=USERNAME,
            password=PASSWORD,
            hostkey_verify=False,
        ) as m:

            # Send the interface configuration to the device
            m.edit_config(target='running', config=add_ip_interface)

            print(f"Interface {interface_name} configured successfully with IP address {ip_address}/{netmask}.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    #interface_name = "eth1/1"  # Replace this with the name of the interface you want to configure
    #ip_address = "192.168.10.2/30"    # Replace this with the desired IP address for the interface
    #netmask = "255.255.255.252"      # Replace this with the desired netmask for the interface
   

    configure_interface()
