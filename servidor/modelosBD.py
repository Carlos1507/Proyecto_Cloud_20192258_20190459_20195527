class FlavorBD:
    def __init__(self, idflavors, ram_mb, disk_gb, cpus, nombre, idflavorglance):
        self.nombre = nombre
        self.ram = ram_mb
        self.cpu = cpus
        self.disk = disk_gb
        self.idflavors = idflavors
        self.idflavorglance = idflavorglance
    def to_dict(self):
        return {
            'idflavors': self.idflavors,
            'ram_mb': self.ram,
            'disk_gb': self.disk, 
            'cpus': self.cpu,
            'nombre': self.nombre,
            'idflavorglace': self.idflavorglance
        }
class RecursosBD:
    def __init__(self, idRecursos, worker, memoriaUso, memoriaTotal, discoAsignado, discoTotal, cpusAsignado, cpuTotal):
        self.idRecursos = idRecursos
        self.worker = worker
        self.memoriaUso = memoriaUso
        self.memoriaTotal = memoriaTotal
        self.discoAsignado = discoAsignado
        self.discoTotal = discoTotal
        self.cpusAsignado = cpusAsignado
        self.cpuTotal = cpuTotal
    def to_dict(self):
        return {
            'idRecursos': self.idRecursos,
            'worker': self.worker,
            'memoriaUso': self.memoriaUso, 
            'memoriaTotal': self.memoriaTotal,
            'discoAsignado': self.discoAsignado,
            'discoTotal': self.discoTotal,
            'cpusAsignado': self.cpusAsignado,
            'cpuTotal': self.cpuTotal
        }
class SliceBD:
    def __init__(self, idSlice, nombre, idOpenstackproject, idLinuxproject, usuario_idUsuario, fecha, sliceJSON):
        self.idSlice = idSlice
        self.nombre = nombre
        self.idOpenstackproject = idOpenstackproject
        self.idLinuxproject = idLinuxproject
        self.usuario_idUsuario = usuario_idUsuario
        self.fecha = fecha
        self.sliceJSON = sliceJSON
    def to_dict(self):
        return {
            'idSlice': self.idSlice,
            'nombre': self.nombre,
            'idOpenstackproject': self.idOpenstackproject, 
            'idLinuxproject': self.idLinuxproject,
            'usuario_idUsuario': self.usuario_idUsuario,
            'fecha': self.fecha,
            'sliceJSON': self.sliceJSON
        }
class ImagenBD:
    def __init__(self, idImagenes, nombre, filename, idglance):
        self.idImagenes = idImagenes
        self.nombre = nombre
        self.filename = filename
        self.idglance = idglance
    def to_dict(self):
        return {
            'idImagenes': self.idImagenes,
            'nombre': self.nombre,
            'filename': self.filename, 
            'idglance': self.idglance
        }

