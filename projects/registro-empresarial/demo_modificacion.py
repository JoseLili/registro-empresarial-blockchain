import algokit_utils
from dotenv import load_dotenv
from smart_contracts.artifacts.registro_empresarial.registro_empresarial_client import (
    RegistroEmpresarialFactory,
    ActualizarDomicilioArgs,
    CambiarEstatusArgs,
)

load_dotenv()

algorand = algokit_utils.AlgorandClient.from_environment()
deployer = algorand.account.from_environment("DEPLOYER")

factory = algorand.client.get_typed_app_factory(
    RegistroEmpresarialFactory, default_sender=deployer.address
)

app_client = factory.get_app_client_by_id(app_id=763199151)

# Modificación 1: actualizar domicilio fiscal
print("Actualizando domicilio fiscal...")
result1 = app_client.send.actualizar_domicilio(
    args=ActualizarDomicilioArgs(
        expediente="NOTARIA-15-2026-024",
        valor="Insurgentes Sur 1602, Col. Crédito Constructor, CDMX",
    )
)
print(f"✓ Domicilio actualizado")
print(f"TX ID: {result1.tx_ids[0]}")
print(f"Lora: https://lora.algokit.io/testnet/transaction/{result1.tx_ids[0]}")

# Modificación 2: cambiar estatus a suspendida
print()
print("Cambiando estatus a suspendida...")
result2 = app_client.send.cambiar_estatus(
    args=CambiarEstatusArgs(
        expediente="NOTARIA-15-2026-042",
        nuevo_estatus="suspendida",
    )
)
print(f"✓ Estatus modificado")
print(f"TX ID: {result2.tx_ids[0]}")
print(f"Lora: https://lora.algokit.io/testnet/transaction/{result2.tx_ids[0]}")

print()
print("Busca en el portal: NOTARIA-15-2025-042")
