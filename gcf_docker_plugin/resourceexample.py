from __future__ import absolute_import
from gcf.geni.am.resource import Resource

from lxml import etree

class ResourceExample(ExtendedResource):

    SLIVER_TYPE = "myressourceexample"
    
    def __init__(self, rid, rtype, host="MYDOMAIN.com"):
        super(ExtendedResource, self).__init__(rid, rtype)
        self.users=dict()
        self.ssh_port=22
        self.error = ""
        self.host = host

    def genAdvertNode(self, _urn_authority, _my_urn):
        r = super(ResourceExample, self).genAdvertNode(_urn_authority, _my_urn)
        etree.SubElement(r, "sliver_type").set("name", SLIVER_TYPE)
        return r

    def getResource(self, component_id=None):
        if component_id is not None:
            if component_id != self.id:
                return None
        return self

    def deallocate(self):
        self.available = True
        self.users = dict()

    def getPort(self):
        return self.ssh_port

    def getUsers(self):
        return self.users.keys()

    def preprovision(self, user, ssh_keys):
        if user not in self.users.keys():
            self.users[user]=ssh_keys

    def provision(self, user, keys):
        #Assuming the AM have SSH root access to the node and the node is up
        #Setup users
        for username in self.users.keys():
            ssh = "ssh root@"+self.host+" -p "+self.ssh_port+" "
            cmd_create_user = ssh+"'grep \'^"+username+":\' /etc/passwd ; if [ $? -ne 0 ] ; then useradd -m -d /home/"+username+" "+ username+" && mkdir -p /home/"+username+"/.ssh ; fi'"
            out = subprocess.check_output(['bash', '-c', cmd_create_user])
            cmd_add_key = ssh+"\"echo '' > /home/"+username+"/.ssh/authorized_keys\""
            out = subprocess.check_output(['bash', '-c', cmd_add_key])
            for key in ssh_keys:
                cmd_add_key = ssh+"\"echo '"+key+"' >> /home/"+username+"/.ssh/authorized_keys\""
                out = subprocess.check_output(['bash', '-c', cmd_add_key])
            cmd_set_rights = ssh+"'chown -R "+username+": /home/"+username+" && chmod 700 /home/"+username+"/.ssh && chmod 644 /home/"+username+"/.ssh/authorized_keys'"
            out = subprocess.check_output(['bash', '-c', cmd_set_rights])
            

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
            return ret

    #A blocking (while ...) method. Return True when the resource is up and ready, or False if you set a timeout
    def checkSshConnection(self):
        try:
            ssh = "ssh root@"+self.host+" -p "+self.ssh_port
            subprocess.check_output(['bash', '-c', ssh])
            return True
        except subprocess.CalledProcessError as e:
            return False
        pass

    #Install the target url to the install_path (decompressed)
    def installCommand(self, url, install_path):
        pass

    #Execute a command with the given shell on the resource
    def executeCommand(self, shell, cmd):
        pass
