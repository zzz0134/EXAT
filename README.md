# EXAT

Three-layer scaffolding with unified APIs:

1. `attacks`: `AttackMethod.generate(inputs, labels, context)`
2. `defenses`: `Defense.apply(inputs, logits=None)`
3. `explainers`: `Explainer.explain(model, inputs, targets=None)`

Implemented attack registry keys:
- `composite_2025`
- `advedge_2024`
- `advedge_plus_2024`
- `singleadv_2024`
- `eabd_2023`
- `heo_2019`
- `our`
- `our1`
- `our2`

Implemented defenses:
- `agg_mean`
- `opt_agg`
- `aggec`
- `hardening_detector`

Implemented 7 explainers:
- `grad_cam`
- `grad_cam_pp`
- `integrated_gradients`
- `saliency`
- `smoothgrad`
- `occlusion`
- `guided_backprop`
