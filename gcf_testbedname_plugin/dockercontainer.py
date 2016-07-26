#----------------------------------------------------------------------
# Copyright (c) 2011-2016 Raytheon BBN Technologies
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and/or hardware specification (the "Work") to
# deal in the Work without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Work, and to permit persons to whom the Work
# is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Work.
#
# THE WORK IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE WORK OR THE USE OR OTHER DEALINGS
# IN THE WORK.
#----------------------------------------------------------------------

from __future__ import absolute_import

from gcf_to_docker import DockerManager

from gcf.geni.am.resource import Resource
from lxml import etree
import uuid
import subprocess

class DockerContainer(Resource):

    DEFAULT_SLIVER_TYPE="dockercontainer"
    
    def __init__(self, agg, starting_ipv4_port, host="localhost", ipv6_prefix=None):
        super(DockerContainer, self).__init__(str(uuid.uuid4()), "docker-container")
        self._agg = agg
        self.sliver_type = DockerContainer.DEFAULT_SLIVER_TYPE
        self.users=list()
        self.ssh_port=22
        self.host = host
        self.starting_ipv4_port=starting_ipv4_port
        self.DockerManager = DockerManager()
        self.mac = self.DockerManager.randomMacAddress()
        if ipv6_prefix is not None and len(ipv6_prefix)>0:
            self.ipv6 = self.DockerManager.computeIpV6(ipv6_prefix, self.mac)
        else:
            self.ipv6=None
        self.DockerManager.checkDocker()
        

    def deprovision(self):
        """Deprovision this resource at the resource provider."""
        self.DockerManager.removeContainer(self.id)
        self.users = list()
        self.ssh_port=22
        
    def deallocate(self):
        self.available=True
        self.sliver_type = DockerContainer.DEFAULT_SLIVER_TYPE
        self._agg.deallocate(container=None, resources=[self])

    def getPort(self):
        return self.ssh_port

    def getUsers(self):
        return self.users

    def preprovision(self, user):
        self.users.append(user)
        self.ssh_port = self.DockerManager.reserveNextPort(self.starting_ipv4_port)

    def provision(self, user, key):
        self.DockerManager.startNew(id=self.id, sliver_type=self.sliver_type, ssh_port=self.ssh_port, mac_address=self.mac)
        self.DockerManager.setupContainer(self.id, user, key)

    def updateUser(self, user, keys):
        if user not in self.users:
            self.users.append(user)
        self.DockerManager.setupUser(self.id, user, keys)

    def manifestAuth(self):
        if len(self.getUsers())==0:
            return []
        else:
            ret = []
            for login in self.getUsers():
                auth=etree.Element("login")
                auth.set("authentication","ssh-keys")
                auth.set("hostname", self.host)
                auth.set("port", str(self.getPort()))
                auth.set("username", login)
                ret.append(auth)
                if self.ipv6 is not None:
                    auth=etree.Element("login")
                    auth.set("authentication","ssh-keys")
                    auth.set("hostname", str(self.ipv6))
                    auth.set("port", "22")
                    auth.set("username", login)
                    ret.append(auth)
            return ret

            
    def genAdvertNode(self, _urn_authority, _my_urn):
        r = etree.Element("node")
        resource_id = str(self.id)
        resource_available = str(self.available).lower()
        resource_urn = self.urn(_urn_authority)
        r.set("component_manager_id", _my_urn)
        r.set("component_name", resource_id)
        r.set("component_id", resource_urn)
        r.set("exclusive", "true")
        etree.SubElement(r, "sliver_type").set("name", self.sliver_type)
        etree.SubElement(r, "available").set("now", resource_available)
        return r

    def reset(self):
        super(DockerContainer, self).reset()
        self._agg.deallocate(container=None, resources=[self])

    def checkSshConnection(self):
        try:
            cmd = "ssh -o BatchMode=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@"+self.host+" -p "+self.ssh_port+" 'test'"
            subprocess.check_output(['bash', '-c', cmd]).decode('utf-8').strip()
        except:
            pass
        
