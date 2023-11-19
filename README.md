# TEL141 - INGENIERÍA DE REDES CLOUD - PROYECTO
## OLIMPUS SYSTEMS - ORQUESTADOR OPENSTACK/LINUX
Este proyecto se desarrolla como un prototipo de una capa superior de personalización para gestión de slices, flavors, imágenes y usuarios. En este contexto, las diversas opciones que ofrece este proyecto brindan al usuario la experiencia de crear máquinas virtuales de acuerdo a la topología preferida, elegir sus parámetros y la zona de disponibilidad a implementar.
Se desarrolla bajo el modelo de un controlador central (Headnode) y un cluster de servidores (Workers), los cuales poseen el la distribución Ubuntu de Linux. Asimismo, esta implementación, en este nivel de versión se implementa en CLI mediante el lenguaje de programación Python en su versión 3, y se integra a Openstack Victoria mediante consultas APIs, y una base de datos MySQL.
La arquitectura es la siguiente:
![Arquitectura de la aplicación]("arquitectura.png")
