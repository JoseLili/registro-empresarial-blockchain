import algokit_utils
from dotenv import load_dotenv
from smart_contracts.artifacts.registro_empresarial.registro_empresarial_client import (
    RegistroEmpresarialFactory,
    RegistrarEmpresaArgs,
    AgregarRegistradorArgs,
)

load_dotenv()

algorand = algokit_utils.AlgorandClient.from_environment()
deployer = algorand.account.from_environment("DEPLOYER")

APP_ID = 763199151

factory = algorand.client.get_typed_app_factory(
    RegistroEmpresarialFactory, default_sender=deployer.address
)

app_client = factory.get_app_client_by_id(app_id=APP_ID)

# Paso 1: Agregar al deployer como registrador
print("Agregando registrador...")
result = app_client.send.agregar_registrador(
    args=AgregarRegistradorArgs(cuenta=deployer.address)
)
print(f"Registrador agregado. TX: {result.tx_ids[0]}")

# Paso 2: Registrar una empresa de prueba
print("Registrando empresa...")
result = app_client.send.registrar_empresa(
    args=RegistrarEmpresaArgs(
        expediente="NOTARIA-42-2024-001",
        razon_social="Tecnologías Blockchain México",
        tipo_sociedad="S.A.",
        representante_legal="Juan Pérez García",
        domicilio_fiscal="Av. Reforma 123, CDMX",
        reparto_acciones="Juan Pérez 50%, María López 50%",
        numero_notaria=42,
        permiso_uso_nombre="PERMISO-SE-2024-001",
    )
)
print(f"Empresa registrada!")
print(f"TX: {result.tx_ids[0]}")
print(f"Lora: https://lora.algokit.io/testnet/transaction/{result.tx_ids[0]}")
