from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping


@dataclass
class Defense:
    """Unified defense API."""

    name: str

    def apply(self, inputs: Any, logits: Any | None = None) -> Any:
        raise NotImplementedError


@dataclass
class FunctionalDefense(Defense):
    fn: Callable[[Any, Any | None], Any]

    def apply(self, inputs: Any, logits: Any | None = None) -> Any:
        return self.fn(inputs, logits)


def _identity(inputs: Any, logits: Any | None = None) -> Any:
    return {"defended": inputs, "logits": logits}


DEFENSES: Mapping[str, Defense] = {
    "agg_mean": FunctionalDefense("AGG-Mean", _identity),
    "opt_agg": FunctionalDefense("Opt-Agg", _identity),
    "aggec": FunctionalDefense("AGGEC", _identity),
    "hardening_detector": FunctionalDefense("Hardening detector", _identity),
}


def build_defense(key: str) -> Defense:
    defense = DEFENSES[key]
    return type(defense)(**defense.__dict__)
