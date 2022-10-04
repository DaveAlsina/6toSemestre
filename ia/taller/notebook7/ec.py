from copy import deepcopy

def obtener_type(objeto):
    c = str(type(objeto))
    return c.split('.')[-1][:-2]

def sust(f, indice, v):
    f1 = deepcopy(f)
    if obtener_type(f) in ['Happens']:
        if v.tipo == 'evento':
            if f1.e_indice == indice:
                f1.e = v
        if v.tipo == 'instante':
            if f1.t_indice == indice:
                f1.t = v
    if obtener_type(f) in ['HoldsAt']:
        if v.tipo == 'fluente':
            if f1.f_indice == indice:
                f1.f = v
        if v.tipo == 'instante':
            if f1.t_indice == indice:
                f1.t = v
    if obtener_type(f) in ['Initiates', 'Terminates']:
        if v.tipo == 'evento':
            if f1.e_indice == indice:
                f1.e = v
        elif v.tipo == 'fluente':
            if f1.f_indice == indice:
                f1.f = v
        elif v.tipo == 'instante':
            if f1.t_indice == indice:
                f1.t = v
    if obtener_type(f) == 'Antes':
        if v.tipo == 'instante':
            if f1.t1_indice == indice:
                f1.t1 = v
            elif f1.t2_indice == indice:
                f1.t2 = v
    if obtener_type(f) == 'Negacion':
        f1.formula = sust(f.formula, indice, v)
    if obtener_type(f) == 'Regla':
        f1.antecedente = sust(f.antecedente, indice, v)
        f1.consecuente = sust(f.consecuente, indice, v)
    if obtener_type(f) == 'Y':
        formulas = [sust(sf, indice, v) for sf in f.formulas]
        f1.formulas = formulas
    if obtener_type(f) == 'Cuantificada':
        f1.formula = sust(f.formula, indice, v)
    return f1



class Tipo:
    def __init__(self, tipo):
        self.tipo = tipo
        
class Constante(Tipo):
    def __init__(self, tipo, nombre='', indice=0):
        super().__init__(tipo)
        self.nombre = nombre
        self.indice = indice
        
    def __str__(self):
        return self.nombre
       
class Fluente(Constante):
    def __init__(self, nombre, atomo, indice=0):
        super().__init__(tipo='fluente', nombre=nombre, indice=indice)
        self.formula = atomo

    def __str__(self):
        return f'f_{self.indice}'

class Evento(Constante):
    def __init__(self, nombre, sujeto='', objeto_d='', objeto_i='', lugar='', indice=0):
        super().__init__(tipo='evento', nombre=nombre, indice=indice)
        if sujeto != '':
            assert(sujeto.tipo in ['agente'])
        self.sujeto = sujeto
        self.objeto_d = objeto_d
        self.objeto_i = objeto_i
        if lugar != '':
            assert(lugar.tipo == 'lugar')
        self.lugar = lugar

    def __str__(self):
        return f'e_{self.indice}'

    def formular(self):
        formulas = [f'{self.nombre}({str(self)})']
        if self.sujeto != '':
            formulas.append(f'SUJETO({str(self)},{self.sujeto.nombre})')
        if self.objeto_d != '':
            formulas.append(f'OBJETO_D({str(self)},{self.objeto_d.nombre})')
        if self.objeto_i != '':
            formulas.append(f'OBJETO_I({str(self)},{self.objeto_i.nombre})')
        if self.lugar != '':
            formulas.append(f'EN({str(self)},{self.lugar.nombre})')
        return formulas
    
class Instante(Constante):
    def __init__(self, valor, indice=0):
        assert(valor == int(valor))
        super().__init__(tipo='instante', nombre=str(valor), indice=indice)
        self.valor = valor
        
    def __str__(self):
        return str(self.valor)
    
class Cuantificador(Tipo):
    def __init__(self, tipo, nombre, indice):
        super().__init__(tipo)
        assert(nombre in ['todo', 'existe'])
        self.nombre = nombre
        self.indice = indice

class Situacion:
    def __init__(self):
        self.eventos = []
        self.fluentes = []
        self.instantes = []
        self.entidades = {}
    
    def nueva_entidad(self, tipo, nombre):
        try:
            n = len(self.entidades[tipo])
            self.entidades[tipo].append(Constante(tipo, nombre, n))
        except:
            n = 0
            self.entidades[tipo] = [Constante(tipo, nombre, n)]
            
    def nuevo_evento(self, nombre, sujeto='', objeto_d='', objeto_i='', lugar=''):
        n = len(self.eventos)
        e = Evento(nombre.upper(), sujeto, objeto_d, objeto_i, lugar, n)
        self.eventos.append(e)
        
    def nuevo_fluente(self, atomo, nombre=''):
        n = len(self.fluentes)
        if nombre == '':
            nombre = atomo.predicado.nombre
        f = Fluente(nombre, atomo)
        self.fluentes.append(f)       

    def nuevo_instante(self, valor=0):
        valores = [i.valor for i in self.instantes]
        if valor not in valores:
            n = len(self.instantes)
            f = Instante(valor, n)
            self.instantes.append(f)
        elif valor == 0:
            n = len(self.instantes)
            f = Instante(n, n)
            self.instantes.append(f)
        
    def __str__(self):
        print('Instantes:', [i.nombre for i in self.instantes])
        cadena = '\nEntidades:\n'
        for tipo in self.entidades:
            cadena += f'\tTipo: {tipo}\n'
            for o in self.entidades[tipo]:
                cadena += '\t' + str(o) + '\n'
            cadena += '\n'
        cadena += 'Eventos:\n'
        for e in self.eventos:
            cadena += f'\t{str(e)}:\n' 
            formulas = e.formular()
            for f in formulas:
                cadena += '\t' + str(f) + '\n'
            cadena += '\n'
        cadena += 'Fluentes:\n'
        for f in self.fluentes:
            cadena += f'\t{str(f)}: {str(f.formula)}\n'
        return cadena
    
class Predicado:
    def __init__(self, nombre, tipos_argumentos):
        self.nombre = nombre
        self.aridad = len(tipos_argumentos)
        self.tipos_argumentos = tipos_argumentos
        
class Formula:
    def __init__(self):
        pass
    
    def __str__(self):
        return str(self)

class Atomo(Formula):
    def __init__(self, nombre, tipos_argumentos, argumentos):
        self.nombre = nombre[0].upper() + nombre[1:].lower()
        self.predicado = Predicado(self.nombre, tipos_argumentos)
        assert(len(tipos_argumentos) == len(argumentos))
        for i, a in enumerate(argumentos):
            assert(a.tipo == tipos_argumentos[i]), f'{a.tipo}; {tipos_argumentos[i]}'
        self.argumentos = argumentos
        
    def __str__(self):
        cadena = self.predicado.nombre + '('
        inicial = True
        for a in self.argumentos:
            if inicial:
                cadena += str(a)
                inicial = False
            else:
                cadena += ',' + str(a)
        return cadena + ')'
    
class Happens(Formula):
    def __init__(self, e_indice, t_indice, e=None, t=None):
        self.e_indice = e_indice
        self.t_indice = t_indice
        self.e = e
        self.t = t
    
    def __str__(self):
        e = f'ev{self.e_indice}' if not self.e else str(self.e)
        t = f'ti{self.t_indice}' if not self.t else str(self.t)
        return f'Happens({e},{t})'
    
class HoldsAt(Formula):
    def __init__(self, f_indice, t_indice, f=None, t=None):
        self.f_indice = f_indice
        self.t_indice = t_indice
        self.f = f
        self.t = t
    
    def __str__(self):
        f = f'flu{self.f_indice}' if not self.f else str(self.f)
        t = f'ti{self.t_indice}' if not self.t else str(self.t)
        return f'HoldsAt({f},{t})'

    
class Initiates(Formula):
    def __init__(self, e_indice, f_indice, t_indice, e=None, f=None, t=None):
        self.e_indice = e_indice
        self.f_indice = f_indice
        self.t_indice = t_indice
        self.e = e
        self.f = f
        self.t = t
    
    def __str__(self):
        e = f'ev{self.e_indice}' if not self.e else str(self.e)
        f = f'flu{self.f_indice}' if not self.f else str(self.f)
        t = f'ti{self.t_indice}' if not self.t else str(self.t)
        return f'Initiates({e},{f},{t})'


class Terminates(Formula):
    def __init__(self, e_indice, f_indice, t_indice, e=None, f=None, t=None):
        self.e_indice = e_indice
        self.f_indice = f_indice
        self.t_indice = t_indice
        self.e = e
        self.f = f
        self.t = t
    
    def __str__(self):
        e = f'ev{self.e_indice}' if not self.e else str(self.e)
        f = f'flu{self.f_indice}' if not self.f else str(self.f)
        t = f'ti{self.t_indice}' if not self.t else str(self.t)
        return f'Terminates({e},{f},{t})'


class Antes(Formula):
    def __init__(self, t1_indice, t2_indice):
        self.t1_indice = t1_indice
        self.t2_indice = t2_indice
        self.t1 = None
        self.t2 = None
        
    def __str__(self):
        t1 = f'ti{self.t1_indice}' if not self.t1 else str(self.t1)
        t2 = f'ti{self.t2_indice}' if not self.t2 else str(self.t2)
        return f'{t1}<{t2}'
    
class Y(Formula):
    def __init__(self, formulas):
        assert(len(formulas) > 1)
        types = ['Formula', 'Atomo', 'Happens', 'HoldsAt', 'Initiates', 'Terminates', 'Antes']
        for f in formulas:
            assert(obtener_type(f) in types)
        self.formulas = formulas
    
    def __str__(self):
        return '(' + '∧'.join([str(f) for f in self.formulas]) + ')'

class O(Formula):
    def __init__(self, formulas):
        assert(len(formulas) > 1)
        types = ['Formula', 'Atomo', 'Happens', 'HoldsAt', 'Initiates', 'Terminates', 'Antes']
        for f in formulas:
            assert(obtener_type(f) in types)
        self.formulas = formulas
    
    def __str__(self):
        return '(' + '∨'.join([str(f) for f in self.formulas]) + ')'
    
class Regla(Formula):
    def __init__(self, antecedente, consecuente):
        self.antecedente = antecedente
        self.consecuente = consecuente
        
    def __str__(self):
        return '(' + f'{str(self.antecedente)}>{str(self.consecuente)}' + ')'
    
class Negacion(Formula):
    def __init__(self, formula):
        self.formula = formula
    
    def __str__(self):
        return '-' + str(self.formula)