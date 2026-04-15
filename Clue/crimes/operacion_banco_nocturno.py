"""
operacion_banco_nocturno.py — La Operación del Banco Nocturno

Durante la madrugada se produjo un acceso ilegal al sistema central del Banco Nocturno y se desviaron fondos a cuentas externas.
El Ingeniero Torres tenía credenciales activas y realizó accesos remotos al sistema esa noche.
La Analista Vega tenía permisos administrativos y aprobó transacciones sospechosas.
El Gerente Silva tenía registro de vuelo internacional durante toda la noche del incidente.
El Guardia López tenía registro verificado de turno en una sucursal distinta durante el mismo periodo.
El Ingeniero Torres no tiene coartada verificada.
La Analista Vega no tiene coartada verificada.
El Ingeniero Torres y la Analista Vega pertenecen al mismo grupo interno llamado red_interna.
Un sistema automatizado reportó actividades sospechosas del Ingeniero Torres y de la Analista Vega.
El Guardia López acusa al Ingeniero Torres.
El Ingeniero Torres declara que la Analista Vega autorizó todo el proceso.
La Analista Vega declara que el Ingeniero Torres actuó por iniciativa propia.

Como detective, he llegado a las siguientes conclusiones:
Quien tiene registro oficial que lo ubica fuera del lugar del crimen está descartado.
Quien realiza accesos no autorizados al sistema participa en el delito.
Quien aprueba transacciones fraudulentas comete fraude financiero.
Quien participa en el delito y no tiene coartada verificada es culpable.
Quien comete fraude financiero y no tiene coartada verificada es culpable.
Dos personas comparten red si pertenecen al mismo grupo interno.
Si dos culpables comparten red, existe una operación coordinada entre ellos.
El testimonio de una persona descartada contra alguien es confiable.
Una red está activa si al menos uno de sus miembros es culpable.
Todo reportado por el sistema pertenece al conjunto de sospechosos críticos.
"""

from src.crime_case import CrimeCase, QuerySpec
from src.predicate_logic import ExistsGoal, ForallGoal, KnowledgeBase, Predicate, Rule, Term


def crear_kb() -> KnowledgeBase:
    kb = KnowledgeBase()

    # Constantes
    ing_torres = Term("ing_torres")
    analista_vega = Term("analista_vega")
    gerente_silva = Term("gerente_silva")
    guardia_lopez = Term("guardia_lopez")
    red_interna = Term("red_interna")

    # === YOUR CODE HERE ===

    # Hechos
    kb.add_fact(Predicate("acceso_sistema", (ing_torres,)))
    kb.add_fact(Predicate("aprueba_transacciones", (analista_vega,)))

    kb.add_fact(Predicate("registro_fuera", (gerente_silva,)))
    kb.add_fact(Predicate("registro_fuera", (guardia_lopez,)))

    kb.add_fact(Predicate("sin_coartada", (ing_torres,)))
    kb.add_fact(Predicate("sin_coartada", (analista_vega,)))

    kb.add_fact(Predicate("pertenece_red", (ing_torres, red_interna)))
    kb.add_fact(Predicate("pertenece_red", (analista_vega, red_interna)))

    kb.add_fact(Predicate("reportado_sistema", (ing_torres,)))
    kb.add_fact(Predicate("reportado_sistema", (analista_vega,)))

    kb.add_fact(Predicate("acusa", (guardia_lopez, ing_torres)))

    # Reglas
    kb.add_rule(
        Rule(
            head=Predicate("descartado", (Term("$X"),)),
            body=(Predicate("registro_fuera", (Term("$X"),)),),
        )
    )

    kb.add_rule(
        Rule(
            head=Predicate("participa_delito", (Term("$X"),)),
            body=(Predicate("acceso_sistema", (Term("$X"),)),),
        )
    )

    kb.add_rule(
        Rule(
            head=Predicate("fraude_financiero", (Term("$X"),)),
            body=(Predicate("aprueba_transacciones", (Term("$X"),)),),
        )
    )

    kb.add_rule(
        Rule(
            head=Predicate("culpable", (Term("$X"),)),
            body=(
                Predicate("participa_delito", (Term("$X"),)),
                Predicate("sin_coartada", (Term("$X"),)),
            ),
        )
    )

    kb.add_rule(
        Rule(
            head=Predicate("culpable", (Term("$X"),)),
            body=(
                Predicate("fraude_financiero", (Term("$X"),)),
                Predicate("sin_coartada", (Term("$X"),)),
            ),
        )
    )

    kb.add_rule(
        Rule(
            head=Predicate("comparten_red", (Term("$X"), Term("$Y"), Term("$R"))),
            body=(
                Predicate("pertenece_red", (Term("$X"), Term("$R"))),
                Predicate("pertenece_red", (Term("$Y"), Term("$R"))),
            ),
        )
    )

    kb.add_rule(
        Rule(
            head=Predicate("operacion_coordinada", (Term("$X"), Term("$Y"))),
            body=(
                Predicate("culpable", (Term("$X"),)),
                Predicate("culpable", (Term("$Y"),)),
                Predicate("comparten_red", (Term("$X"), Term("$Y"), Term("$R"))),
            ),
        )
    )

    kb.add_rule(
        Rule(
            head=Predicate("testimonio_confiable", (Term("$X"), Term("$Y"))),
            body=(
                Predicate("descartado", (Term("$X"),)),
                Predicate("acusa", (Term("$X"), Term("$Y"))),
            ),
        )
    )

    kb.add_rule(
        Rule(
            head=Predicate("red_activa", (Term("$R"),)),
            body=(
                Predicate("pertenece_red", (Term("$X"), Term("$R"))),
                Predicate("culpable", (Term("$X"),)),
            ),
        )
    )

    kb.add_rule(
        Rule(
            head=Predicate("sospechoso_critico", (Term("$X"),)),
            body=(Predicate("reportado_sistema", (Term("$X"),)),),
        )
    )

    # === END YOUR CODE ===

    return kb


CASE = CrimeCase(
    id="operacion_banco_nocturno",
    title="La Operación del Banco Nocturno",
    suspects=("ing_torres", "analista_vega", "gerente_silva", "guardia_lopez"),
    narrative=__doc__,
    description=(
        "Un ataque al sistema financiero durante la madrugada revela accesos indebidos y transacciones sospechosas. "
        "Dos empleados con roles distintos podrían haber coordinado el fraude."
    ),
    create_kb=crear_kb,
    queries=(
        QuerySpec(
            description="¿El Gerente Silva está descartado?",
            goal=Predicate("descartado", (Term("gerente_silva"),)),
        ),
        QuerySpec(
            description="¿El Ingeniero Torres es culpable?",
            goal=Predicate("culpable", (Term("ing_torres"),)),
        ),
        QuerySpec(
            description="¿La Analista Vega cometió fraude financiero?",
            goal=Predicate("fraude_financiero", (Term("analista_vega"),)),
        ),
        QuerySpec(
            description="¿Existe operación coordinada entre Torres y Vega?",
            goal=Predicate("operacion_coordinada", (Term("ing_torres"), Term("analista_vega"))),
        ),
        QuerySpec(
            description="¿El testimonio del Guardia López contra Torres es confiable?",
            goal=Predicate("testimonio_confiable", (Term("guardia_lopez"), Term("ing_torres"))),
        ),
        QuerySpec(
            description="¿Existe alguna red activa?",
            goal=ExistsGoal("$R", Predicate("red_activa", (Term("$R"),))),
        ),
        QuerySpec(
            description="¿Todo reportado por el sistema es sospechoso crítico?",
            goal=ForallGoal(
                "$X",
                Predicate("reportado_sistema", (Term("$X"),)),
                Predicate("sospechoso_critico", (Term("$X"),)),
            ),
        ),
    ),
)