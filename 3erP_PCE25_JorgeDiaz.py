import requests
import json
import subprocess
import argparse
import sys
import logging
#3er Parcial PC

logging.basicConfig(filename="Registros_3erParcial.log", level=logging.INFO)

def obtener_ips():
    print("Obteniendo IP's.....")
    try:
        powershell="powershell -Executionpolicy Bypass -File IPsActivas.ps1"
        ejecucion=subprocess.run(powershell, capture_output=True, text=True)
        salida=ejecucion.stdout
        print("Generando lista de IP's.......")
        ips_list=salida.split()
        print(ips_list)
        logging.info(f"La lista de ip's obtenidas fueron: {ips_list}")
        return ips_list
    except Exception as e:
        print(f"Se a producido un error al obtener las IP's: {e}")
        logging.error("Se a producido un error al obtener las IP's:" + str(e))
        
    
def checarIP(ip):
    #Código para consultar la API de Abuse IP BD
    try:
        url = 'https://api.abuseipdb.com/api/v2/check'
        querystring = {
            'ipAddress': ip,
            'maxAgeInDays': '90'
        }
        headers = {
            'Accept': 'application/json',
            'Key': '1351d01769557d0f4f0e59265e9b3b401a122bac5c33b6fcbf15ac6f7a1d7e55b5d53ff5f43a287c'
        }
        response = requests.request(method='GET', url=url,
                                    headers=headers, params=querystring)
        if response.status_code==200:
            print("Se a conectado a la API con exito :D")
            data=response.json()
            if data['data']['abuseConfidenceScore']>50:
                print("Ip sospechosa")
                print(data['data']['domain'])
                logging.info("Escaneo completado, ip sospechosa")
            else:
                print("IP no sospechosa")
                print(data['data']['domain'])
                logging.info("Escaneo completado, ip no sospechosa")
                
        # Formatted output
        decodedResponse = json.loads(response.text)
        apiresp=json.dumps(decodedResponse, sort_keys=True, indent=4)
        logging.info(f"la información de la ip analizada es:\n{apiresp}")
        return apiresp
    except Exception as e:
        print(f"Ocurrio un error al querer conectar la API: {e}")
        logging.error("Ocurrio un error en la conexion de la API: "+str(e))
    

def main():
    #todo el codigo del proyecto estará aquí
    print("Hola este es mi 3er Parcial de programación para ciberseguridad!")
    print("Mi nombre es:\nJorge Alejandro Diaz Garcia")
    print("Mi matricula es:\n2086071")
    parser=argparse.ArgumentParser()
    parser.add_argument("-ipscan", dest="IPscan", nargs='+', help="Ingrese la dirección(es) IPV4 a analizar")
    args=parser.parse_args()
    if args.IPscan==["0"]:   
        ip_list=obtener_ips()
        for ip in ip_list:
            sys.stdout.write(str(checarIP(ip)))
            if ip==ip_list[2]:
                print("Se han analizado 3 direcciones IP")
                break
    else:
        print(args.IPscan)
        ip_list=args.IPscan
        for i,ip in enumerate(ip_list):
            print(f"Analizando la ip: {ip}")
            sys.stdout.write(str(checarIP(ip)))
        
if __name__ == "__main__":
    main()
