from exat.attacks import ATTACKS, AttackContext
from exat.defenses import DEFENSES
from exat.explainers import EXPLAINERS
from exat.tables.appendix_tables import run_appendix_table


class DummyModel:
    def __call__(self, x):
        return x


def test_attack_registry_contains_requested_methods():
    expected = {
        "composite_2025",
        "advedge_2024",
        "advedge_plus_2024",
        "singleadv_2024",
        "eabd_2023",
        "heo_2019",
        "our",
        "our1",
        "our2",
    }
    assert expected.issubset(set(ATTACKS))


def test_defense_registry_contains_requested_methods():
    assert set(DEFENSES) == {"agg_mean", "opt_agg", "aggec", "hardening_detector"}


def test_explainer_registry_has_explicit_seven_methods():
    assert set(EXPLAINERS) == {
        "grad_cam",
        "grad_cam_pp",
        "integrated_gradients",
        "saliency",
        "smoothgrad",
        "occlusion",
        "guided_backprop",
    }


def test_table_pipeline_uses_unified_apis_end_to_end():
    model = DummyModel()
    rows = run_appendix_table(model=model, batch=[1, 2], labels=[0, 1])
    assert rows
    assert {"attack", "defense", "explainer", "result"}.issubset(rows[0].keys())


def test_attack_api_shape_generate():
    model = DummyModel()
    attack = ATTACKS["heo_2019"]
    output = attack.generate([1], [0], AttackContext(model=model, metadata={"attack": attack.name}))
    assert "adv_inputs" in output
