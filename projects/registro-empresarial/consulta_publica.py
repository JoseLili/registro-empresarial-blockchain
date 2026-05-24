import algokit_utils
from dotenv import load_dotenv
from smart_contracts.artifacts.registro_empresarial.registro_empresarial_client import (
    RegistroEmpresarialFactory,
    ConsultarEmpresaArgs,
)

load_dotenv()

# Usa el mismo .env — la consulta readonly no requiere firmar nada
algorand = algokit_utils.AlgorandClient.from_environment()

APP_ID = 763199151
EXPEDIENTE = "NOTARIA-42-2024-001"

factory = algorand.client.get_typed_app_factory(
    RegistroEmpresarialFactory,
    default_sender="JVKLMK2U7ERR2BFTRX7RJ3GOW7T5TYLZI565FISBYXZJOXDQYGBAA7JQY4"
)

app_client = factory.get_app_client_by_id(app_id=APP_ID)

print(f"=== Consulta pública — App ID: {APP_ID} ===")
print(f"Buscando expediente: {EXPEDIENTE}\n")

resultado = app_client.send.consultar_empresa(
    args=ConsultarEmpresaArgs(expediente=EXPEDIENTE)
)

empresa = resultado.abi_return
print(f"Razón social:        {empresa.razon_social}")
print(f"RFC:                 {empresa.rfc if empresa.rfc else '(pendiente de tramitar)'}")
print(f"Tipo de sociedad:    {empresa.tipo_sociedad}")
print(f"Estatus:             {empresa.estatus}")
print(f"Representante legal: {empresa.representante_legal}")
print(f"Domicilio fiscal:    {empresa.domicilio_fiscal}")
print(f"Reparto acciones:    {empresa.reparto_acciones}")
print(f"Número notaría:      {empresa.numero_notaria}")
print(f"Permiso uso nombre:  {empresa.permiso_uso_nombre}")
