#!/usr/bin/env python
#
# Copyright (c) 2022,2023 Eric Gustafson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""The nordrunner program"""

import requests

from jinja2 import Environment, PackageLoader


NORD_API = 'https://api.nordvpn.com/v1/servers/recommendations'
NORD_TEMPLATE = 'nordvpn.ovpn'

HTTP_PROXIES = {
    'http': 'http://proxy.elfwerks:3128',
    'https': 'http://proxy.elfwerks:3128',
}

LOCAL_ROUTER = 'gw 10.3.4.254 dev ens192'


def fetch_recommended():
    '''fetch the NordVPN recommended server'''
    result = requests.get(NORD_API, proxies=HTTP_PROXIES)
    j = result.json()
    return j


def print_recommendation(reco):
    '''print_recommendation'''
    print("id:       {}".format(reco[0]['id']))
    print("ip:       {}".format(reco[0]['station']))
    print("hostname: {}".format(reco[0]['hostname']))


def generate_ovpn(reco):
    '''generate an ovpn configuration file from the recommendation'''
    env = Environment(
        loader=PackageLoader(__name__)
    )
    template = env.get_template(NORD_TEMPLATE)
    return template.render(reco[0])


def install_host_route(host_ip):
    '''install host route to Nord endpoint'''
    route_cmd = "route add -host {} {}".format(host_ip, LOCAL_ROUTER)
    print("> {}".format(route_cmd))


def main():
    '''the Main program'''
    #print("nordrunner - stubbed out, running...")
    reco = fetch_recommended()
    #print(json.dumps(reco))
    print_recommendation(reco)
    print("__name__: {}".format(__name__))
    print("----")
    ovpn_config = generate_ovpn(reco)
    #print(ovpn_config)
    install_host_route(reco[0]['station'])


if __name__=='__main__':
    main()

#
# Strategy:
#
# Assumptions:
# - Static openvpn config in etc dir (/etc/openvpn)
#   - nordvpn.auth file (as possibly configed in template)
#   - hook scripts specified in .ovpn template
# - Template .ovpn file provided:
#   - ?? /etc/openvpn/nordvpn.ovpn.j2
#
# 1. Fetch recommended endpoint from nord
# 2. Generate Config for endpoint --> where (what dir)
#    - /etc/openvpn/nordvpn  (NORD_CONF_DIR)
# 3. Pre-up hooks (install point route to endpoint)
# 4. exec openvpn w/ flags
#
