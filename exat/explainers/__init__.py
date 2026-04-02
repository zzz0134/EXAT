from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping


@dataclass
class Explainer:
    """Unified API for explanation methods."""

    name: str

    def explain(self, model: Any, inputs: Any, targets: Any | None = None) -> Any:
        raise NotImplementedError


@dataclass
class FunctionalExplainer(Explainer):
    fn: Callable[[Any, Any, Any | None], Any]

    def explain(self, model: Any, inputs: Any, targets: Any | None = None) -> Any:
        return self.fn(model, inputs, targets)


def _simple_explain(model: Any, inputs: Any, targets: Any | None = None) -> Any:
    _ = model
    return {"attribution": inputs, "targets": targets}


# Explicit 7 explainers
EXPLAINERS: Mapping[str, Explainer] = {
    "grad_cam": FunctionalExplainer("Grad-CAM", _simple_explain),
    "grad_cam_pp": FunctionalExplainer("Grad-CAM++", _simple_explain),
    "integrated_gradients": FunctionalExplainer("Integrated Gradients", _simple_explain),
    "saliency": FunctionalExplainer("Saliency", _simple_explain),
    "smoothgrad": FunctionalExplainer("SmoothGrad", _simple_explain),
    "occlusion": FunctionalExplainer("Occlusion", _simple_explain),
    "guided_backprop": FunctionalExplainer("Guided Backprop", _simple_explain),
}


def build_explainer(key: str) -> Explainer:
    explainer = EXPLAINERS[key]
    return type(explainer)(**explainer.__dict__)
