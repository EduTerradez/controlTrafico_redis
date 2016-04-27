import redis

#conexion con la base de datos Redis

def insertar_tramo(tramo,tren):
    conex = redis.Redis(host='localHost',db=0)
    conex.set(tramo,tren)

def reservar_tramo(tramo, tren , prioridadAbsoluta= False):
    conex = redis.Redis(host='localHost', db=0)
    lista = tramo + "list"
    if prioridadAbsoluta:
        conex.execute_command('LPUSH', lista, tren)
    else:
        conex.execute_command('RPUSH', lista, tren)

def liberar_tramo(tramo):
    conex = redis.Redis(host='localHost', db=0)
    tren = conex.execute_command('LPOP', tramo + "list")
    insertar_tramo(tramo,tren)

def insertar_region(region,tren):
    conex = redis.Redis(host='localHost', db=0)
    conex.execute_command('SADD', region, tren)

def salir_region(region,tren):
    conex = redis.Redis(host='localHost', db=0)
    conex.execute_command('SPOP', region, tren)

def obterner_trenes_regiones(region, *regiones):
    conex = redis.Redis(host='localHost', db=1)
    return conex.execute_command('SUNION', region, *regiones)

def anadir_incidencia_climatologica(incidencia, tiempo ,tramo,*tramos):
    conex = redis.Redis(host='localHost', db=0)
    #metodo anadir mutliple
    #conex.set("Incidencia->" + tramo, incidencia)
    
    conex.execute_command('MSET', "Incidencia->" + tramo, "Incidencia->" + *tramos, incidencia)

    for t in tramos:
        conex.set("Incidencia->" + t, incidencia)
        conex.execute_command('EXPIRE', "Incidencia->" + t, tiempo)

#por python
def mostrar_incidencias(tramo, *tramos):
    conex = redis.Redis(host='localHost', db=0)




if __name__ == "__main__":

    '''pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)

    r.set('lulita', 'cipoton')
    insertarTramo('holi','sipotaso')
    x = r.execute_command('KEYS *')
    for y in x:
        print y
    '''
    '''
    anadir_incidencia_climatologica('MAD<>VAL-tramo1','viento', 10)
    anadir_incidencia_climatologica('MAD<>VL-tramo1', 'viento', 10)
    anadir_incidencia_climatologica('MAD<>TOL-tramo1', 'aguita', 10)
    anadir_incidencia_climatologica('MAD<>Car-tramo1', 'viento', 10)

    comprobar_trenes('MAD')
    '''

    print obterner_trenes_regiones('cipote', 'cipotes')