import re
from configparser import ConfigParser

def check_reachability_from_openstack(conn, tag, inventory_file, group_name="webservers"):
    def get_expected_hosts(inventory_file, group_name):
        config = ConfigParser(allow_no_value=True, delimiters=("="))
        config.optionxform = str  # Preserve case
        config.read(inventory_file)
        if group_name not in config:
            raise ValueError(f"Group '{group_name}' not found in inventory")
        return set(config[group_name].keys())

    def get_active_tagged_servers(conn, tag):
        servers = conn.compute.servers()
        pattern = re.compile(f"^{tag}_dev\\d+$")
        return set(
            server.name
            for server in servers
            if pattern.match(server.name)
        )

    group_hosts = get_expected_hosts(inventory_file, group_name)

    active_servers = get_active_tagged_servers(conn, tag)

    reachable_hosts = group_hosts & active_servers
    unreachable_hosts = group_hosts - active_servers

    return reachable_hosts, unreachable_hosts
