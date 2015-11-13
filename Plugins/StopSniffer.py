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


import base64
import os
import zope.interface
from .IPlugin import IPlugin

class Handler:
    zope.interface.implements(IPlugin)

    def run(self, thug, log):
        log.info("[Plugins][StopSniffer] Stopping sniffer")
        sniffer = getattr(log, 'sniffer', None)
        if sniffer and not sniffer.poll():
            try:
                log.debug("[Plugins][StopSniffer] Gracefully terminating process")
                sniffer.terminate()
                log.debug("[Plugins][StopSniffer] Process terminated gracefully")
            except:
                try:
                    if not sniffer.poll():
                        log.debug("[Plugins][StopSniffer] Killing sniffer")
                        sniffer.kill()
                except OSError as e:
                    log.debug("[Plugins][StopSniffer] Error killing sniffer: %s. Continue", e)
                    pass
                except Exception as e:
                    log.exception("[Plugins][StopSniffer] Unable to stop the sniffer with pid %d: %s",
                                    sniffer.pid, e)

        mongoLogger = log.ThugLogging.modules.get('mongodb', None)
        if mongoLogger and mongoLogger.enabled:
            db = mongoLogger.urls.database
            if os.path.isfile(log.sniffer_filename):
                with open(log.sniffer_filename, 'rb') as i:
                    content = i.read()

                os.unlink(log.sniffer_filename)

                content_id = mongoLogger.fs.put(base64.b64encode(content)) if content else None
                pcap = {
                    'analysis_id'   : mongoLogger.analysis_id,
                    'content_id'    : content_id,
                    'mime-type'     : 'application/vnd.tcpdump.pcap',
                }
                db.pcaps.insert(pcap)

                log.info("[Plugins][StopSniffer] PCAP successfully added to Mongo")
