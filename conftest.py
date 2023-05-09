"""
Se crea este archivo que almacena accesorios y/o fixtures que se usaran en algunas pruebas o en algun
test global
"""

import pytest
from ddf import G, N, F
from users.models import User



@pytest.fixture  # Crea instancias automaticas segun el modelo que se le pase
def user_creation():
    return UserFactory() #Se debe instanciar con los dos parentesis
