from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Mapping, Protocol


class ModelLike(Protocol):
    def __call__(self, x: Any) -> Any: ...


@dataclass
class AttackContext:
    model: ModelLike
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AttackMethod:
    """Unified API for all attack methods."""

    name: str

    def generate(self, inputs: Any, labels: Any, context: AttackContext) -> Any:
        raise NotImplementedError


@dataclass
class WrappedAttack(AttackMethod):
    """Adapter for public-code baselines."""

    runner: Callable[[Any, Any, AttackContext], Any]

    def generate(self, inputs: Any, labels: Any, context: AttackContext) -> Any:
        return self.runner(inputs, labels, context)


@dataclass
class ReimplementedAttack(AttackMethod):
    """Placeholder for paper reimplementations."""

    algorithm: Callable[[Any, Any, AttackContext], Any]

    def generate(self, inputs: Any, labels: Any, context: AttackContext) -> Any:
        return self.algorithm(inputs, labels, context)


def _echo_attack(inputs: Any, labels: Any, context: AttackContext) -> Any:
    return {"adv_inputs": inputs, "labels": labels, "attack": context.metadata.get("attack")}


ATTACKS: Mapping[str, AttackMethod] = {
    # Public-code wrappers
    "heo_2019": WrappedAttack("Heo 2019", _echo_attack),
    "eabd_2023": WrappedAttack("EABD 2023", _echo_attack),
    "singleadv_2024": WrappedAttack("SingleADV 2024", _echo_attack),
    "advedge_2024": WrappedAttack("AdvEdge 2024", _echo_attack),
    "advedge_plus_2024": WrappedAttack("AdvEdge+ 2024", _echo_attack),
    # In-repo methods
    "our": ReimplementedAttack("our", _echo_attack),
    "our1": ReimplementedAttack("our1", _echo_attack),
    "our2": ReimplementedAttack("our2", _echo_attack),
    # Missing-code paper reimplementation target
    "composite_2025": ReimplementedAttack("Composite 2025", _echo_attack),
}


def build_attack(key: str, **metadata: Any) -> AttackMethod:
    attack = ATTACKS[key]
    attack_copy = type(attack)(**attack.__dict__)
    if metadata:
        # metadata is attached at callsite via context
        metadata.setdefault("attack", attack.name)
    return attack_copy
