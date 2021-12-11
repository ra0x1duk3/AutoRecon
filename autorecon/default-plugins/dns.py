from autorecon.plugins import ServiceScan

class NmapDNS(ServiceScan):

  def __init__(self):
    super().__init__()
    self.name = 'Nmap DNS'
    self.tags = ['default', 'safe', 'dns']

  def configure(self):
    self.match_service_name('^domain')

  async def run(self, service):
    await service.execute('nmap {nmap_extra} -sV -p {port} --script="banner,(dns* or ssl*) and not (brute or broadcast or dos or external or fuzzer)" -oN "{scandir}/{protocol}_{port}_dns_nmap.txt" -oX "{scandir}/xml/{protocol}_{port}_dns_nmap.xml" {address}')

class DNSZoneTransfer(ServiceScan):

  def __init__(self):
    super().__init__()
    self.name = 'DNS Zone Transfer'
    self.tags = ['default', 'safe', 'dns']

  def configure(self):
    self.match_service_name('^domain')

  async def run(self, service):
    if self.get_global('domain'):
      await service.execute('dig AXFR -p {port} @{address} ' + self.get_global('domain'), outfile='{protocol}_{port}_dns_zone-transfer-domain.txt')
    if service.target.type == 'hostname':
      await service.execute('dig AXFR -p {port} @{address} {address}', outfile='{protocol}_{port}_dns_zone-transfer-hostname.txt')
    await service.execute('dig AXFR -p {port} @{address}', outfile='{protocol}_{port}_dns_zone-transfer.txt')

class DNSReverseLookup(ServiceScan):

  def __init__(self):
    super().__init__()
    self.name = 'DNS Reverse Lookup'
    self.tags = ['default', 'safe', 'dns']

  def configure(self):
    self.match_service_name('^domain')

  async def run(self, service):
    await service.execute('dig -p {port} -x {address} @{address}', outfile='{protocol}_{port}_dns_reverse-lookup.txt')

class NmapMulticastDNS(ServiceScan):

  def __init__(self):
    super().__init__()
    self.name = 'Nmap Multicast DNS'
    self.tags = ['default', 'safe', 'dns']

  def configure(self):
    self.match_service_name(['^mdns', '^zeroconf'])

  async def run(self, service):
    await service.execute('nmap {nmap_extra} -sV -p {port} --script="banner,(dns* or ssl*) and not (brute or broadcast or dos or external or fuzzer)" -oN "{scandir}/{protocol}_{port}_multicastdns_nmap.txt" -oX "{scandir}/xml/{protocol}_{port}_multicastdns_nmap.xml" {address}')
