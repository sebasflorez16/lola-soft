
#Se creo este archivo para generalizar las vistas genericas. Asi pasamos un solo queryset para todas las vistas
#hasta el momento. No hacemos un queryset por cada vista.
#El get_serializer() toma lo que le pasamos en el serializer_class "El serializador y dentro del mismo ya esta el modelo"
# en las vistas solo pasamos el nombre del serializador. 

from rest_framework import generics

class GeneralListAPIView(generics.ListAPIView):
    serializer_class = None


    def get_queryset(self):
        model = self.get_serializer().Meta.model #La ruta del modelo dentro del serializador
        return model.objects.filter(state = True)