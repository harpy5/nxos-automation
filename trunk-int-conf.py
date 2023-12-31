from ncclient import manager
from ncclient.xml_ import new_ele, sub_ele

import os

# Replace these with your Nexus 9000 device details
#DEVICE_IP = "10.85.48.163"
NETCONF_PORT = 830
#USERNAME = "cisco"
#PASSWORD = "cisco"
DEVICE_IP = os.environ.get('DEVICE_IP')

USERNAME = os.environ.get('USER_NAME')
PASSWORD =os.environ.get('PASSWORD')

def configure_interface(interface_name, allowed_vlans):
    # NETCONF template for interface configuration
    trunk_config = f"""<config>
        <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
            <intf-items>
                <phys-items>
                    <PhysIf-list>
                        <id>{interface_name}</id>
                        <adminSt>up</adminSt>
                        <layer>Layer2</layer>
                        <descr>Full intf config via NETCONF</descr>
                        <mode> trunk </mode>
                        <trunkVlans>{allowed_vlans}</trunkVlans>
                    </PhysIf-list>
                </phys-items>
            </intf-items>
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
            m.edit_config(target='running', config=trunk_config)

            print(f"Interface {interface_name} configured successfully as trunk")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
     allowed_vlans = os.environ.get('ALLOWED_VLANS')
     interface_name = os.environ.get('INTERFACE_NAME')

     configure_interface(interface_name, allowed_vlans)
