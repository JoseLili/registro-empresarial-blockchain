import algokit_utils
from dotenv import load_dotenv
from smart_contracts.artifacts.registro_empresarial.registro_empresarial_client import (
    RegistroEmpresarialFactory,
    AgregarRegistradorArgs,
)

load_dotenv()

algorand = algokit_utils.AlgorandClient.from_environment()
deployer = algorand.account.from_environment("DEPLOYER")

factory = algorand.client.get_typed_app_factory(
    RegistroEmpresarialFactory, default_sender=deployer.address
)

app_client = factory.get_app_client_by_id(app_id=763199151)

print("Agregando Pera Wallet como registradora...")
result = app_client.send.agregar_registrador(
    args=AgregarRegistradorArgs(
        cuenta="OVP2IBHMIRHB2KIGUEPT4TROKG42IJ5HRRTS3NCUKCMNWIRE53JKWZLNQI"
    )
)
print(f"Listo. TX: {result.tx_ids[0]}")
