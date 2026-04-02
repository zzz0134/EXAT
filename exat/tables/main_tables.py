from __future__ import annotations

from typing import Any, Iterable

from exat.attacks import ATTACKS, AttackContext
from exat.defenses import DEFENSES
from exat.explainers import EXPLAINERS


def run_main_table(model: Any, batch: Any, labels: Any, attack_keys: Iterable[str]) -> list[dict[str, Any]]:
    """Main-table runner that calls only unified APIs."""

    rows: list[dict[str, Any]] = []
    for attack_key in attack_keys:
        attack = ATTACKS[attack_key]
        context = AttackContext(model=model, metadata={"attack": attack.name})
        adv = attack.generate(batch, labels, context)
        for defense in DEFENSES.values():
            defended = defense.apply(adv)
            for explainer in EXPLAINERS.values():
                explanation = explainer.explain(model, defended, labels)
                rows.append(
                    {
                        "attack": attack.name,
                        "defense": defense.name,
                        "explainer": explainer.name,
                        "result": explanation,
                    }
                )
    return rows
