from autorecon.plugins import ServiceScan

class NmapNFS(ServiceScan):

  def __init__(self):
    super().__init__()
    self.name = "Nmap NFS"
    self.tags = ['default', 'safe', 'nfs']

  def configure(self):
    self.match_service_name(['^nfs', '^rpcbind'])

  async def run(self, service):
    await service.execute('nmap {nmap_extra} -sV -p {port} --script="banner,(rpcinfo or nfs*) and not (brute or broadcast or dos or external or fuzzer)" -oN "{scandir}/{protocol}_{port}_nfs_nmap.txt" -oX "{scandir}/xml/{protocol}_{port}_nfs_nmap.xml" {address}')

class Showmount(ServiceScan):

  def __init__(self):
    super().__init__()
    self.name = "showmount"
    self.tags = ['default', 'safe', 'nfs']

  def configure(self):
    self.match_service_name(['^nfs', '^rpcbind'])

  async def run(self, service):
    await service.execute('showmount -e {address} 2>&1', outfile='{protocol}_{port}_showmount.txt')

class NmapMountd(ServiceScan):

  def __init__(self):
    super().__init__()
    self.name = "Nmap Mountd"
    self.tags = ['default', 'safe', 'nfs']

  def configure(self):
    self.match_service_name('^mountd')

  async def run(self, service):
    await service.execute('nmap {nmap_extra} -sV -p {port} --script="banner,nfs* and not (brute or broadcast or dos or external or fuzzer)" -oN "{scandir}/{protocol}_{port}_mountd_nmap.txt" -oX "{scandir}/xml/{protocol}_{port}_mountd_nmap.xml" {address}')
