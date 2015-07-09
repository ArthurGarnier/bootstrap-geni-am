#----------------------------------------------------------------------
# Copyright (c) 2015 Inria by David Margery
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
"""
An empty aggregate manager delegate 
"""

import gcf.geni.am.am3 as am3

class MyTestbedDelegate(am3.ReferenceAggregateManager):
    CONFIG_LOCATIONS=["/etc/geni-tools-delegate/testbed.ini", 
                     "testbed.ini"]

    def __init__(self, root_cert, urn_authority, url, **kwargs):
        super(MyTestbedDelegate,self).__init__(root_cert,urn_authority,url,**kwargs)

        self.logger=logging.getLogger('geni-delegate')

        self.aggregate_manager_id=self.getAggregateManagerId(kwargs['certfile'])
        self._my_urn=self.aggregate_manager_id

        urn_components=self.aggregate_manager_id.split('+')
        self.urn_authority_prefix="%s+%s"%(urn_components[0],urn_components[1])

        self.parser=SafeConfigParser()
        found_configs=self.parser.read(self.CONFIG_LOCATIONS)
        if len(found_configs) < 1:
            self.logger.warn('Did not find testbed configuration from %s' % self.CONFIG_LOCATIONS)
        else:
            self.logger.info("Read configuration from the following sources: %s" % found_configs)
        self.logger.debug("Starting testbed aggregate manager delegate for urn %s at url %s"% (urn_authority,url))


    def GetVersion(self, options):
        return super(MyTestbedDelegate, self).GetVersion(options)


    def ListResources(self, credentials, options):
        privileges = ()
        self.getVerifiedCredentials(None,
                                    credentials, 
                                    options,
                                    privileges)
        # If we get here, the credentials give the caller
        # all needed privileges to act on the given target.



    def Allocate(self, slice_urn, credentials, rspec, options):
        privileges = (am3.ALLOCATE_PRIV,)

        creds=self.getVerifiedCredentials(slice_urn, 
                                          credentials, 
                                          options, 
                                          privileges)
        # If we get here, the credentials give the caller
        # all needed privileges to act on the given target.


    def Provision(self, urns, credentials, options):
        privileges = (am3.PROVISION_PRIV,)
        creds = self.getverifiedcredentials(the_slice.urn, 
                                            credentials, 
                                            options, 
                                            privileges)


    def PerformOperationalAction(self, urns, credentials, action, options):
        privileges = (am3.PERFORM_ACTION_PRIV,)
        creds = self.getVerifiedCredentials(the_slice.urn, 
                                            credentials, 
                                            options, 
                                            privileges)


    def Status(self, urns, credentials, options):
        privileges = (am3.SLIVERSTATUSPRIV,)
        creds=self.getVerifiedCredentials(the_slice.urn, 
                                          credentials, 
                                          options, 
                                          privileges)



    def Describe(self, urns, credentials, options):
        privileges = (am3.SLIVERSTATUSPRIV,)
        creds= self.getVerifiedCredentials(the_slice.urn, 
                                           credentials, 
                                           options, 
                                           privileges)


    def Renew(self, urns, credentials, expiration_time, options):
        privileges = (am3.RENEWSLIVERPRIV,)
        creds = self.getVerifiedCredentials(the_slice.urn, 
                                            credentials, 
                                            options, 
                                            privileges)


    def Shutdown(self, slice_urn, credentials, options):
        privileges = (am3.SHUTDOWNSLIVERPRIV,)
        self.getVerifiedCredentials(slice_urn, 
                                    credentials, 
                                    options, 
                                    privileges)
        return self.successResult(True)
