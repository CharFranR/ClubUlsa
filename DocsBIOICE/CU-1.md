@startuml
title Diagrama de casos de uso - BioICE

left to right direction


actor Colaborador
actor Visitante
actor Administrador

rectangle "BioICE" {
    usecase "Notificar" as UC10
    usecase "Consultar historial de consumo de biogas" as UC9
    usecase "Consultar historial de llenados" as UC8
    usecase "Registrar llenado de biodigestor" as UC7
    usecase "Consultar historial de calibraciones" as UC6
    usecase "Registrar calibración" as UC5
    usecase "Generar reportes por evento" as UC4
    usecase "Generar reportes por fechas" as UC3
    usecase "Consultar datos de sensores" as UC2
    usecase "Iniciar Sesión" as UC1
}


Administrador --> UC1
Administrador --> UC2
Administrador --> UC3
Administrador --> UC4
Administrador --> UC5
Administrador --> UC6
Administrador --> UC7
Administrador --> UC8
Administrador --> UC9
UC10 --> Administrador


UC1 --> Colaborador
UC2 --> Colaborador
UC4 --> Colaborador
UC7 --> Colaborador
UC8 --> Colaborador

UC1 --> Visitante
UC2 --> Visitante
UC3 --> Visitante
@enduml