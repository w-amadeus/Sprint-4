import argparse
import pandas as pd
from datetime import datetime

def generar_csv(df, dni):
    fecha = datetime.now().timestamp()
    return df.to_csv('{dni}_{fecha}'.format(dni=dni, fecha=fecha), index=False, encoding='utf-8')

def filtrar_cheques(df, dni, tipo, estado, fecha):
    if estado:
        estado = [estado]
    if fecha:
        min_fecha = datetime.fromisoformat(fecha[:10]).timestamp()
        max_fecha = datetime.fromisoformat(fecha[11:]).timestamp()

    return df.loc[(df['DNI'] == dni) & (df['Tipo'] == tipo) &
                  (df['Estado'].isin(estado if estado else ['pendiente', 'aprobado', 'rechazado'])) &
                  (df['FechaOrigen'] >= min_fecha if fecha else True) & (df['FechaOrigen'] < max_fecha if fecha else True)]

def main(archivo: str, dni: str, salida: str, tipo_cheque: str, estado_cheque: str, rango_fecha: str):
    try:
        df = pd.read_csv(archivo)
        if (df.loc[df['DNI'] == dni]).NroCheque.is_unique:
            if salida == 'pantalla':
                print(filtrar_cheques(df, dni, tipo_cheque, estado_cheque, rango_fecha))
            elif salida == 'csv':
                datos = (filtrar_cheques(df, dni, tipo_cheque, estado_cheque, rango_fecha))[['FechaOrigen', 'FechaPago', 'Valor', 'NumeroCuentaOrigen']]
                generar_csv(datos, dni)
            else:
                print('Error: no existe la opcion')
        else:
            print('Error: número de cheque repetido')
    except FileNotFoundError:
        print('El archivo {archivo} no existe'.format(archivo=archivo))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validador de cheques')
    parser.add_argument('-archivo', required=True, help='Nombre del archivo csv')
    parser.add_argument('-dni', required=True, help="DNI a consultar")
    parser.add_argument('-salida', required=True, help="Salida: [PANTALLA, CSV")
    parser.add_argument('-tipo_cheque', required=True, help='Tipo de cheque: [ EMITIDO, DEPOSITADO ]')
    parser.add_argument('-estado_cheque', required=False, help='(Opcional) Estado del cheque: [PENDIENTE, APROBADO, RECHAZADO]')
    parser.add_argument('-rango_fecha', required=False, help='(Opcional) Rango de fecha: xx-xx-xxxx:yy-yy-yyyy')
    args = parser.parse_args()

    main(args.archivo, args.dni, args.salida, args.tipo_cheque, args.estado_cheque, args.rango_fecha)
