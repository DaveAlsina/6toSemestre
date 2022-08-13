from time import time
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols

def obtiene_tiempos(fun, args, num_it=10):
    tiempos_fun = []
    for i in range(num_it):
        arranca = time()
        x = fun(*args)
        para = time()
        tiempos_fun.append(para - arranca)
    return tiempos_fun

def compara_funciones(funs = None, arg = None, nombres = None, N=10):
    nms = []
    ts = []
    for i, fun in enumerate(funs):
        nms += [nombres[i] for x in range(N)]
        ts += obtiene_tiempos(fun, [arg], N)
    data = pd.DataFrame({'Función':nms, 'Tiempo':ts})
    return data

def compara_funciones_sobreargumentos(funs, args, nombres, N=10):
    data_list = []

    #progress bar that shows the progress of the function, 
    #in only one line with  \r to overwrite the previous line
        for i, fun in enumerate(funs):
            data = compara_funciones(fun, args[i], nombres[i], N)
            data_list.append(data)



    with tqdm(total=len(funs), desc='\rComparando funciones',) as pbar:

        for i, arg in enumerate(args):
            nms = []
            argumentos = []
            ts = []

        with tqdm(total=len(funs), desc='\rComparando funciones',) as pbar2:

            for i, fun in tqdm(enumerate(funs), desc='\rProbando en funciones escogidas', total=len(funs)):
                nms += [nombres[i] for x in range(N)]
                argumentos += [i for x in range(N)]
                ts += obtiene_tiempos(fun, [arg], N)
                pbar2.update(1)

        data_list.append(pd.DataFrame({'Función':nms, 'Num_argumento':argumentos, 'Tiempo':ts}))
        pbar.update(1)

    return pd.concat(data_list)



