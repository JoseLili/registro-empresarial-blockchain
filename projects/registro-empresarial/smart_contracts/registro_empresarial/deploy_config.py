import logging
import algokit_utils

logger = logging.getLogger(__name__)


def deploy() -> None:
    from smart_contracts.artifacts.registro_empresarial.registro_empresarial_client import (
        RegistroEmpresarialFactory,
    )

    algorand = algokit_utils.AlgorandClient.from_environment()
    deployer = algorand.account.from_environment("DEPLOYER")

    factory = algorand.client.get_typed_app_factory(
        RegistroEmpresarialFactory, default_sender=deployer.address
    )

    app_client, result = factory.send.create.crear()

    logger.info(
        f"Contrato desplegado: {app_client.app_client.app_name} "
        f"(App ID: {app_client.app_client.app_id}) "
        f"(Dirección: {app_client.app_client.app_address})"
    )

    algorand.send.payment(
        algokit_utils.PaymentParams(
            amount=algokit_utils.AlgoAmount(algo=2),
            sender=deployer.address,
            receiver=app_client.app_client.app_address,
        )
    )
    logger.info("Contrato fondeado con 2 ALGO para Box Storage")
