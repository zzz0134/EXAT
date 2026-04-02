from __future__ import annotations

from typing import Any

from exat.tables.main_tables import run_main_table


def run_appendix_table(model: Any, batch: Any, labels: Any) -> list[dict[str, Any]]:
    """Appendix-table runner reuses unified APIs and generic table flow."""

    attack_keys = [
        "heo_2019",
        "eabd_2023",
        "singleadv_2024",
        "advedge_2024",
        "advedge_plus_2024",
        "our",
        "our1",
        "our2",
        "composite_2025",
    ]
    return run_main_table(model, batch, labels, attack_keys=attack_keys)
