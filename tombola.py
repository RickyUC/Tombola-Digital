__author__ = 'Ricardo Del Río'

'''
¡ADVERTENCIA!

El siguiente programa no tiene implementado manejo de excepciones,
de modo que si se ingresan mal los datos o se entrega una base de datos vacía el programa se caerá.

'''

from random import randint, shuffle
from datetime import datetime as dt
from os import system as s

class BoletoRifa:
    '''
    Esta clase representa cada uno de los boleltos que fueron vendidos en la rifa y los almacena en una lista.
    '''
    boletos = []
    def __init__(self, nombre, direccion, email, telefono, cod_envio, fecha, ID, enviado):
        self.id = ID
        self.nombre = nombre
        self.direccion = direccion
        self.email = email
        self.telefono = telefono
        self.cod_envio = cod_envio
        if enviado:
            self.correo_enviado = True
        else:
            self.correo_enviado = False
        self.fecha_compra = fecha
        BoletoRifa.boletos.append(self)


class Tombola:
    '''
    Esta clase es la representación digital de una tómbola para sorteos.
    '''
    def __init__(self):
        self.seleccionados = []
        self.premiados = []

    def cargar_base_datos(self, path):
        '''
        Recupera los boletos de la base de datos indicada en el path.
        :param path:
        '''
        with open(path, 'r', encoding='utf-8') as archivo:
            boletos = archivo.readlines()
            # Eliminación carácteres codificación:
            boletos = [boletos.pop(0).replace('\ufeff','')] + boletos
            # Almacenamiento de los datos:
            for boleto in boletos:
                BoletoRifa(*boleto.strip().split(';'))

    def revolver_y_seleccionar(self):
        '''
        Simulando la utilización de una tombola real, este método mezcla los boletos y luego selecciona uno al azar.
        Este es guardado en la lista 'self.seleccionados'
        '''
        shuffle(BoletoRifa.boletos)
        num = randint(0,len(BoletoRifa.boletos)-1)
        seleccionado = BoletoRifa.boletos.pop(num)
        self.seleccionados.append(seleccionado)


    def def_premiados_y_mostrar(self):
        '''
        En base al orden en que los boletos fueron seleccionados, se define que boletos son los premiados (pares) y
        cuales son 'al agua' (impares).
        Se imprimen en la pantalla los resultados.
        Para el correcto funcionamiento de este método es necesario que la funcion 'revolver_y_seleccionar()' haya sido
        ejecutada el doble de veces que la cantidad de premios que se sortean.
        '''
        contador = 1
        n_premio = 1
        for seleccionado in self.seleccionados:
            if contador%2 == 0:
                print('\t{}) PREMIO {}:   {} {}'.format(contador,n_premio, seleccionado.id, seleccionado.nombre))
                self.premiados.append(seleccionado)
                n_premio += 1
            else:
                print('\t{}) AL AGUA:    {} {}'.format(contador,seleccionado.id, seleccionado.nombre))
            contador += 1

    def calcular_probs(self,c_premios):
        '''
        Calcula la probabilidad con la formula 'casos posibles' divididos por 'casos totales'.
        El resultado se entrega en porcentaje.
        :param c_premios:
        '''
        return (c_premios/len(BoletoRifa.boletos))*100


if __name__ == '__main__':
    '''
    Se genera un ciclo con una cantidad de vueltas que duplica la cantidad de premios que se entregarán.
    Se muestran todos los datos de la rifa, el sorteo y elementos de formato.
    '''
    t = Tombola()
    texto = '''
        {0}
        |                                             |
        |  BIENVENIDO AL SOFTWARE DE TOMBOLA VIRTUAL  |
        |  Ingresa los Siguientes Datos:              |
        |                                             |
        {0}
        '''.format('-' * 46)
    print(texto+'\n')
    base_datos = input('>>> Ingresa el nombre del archivo con la base de datos: ')
    c_premios = int(input('>>> Cantidad de premios en sorteo: '))
    t.cargar_base_datos(base_datos)

    s('cls')

    texto = '''
            {0}
            |                                             |
            |         RESULTADOS TOMBOLA DIGITAL          |
            |                                             |
            {0}
            '''.format('-' * 46)
    print(texto + '\n')
    print('\tFecha/Hora sorteo:                {}'.format(dt.now()))
    print('\tCantidad de premios:              {}'.format(c_premios))
    print('\tProbabilidad de ganar un premio:  {}%\n '.format(t.calcular_probs(c_premios)))
    print('\tSORTEO:\n')
    for i in range(c_premios*2):
        t.revolver_y_seleccionar()
    t.def_premiados_y_mostrar()
    print('\n\n\tFELICIDADES!!\n\n')
