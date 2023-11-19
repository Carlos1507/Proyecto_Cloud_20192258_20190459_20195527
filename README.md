# TEL141 - INGENIERÍA DE REDES CLOUD - PROYECTO
## OLIMPUS SYSTEMS - ORQUESTADOR OPENSTACK/LINUX
Este proyecto se desarrolla como un prototipo de una capa superior de personalización para gestión de slices, flavors, imágenes y usuarios. En este contexto, las diversas opciones que ofrece este proyecto brindan al usuario la experiencia de crear máquinas virtuales de acuerdo a la topología preferida, elegir sus parámetros y la zona de disponibilidad a implementar.
Se desarrolla bajo el modelo de un controlador central (Headnode) y un cluster de servidores (Workers), los cuales poseen el la distribución Ubuntu de Linux. Asimismo, esta implementación, en este nivel de versión se implementa en CLI mediante el lenguaje de programación Python en su versión 3, y se integra a Openstack Victoria mediante consultas APIs, y una base de datos MySQL.
### La arquitectura es la siguiente:
![Arquitectura de la aplicación](arquitectura.png)
### Dependencias necesarias:
Los requerimientos en dependencias y versiones de python para este proyecto se encuentran en el archivo a continuación, asimismo, se sugiere instalarlas en un entorno virtual.
[Requerimientos](requirements.txt)
## Estructura del proyecto e instalación
El proyecto consta de dos partes, cliente y servidor, ambos en python 3.
Asimismo, en cuanto a equipos de cómputo, tenemos: computadora local, controlador (Headnode), gateway y cluster de servidores (Worker 1, 2 y 3)
1. En el headnode y workers se instala Openstack y se configuran e instalan las herramientas de **Chrony**, **MariaDB**, **RabbitMQ**, **Memcached**, **Etcd**; y los servicios de **Openstack**: *Keystone*,  *Glance*, *Placement*, *Nova*, *Neutron*, *Horizon*
2. Dar salida a los servicios de openstack con iptables en el gateway: `iptables -t nat -A PREROUTING -p tcp -m tcp --dport XXXX -j DNAT --to-destination 10.0.10.2:XXXX`, donde *XXXX* es el puerto al que se le desea dar salida
3. Dado que el servidor se usará en el puerto 8000, dar salida también a este puerto en el gateway: `iptables -t nat -A PREROUTING -p tcp -m tcp --dport 8000 -j DNAT --to-destination 10.0.10.2:8000`
4. Instalación de docker:
```
sudo apt update
```