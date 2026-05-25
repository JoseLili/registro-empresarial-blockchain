# Registro Empresarial en Blockchain

Prototipo de smart contract para el registro auditable de empresas
mexicanas sobre Algorand blockchain.

**App ID:** 763199151 — [Ver en Lora Explorer](https://lora.algokit.io/testnet/application/763199151)

## Descripción

Sistema de registro empresarial permisionado que garantiza
trazabilidad e integridad de los datos mediante blockchain.
Cualquier ciudadano puede consultar el estado de una empresa
sin costo ni autenticación. Solo cuentas autorizadas pueden
registrar o modificar empresas.

## Arquitectura

Administrador (Gobierno)
└── Gestiona registradores autorizados comparado a las Notarias que exiten.
Registradores (Notarías)
└── Registran y modifican empresas, uno requiere acudir a una de estas para escriturizar una empresa.
Público
└── Consulta sin costo ni permiso. 

## Campos registrados

|           Campo       |  Tipo  |          Mutabilidad              |
|-----------------------|--------|-----------------------------------|
| Expediente notarial   | String | Inmutable (llave primaria)        |
| Razón social          | String | Mutable                           |
| RFC                   | String | Escritura única                   |
| Tipo de sociedad      | String | Enum (11 tipos válidos)           |
| Estatus               | String | Enum (activa/suspendida/disuelta) |
| Representante legal   | String | Mutable 			     |
| Domicilio fiscal      | String | Mutable			     |
| Reparto de acciones   | String | Mutable			     |
| Número de notaría     | UInt64 | Inmutable			     |
| Permiso uso de nombre | String | Mutable			     |

## Tecnologías

- **Blockchain:** Algorand TestNet
- **Lenguaje:** Algorand Python
- **Compilador:** PuyaPy 5.8.1
- **Herramientas:** AlgoKit, algosdk v2.7.0
- **Estándares:** ARC-4, ARC-28 Events

## Instalación

```bash
# Instalar dependencias
poetry install

# Compilar contrato
algokit project run build

# Desplegar en TestNet
algokit deploy
```

## Scripts de interacción

```bash
# Registrar empresa de prueba
poetry run python prueba_demo.py

# Modificar empresa existente
poetry run python demo_modificacion.py

# Consulta pública sin wallet
poetry run python consulta_publica.py

# Agregar registrador autorizado
poetry run python agregar_pera.py
```

## Contrato desplegado

| Parámetro  |       Valor      |
|------------|------------------|
| App ID     | 763199151        |
| Red        | Algorand TestNet |
| Compilador | PuyaPy 5.8.1     |
| Bloque     | 63678591         |

## Uso de IA

Este proyecto fue desarrollado con asistencia de Claude (Anthropic)
para el diseño del contrato, resolución de errores de compilación
y configuración del entorno. El diseño del modelo de datos,
las decisiones de arquitectura, la lógica de negocio y demostracion en el sitio
https://azure-flamingo-946484.hostingersite.com/?authuser=0  fueron
definidos por el autor basándose en conocimiento real del
proceso de constitución empresarial en México.

## Autor

José Emiliano Lili Beltrán  
Fundamentos de Blockchain — Mayo 2026  
Posgrado en Ciencia e Ingeniería de la Computación, UNAM
