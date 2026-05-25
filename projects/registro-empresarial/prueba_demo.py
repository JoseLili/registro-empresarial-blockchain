import algokit_utils
from dotenv import load_dotenv
from smart_contracts.artifacts.registro_empresarial.registro_empresarial_client import (
    RegistroEmpresarialFactory,
    RegistrarEmpresaArgs,
)

load_dotenv()

algorand = algokit_utils.AlgorandClient.from_environment()
deployer = algorand.account.from_environment("DEPLOYER")

factory = algorand.client.get_typed_app_factory(
    RegistroEmpresarialFactory, default_sender=deployer.address
)

app_client = factory.get_app_client_by_id(app_id=763199151)

print("Registrando empresa en la blockchain...")
print("Expediente: NOTARIA-15-2025-042")
print("Empresa: Consultoría Digital Beltrán S.A.")
print()

result = app_client.send.registrar_empresa(
    args=RegistrarEmpresaArgs(
        expediente="NOTARIA-15-2026-024",
        razon_social="Consultoría Digital Lili  S.A.",
        tipo_sociedad="S.A.",
        representante_legal="José Emiliano Lili Beltrán",
        domicilio_fiscal="Av. Universidad 3000, CU, CDMX",
        reparto_acciones="José Emiliano Lili Beltrán 100%",
        numero_notaria=15,
        permiso_uso_nombre="PERMISO-SE-2025-062",
    )
)

print(f"✓ Empresa registrada exitosamente")
print(f"TX ID: {result.tx_ids[0]}")
print(f"Verifica en Lora: https://lora.algokit.io/testnet/transaction/{result.tx_ids[0]}")
