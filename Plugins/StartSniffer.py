#!/usr/bin/env python
#
# StartSniffer.py
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA  02111-1307  USA


import subprocess
import tempfile
import zope.interface
from .IPlugin import IPlugin

class Handler:
    zope.interface.implements(IPlugin)

    def run(self, thug, log):
        log.info("[Plugins][StartSniffer] Starting sniffer")
        _o, log.sniffer_filename = tempfile.mkstemp(suffix='.pcap')
        try:
            log.sniffer = subprocess.Popen([
                '/usr/sbin/tcpdump',
                '-i', 'any',
                '-w', log.sniffer_filename
            ])
        except Exception as e:
            log.exception("Unable to start sniffer: {}".format(e))
        else:
            log.info("[Plugins][StartSniffer] Sniffer running on pid {}".format(log.sniffer.pid))
