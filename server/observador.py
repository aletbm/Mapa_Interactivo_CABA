from modelo import log


class Tema: 

    observadores = []

    def agregar(self, obj):
        self.observadores.append(obj)

    def notificar(self):
        for observador in self.observadores:
            observador.update()


class TemaConcreto(Tema):
    def __init__(self):
        """
        

        Returns
        -------
        None.

        """
        self.lat = None
        self.lng = None
        self.dir = None
        self.bus = None

    def set_estado(self, latitud, longitud, direccion, busqueda):
        """
        

        """
        self.lng = longitud
        self.lat = latitud
        self.dir = direccion
        self.bus = busqueda
        self.notificar()

    def get_estado(self):
     
        return self.lat, self.lng, self.dir, self.bus


class Observador:
    def update(self):
        """
        actualiza el evento observado
        """
        raise NotImplementedError("Delegación de actualización")


class ConcreteObserverA(Observador):
    def __init__(self, obj):
        """


        """
        self.observador_a = obj
        self.observador_a.agregar(self)

    def update(self):
        """
    
        None.

        """
        self.lat, self.lng, self.dir, self.bus = self.observador_a.get_estado()
        milog = log()
        milog.direccion = self.dir
        milog.latitud = self.lat
        milog.longitud = self.lng
        milog.busqueda = self.bus
        milog.save()
