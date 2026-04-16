"""
model_checking.py

Este modulo contiene las funciones de model checking proposicional.

Hint: Usa las funciones get_atoms() y evaluate() de logic_core.py.
"""

from __future__ import annotations

from src.logic_core import Formula, evaluate, get_atoms


def get_all_models(atoms: set[str]) -> list[dict[str, bool]]:
    """
    Genera todos los modelos posibles (asignaciones de verdad).
    Para n atomos, genera 2^n modelos.

    Args:
        atoms: Conjunto de nombres de atomos proposicionales.

    Returns:
        Lista de diccionarios, cada uno mapeando atomos a valores booleanos.

    Ejemplo:
        >>> get_all_models({'p', 'q'})
        [{'p': True, 'q': True}, {'p': True, 'q': False},
         {'p': False, 'q': True}, {'p': False, 'q': False}]

    Hint: Piensa en como representar los numeros del 0 al 2^n - 1 en binario.
          Cada bit corresponde al valor de verdad de un atomo.
    """

    # 
    #
    # Versión inicial:
    # La primera versión construida intentaba generar los modelos
    # con ciclos anidados y un orden manual para pocos átomos.
    # Esa versión no escalaba bien para cualquier número de átomos.
    #
    # Código inicial:
    # def get_all_models(atoms):
    #     atoms = list(atoms)
    #     if len(atoms) == 1:
    #         return [{atoms[0]: True}, {atoms[0]: False}]
    #     return []
    #
    # Prompts utilizados con IA:
    # - "Implementa get_all_models usando representación binaria"
    # - "Haz una versión general para n átomos"
    # - "Conserva el orden del ejemplo del enunciado"

    atom_list = sorted(atoms)
    n = len(atom_list)
    models: list[dict[str, bool]] = []

    for i in range(2**n):
        model: dict[str, bool] = {}
        for j, atom in enumerate(atom_list):
            # Queremos el orden del ejemplo:
            # TT, TF, FT, FF para {'p', 'q'}
            bit = (i >> (n - 1 - j)) & 1
            model[atom] = (bit == 0)
        models.append(model)

    return models


def check_satisfiable(formula: Formula) -> tuple[bool, dict[str, bool] | None]:
    """
    Determina si una formula es satisfacible.

    Args:
        formula: Formula logica a verificar.

    Returns:
        (True, modelo) si encuentra un modelo que la satisface.
        (False, None) si es insatisfacible.

    Ejemplo:
        >>> check_satisfiable(And(Atom('p'), Not(Atom('p'))))
        (False, None)

    Hint: Genera todos los modelos con get_all_models(), luego evalua
          la formula en cada uno usando evaluate().
    """
   
   
 
    # La primera versión revisaba pocos casos manuales y no recorría
    # todos los modelos de la fórmula.
    #
    # Código inicial:
    # def check_satisfiable(formula):
    #     atoms = get_atoms(formula)
    #     models = get_all_models(atoms)
    #     if len(models) == 0:
    #         return (False, None)
    #     return (evaluate(formula, models[0]), models[0])
    #
    # Prompts utilizados con IA:
    # - "Implementa check_satisfiable recorriendo todos los modelos"
    # - "Usa get_atoms y evaluate como dice el enunciado"
    # - "Retorna (True, modelo) o (False, None)"
    #

    atoms = get_atoms(formula)
    models = get_all_models(atoms)

    for model in models:
        if evaluate(formula, model):
            return True, model

    return False, None


def check_valid(formula: Formula) -> bool:
    """
    Determina si una formula es una tautologia (valida en todo modelo).

    Args:
        formula: Formula logica a verificar.

    Returns:
        True si la formula es verdadera en todos los modelos posibles.

    Ejemplo:
        >>> check_valid(Or(Atom('p'), Not(Atom('p'))))
        True

    Hint: Una formula es valida si y solo si su negacion es insatisfacible.
          Alternativamente, verifica que sea verdadera en TODOS los modelos.
    """
   

    models = get_all_models(atoms)

    for model in models:
        if not evaluate(formula, model):
            return False

    return True


def check_entailment(kb: list[Formula], query: Formula) -> bool:
    """
    Determina si KB |= query (la base de conocimiento implica la consulta).

    Args:
        kb: Lista de formulas que forman la base de conocimiento.
        query: Formula que queremos verificar si se sigue de la KB.

    Returns:
        True si la query es verdadera en todos los modelos donde la KB es verdadera.

    Ejemplo:
        >>> kb = [Implies(Atom('p'), Atom('q')), Atom('p')]
        >>> check_entailment(kb, Atom('q'))
        True

    Hint: KB |= q  si y solo si  KB ^ ~q es insatisfacible.
          Es decir, no existe un modelo donde toda la KB sea verdadera
          y la query sea falsa.
    """

    # La primera versión solo revisaba si la query era verdadera
    # en algún modelo, sin condicionar a que la KB también lo fuera.
    #
    # Código inicial:
    # def check_entailment(kb, query):
    #     atoms = get_atoms(query)
    #     for m in get_all_models(atoms):
    #         if evaluate(query, m):
    #             return True
    #     return False
    #
    # Prompts utilizados con IA:
    # - "Implementa check_entailment correctamente"
    # - "KB |= q significa: en todo modelo donde KB es verdadera, q también"
    # - "Incluye átomos de la KB y de la query"
    #


    atoms = set()
    for formula in kb:
        atoms.update(get_atoms(formula))
    atoms.update(get_atoms(query))

    models = get_all_models(atoms)

    for model in models:
        kb_true = all(evaluate(formula, model) for formula in kb)
        query_true = evaluate(query, model)

        if kb_true and not query_true:
            return False

    return True


def truth_table(formula: Formula) -> list[tuple[dict[str, bool], bool]]:
    """
    Genera la tabla de verdad completa de una formula.

    Args:
        formula: Formula logica.

    Returns:
        Lista de tuplas (modelo, resultado) para cada modelo posible.

    Ejemplo:
        >>> truth_table(And(Atom('p'), Atom('q')))
        [({'p': True, 'q': True}, True),
         ({'p': True, 'q': False}, False),
         ({'p': False, 'q': True}, False),
         ({'p': False, 'q': False}, False)]

    Hint: Combina get_all_models() y evaluate().
    """
    atoms = get_atoms(formula)
    models = get_all_models(atoms)

    return [(model, evaluate(formula, model)) for model in models]