from algopy import ARC4Contract, GlobalState, UInt64, Txn, BoxMap, arc4, subroutine, String


# ── ARC-28 Events ─────────────────────────────────────────────────────────────

class EmpresaRegistrada(arc4.Struct):
    expediente: arc4.String      # Llave única - número de libro/operación notarial
    razon_social: arc4.String
    tipo_sociedad: arc4.String
    numero_notaria: arc4.UInt64  # Inmutable - queda en event Y en Box para consulta pública
    registrador: arc4.Address


class CampoActualizado(arc4.Struct):
    expediente: arc4.String
    campo: arc4.String
    valor_nuevo: arc4.String
    registrador: arc4.Address


class RFCRegistrado(arc4.Struct):
    # RFC tiene su propio event porque tiene regla especial: solo se escribe una vez
    expediente: arc4.String
    rfc: arc4.String
    registrador: arc4.Address


class EstatusModificado(arc4.Struct):
    expediente: arc4.String
    estatus_anterior: arc4.String
    estatus_nuevo: arc4.String
    registrador: arc4.Address


class RegistradorAgregado(arc4.Struct):
    cuenta: arc4.Address


class RegistradorRemovido(arc4.Struct):
    cuenta: arc4.Address


# ── Estructura de datos de empresa ────────────────────────────────────────────

class DatosEmpresa(arc4.Struct):
    razon_social: arc4.String
    rfc: arc4.String              # Inicia vacío, se escribe una sola vez
    tipo_sociedad: arc4.String    # Validado por enumeración
    estatus: arc4.String          # Validado por enumeración: activa, suspendida, disuelta
    representante_legal: arc4.String
    domicilio_fiscal: arc4.String
    reparto_acciones: arc4.String
    numero_notaria: arc4.UInt64   # Inmutable
    permiso_uso_nombre: arc4.String


# ── Contrato principal ────────────────────────────────────────────────────────

class RegistroEmpresarial(ARC4Contract):

    def __init__(self) -> None:
        self.admin = GlobalState(arc4.Address)
        self.total_empresas = GlobalState(UInt64)
        self.empresas = BoxMap(arc4.String, DatosEmpresa)
        self.registradores = BoxMap(arc4.Address, arc4.Bool)

    # ── Despliegue ────────────────────────────────────────────────────────────

    @arc4.abimethod(create="require")
    def crear(self) -> None:
        """Se ejecuta una sola vez al desplegar. El deployer se vuelve admin."""
        self.admin.value = arc4.Address(Txn.sender)
        self.total_empresas.value = UInt64(0)

    # ── Gestión de registradores (solo admin) ─────────────────────────────────

    @arc4.abimethod()
    def agregar_registrador(self, cuenta: arc4.Address) -> None:
        assert (
            arc4.Address(Txn.sender) == self.admin.value
        ), "Solo el admin puede agregar registradores"
        self.registradores[cuenta] = arc4.Bool(True)
        arc4.emit(RegistradorAgregado(cuenta=cuenta))

    @arc4.abimethod()
    def remover_registrador(self, cuenta: arc4.Address) -> None:
        assert (
            arc4.Address(Txn.sender) == self.admin.value
        ), "Solo el admin puede remover registradores"
        assert cuenta in self.registradores, "La cuenta no es registradora"
        del self.registradores[cuenta]
        arc4.emit(RegistradorRemovido(cuenta=cuenta))

    # ── Registro inicial de empresa ───────────────────────────────────────────

    @arc4.abimethod()
    def registrar_empresa(
        self,
        expediente: arc4.String,
        razon_social: arc4.String,
        tipo_sociedad: arc4.String,
        representante_legal: arc4.String,
        domicilio_fiscal: arc4.String,
        reparto_acciones: arc4.String,
        numero_notaria: arc4.UInt64,
        permiso_uso_nombre: arc4.String,
    ) -> None:
        """
        Da de alta una empresa. El expediente notarial es el identificador único.
        El RFC inicia vacío — se registra después con registrar_rfc().
        """
        assert self._es_registrador(), "No autorizado para registrar empresas"
        assert expediente not in self.empresas, "El expediente ya está registrado"
        assert self._tipo_sociedad_valido(tipo_sociedad), "Tipo de sociedad no válido"

        self.empresas[expediente] = DatosEmpresa(
            razon_social=razon_social,
            rfc=arc4.String(""),          # Vacío hasta tramitar RFC ante el SAT
            tipo_sociedad=tipo_sociedad,
            estatus=arc4.String("activa"),
            representante_legal=representante_legal,
            domicilio_fiscal=domicilio_fiscal,
            reparto_acciones=reparto_acciones,
            numero_notaria=numero_notaria,
            permiso_uso_nombre=permiso_uso_nombre,
        )
        self.total_empresas.value = self.total_empresas.value + UInt64(1)
        arc4.emit(
            EmpresaRegistrada(
                expediente=expediente,
                razon_social=razon_social,
                tipo_sociedad=tipo_sociedad,
                numero_notaria=numero_notaria,
                registrador=arc4.Address(Txn.sender),
            )
        )

    # ── Registro de RFC (solo una vez) ────────────────────────────────────────

    @arc4.abimethod()
    def registrar_rfc(self, expediente: arc4.String, rfc: arc4.String) -> None:
        """
        Registra el RFC de una empresa. Solo puede hacerse una vez.
        El RFC llega después de la constitución — no al momento del alta.
        """
        assert self._es_registrador(), "No autorizado"
        assert expediente in self.empresas, "Empresa no encontrada"
        empresa = self.empresas[expediente].copy()
        assert empresa.rfc.native == String(""), "El RFC ya fue registrado y no puede modificarse"
        empresa.rfc = rfc
        self.empresas[expediente] = empresa.copy()
        arc4.emit(RFCRegistrado(
            expediente=expediente,
            rfc=rfc,
            registrador=arc4.Address(Txn.sender),
        ))

    # ── Actualizaciones de campos mutables ────────────────────────────────────

    @arc4.abimethod()
    def actualizar_razon_social(self, expediente: arc4.String, valor: arc4.String) -> None:
        assert self._es_registrador(), "No autorizado"
        assert expediente in self.empresas, "Empresa no encontrada"
        empresa = self.empresas[expediente].copy()
        empresa.razon_social = valor
        self.empresas[expediente] = empresa.copy()
        arc4.emit(CampoActualizado(
            expediente=expediente,
            campo=arc4.String("razon_social"),
            valor_nuevo=valor,
            registrador=arc4.Address(Txn.sender),
        ))

    @arc4.abimethod()
    def actualizar_representante_legal(self, expediente: arc4.String, valor: arc4.String) -> None:
        assert self._es_registrador(), "No autorizado"
        assert expediente in self.empresas, "Empresa no encontrada"
        empresa = self.empresas[expediente].copy()
        empresa.representante_legal = valor
        self.empresas[expediente] = empresa.copy()
        arc4.emit(CampoActualizado(
            expediente=expediente,
            campo=arc4.String("representante_legal"),
            valor_nuevo=valor,
            registrador=arc4.Address(Txn.sender),
        ))

    @arc4.abimethod()
    def actualizar_domicilio(self, expediente: arc4.String, valor: arc4.String) -> None:
        assert self._es_registrador(), "No autorizado"
        assert expediente in self.empresas, "Empresa no encontrada"
        empresa = self.empresas[expediente].copy()
        empresa.domicilio_fiscal = valor
        self.empresas[expediente] = empresa.copy()
        arc4.emit(CampoActualizado(
            expediente=expediente,
            campo=arc4.String("domicilio_fiscal"),
            valor_nuevo=valor,
            registrador=arc4.Address(Txn.sender),
        ))

    @arc4.abimethod()
    def actualizar_reparto_acciones(self, expediente: arc4.String, valor: arc4.String) -> None:
        assert self._es_registrador(), "No autorizado"
        assert expediente in self.empresas, "Empresa no encontrada"
        empresa = self.empresas[expediente].copy()
        empresa.reparto_acciones = valor
        self.empresas[expediente] = empresa.copy()
        arc4.emit(CampoActualizado(
            expediente=expediente,
            campo=arc4.String("reparto_acciones"),
            valor_nuevo=valor,
            registrador=arc4.Address(Txn.sender),
        ))

    @arc4.abimethod()
    def actualizar_permiso_uso_nombre(self, expediente: arc4.String, valor: arc4.String) -> None:
        assert self._es_registrador(), "No autorizado"
        assert expediente in self.empresas, "Empresa no encontrada"
        empresa = self.empresas[expediente].copy()
        empresa.permiso_uso_nombre = valor
        self.empresas[expediente] = empresa.copy()
        arc4.emit(CampoActualizado(
            expediente=expediente,
            campo=arc4.String("permiso_uso_nombre"),
            valor_nuevo=valor,
            registrador=arc4.Address(Txn.sender),
        ))

    @arc4.abimethod()
    def cambiar_estatus(self, expediente: arc4.String, nuevo_estatus: arc4.String) -> None:
        """Valores válidos: activa, suspendida, disuelta"""
        assert self._es_registrador(), "No autorizado"
        assert expediente in self.empresas, "Empresa no encontrada"
        assert (
            nuevo_estatus.native == String("activa")
            or nuevo_estatus.native == String("suspendida")
            or nuevo_estatus.native == String("disuelta")
        ), "Estatus inválido. Use: activa, suspendida o disuelta"
        empresa = self.empresas[expediente].copy()
        estatus_anterior = empresa.estatus
        empresa.estatus = nuevo_estatus
        self.empresas[expediente] = empresa.copy()
        arc4.emit(EstatusModificado(
            expediente=expediente,
            estatus_anterior=estatus_anterior,
            estatus_nuevo=nuevo_estatus,
            registrador=arc4.Address(Txn.sender),
        ))

    # ── Consultas públicas ────────────────────────────────────────────────────

    @arc4.abimethod(readonly=True)
    def consultar_empresa(self, expediente: arc4.String) -> DatosEmpresa:
        """Cualquiera puede consultar. No genera transacción ni costo."""
        assert expediente in self.empresas, "Empresa no encontrada"
        return self.empresas[expediente].copy()

    @arc4.abimethod(readonly=True)
    def es_registrador(self, cuenta: arc4.Address) -> arc4.Bool:
        if cuenta in self.registradores:
            return arc4.Bool(self.registradores[cuenta].native)
        return arc4.Bool(False)

    @arc4.abimethod(readonly=True)
    def obtener_total(self) -> UInt64:
        return self.total_empresas.value

    # ── Subroutines internas ──────────────────────────────────────────────────

    @subroutine
    def _es_registrador(self) -> bool:
        sender = arc4.Address(Txn.sender)
        if sender in self.registradores:
            return self.registradores[sender].native
        return False

    @subroutine
    def _tipo_sociedad_valido(self, tipo: arc4.String) -> bool:
        """Enumeración de tipos de sociedad válidos en México."""
        t = tipo.native
        return (
            t == String("S.A.")
            or t == String("S. de R.L.")
            or t == String("S.A.S.")
            or t == String("S.C.L.")
            or t == String("S.C.V.")
            or t == String("S. en N.C.")
            or t == String("S. en C.")
            or t == String("S. en C. por A.")
            or t == String("S.C.")
            or t == String("A.C.")
            or t == String("S.A.P.I.")
        )