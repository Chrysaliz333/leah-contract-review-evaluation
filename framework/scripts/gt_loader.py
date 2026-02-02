"""Mode-aware Ground Truth loader for multi-mode evaluation.

Interprets gt_structure from mode config to load GT files correctly for:
- flat: One GT file per contract (freeform, guidelines)
- dual_part: Part A + Part B (freeform_stacking)
- per_contract_type: One GT file per contract type (rules, rules_stacking)
"""

from pathlib import Path
import json
from typing import Optional
from dataclasses import dataclass


@dataclass
class GTLoadResult:
    """Result of GT loading with metadata."""
    data: dict
    gt_type: str  # flat, dual_part, per_contract_type
    source_files: list[Path]


class GTLoader:
    """Mode-aware Ground Truth loader.

    Interprets gt_structure from mode config to load GT files.
    """

    def __init__(self, mode_dir: Path, config: dict):
        self.mode_dir = mode_dir
        self.config = config
        self.gt_structure = config.get("gt_structure", {})
        self.paths_config = config.get("paths", {})
        self.gt_type = self.gt_structure.get("type", "flat")

    def load(
        self,
        contract: str,
        contract_type: Optional[str] = None
    ) -> GTLoadResult:
        """Load GT for a contract respecting mode configuration."""
        if self.gt_type == "flat":
            return self._load_flat(contract)
        elif self.gt_type == "dual_part":
            return self._load_dual_part(contract)
        elif self.gt_type == "per_contract_type":
            return self._load_per_contract_type(contract, contract_type)
        else:
            raise ValueError(f"Unknown GT type: {self.gt_type}")

    def _load_file(self, path: Path) -> dict:
        """Load and validate a single GT file."""
        if not path.exists():
            raise FileNotFoundError(f"GT file not found: {path}")
        with open(path) as f:
            return json.load(f)

    def _load_flat(self, contract: str) -> GTLoadResult:
        """Load single GT file for contract (freeform, guidelines)."""
        gt_dir = self.mode_dir / self.paths_config.get("ground_truth", "ground_truth")
        pattern = self.paths_config.get("gt_pattern", "{contract}.json")

        # Handle both string pattern and dict pattern (for dual_part fallback)
        if isinstance(pattern, dict):
            pattern = "{contract}.json"

        gt_path = gt_dir / pattern.format(contract=contract)
        data = self._load_file(gt_path)
        return GTLoadResult(data=data, gt_type="flat", source_files=[gt_path])

    def _load_dual_part(self, contract: str) -> GTLoadResult:
        """Load dual-part GT (Part A from this mode, Part B from freeform)."""
        gt_dir = self.mode_dir / self.paths_config.get("ground_truth", "ground_truth")
        gt_pattern = self.paths_config.get("gt_pattern", {})

        # Part A: CP redlines from this mode (stacking GT)
        stacking_contract = f"{contract}_stacking"
        part_a_path = gt_dir / f"{stacking_contract}.json"
        if not part_a_path.exists():
            part_a_pattern = gt_pattern.get("part_a", "{contract}_part_a.json")
            part_a_path = gt_dir / part_a_pattern.format(contract=contract)

        # Part B: Whole document from freeform GT
        part_b_pattern = gt_pattern.get("part_b", "../freeform/ground_truth/{contract}.json")
        part_b_path = (gt_dir / part_b_pattern.format(contract=contract)).resolve()

        source_files = []

        # Load Part A (may not exist for all contracts)
        part_a_data = {"ground_truth": [], "part_a_cp_redlines": []}
        if part_a_path.exists():
            part_a_data = self._load_file(part_a_path)
            source_files.append(part_a_path)

        # Load Part B (should exist)
        part_b_data = {"ground_truth": []}
        if part_b_path.exists():
            part_b_data = self._load_file(part_b_path)
            source_files.append(part_b_path)

        return GTLoadResult(
            data={
                "part_a": part_a_data,
                "part_b": part_b_data,
                "gt_metadata": {
                    "mode": self.config.get("mode"),
                    "contract": contract,
                    "dual_part": True
                }
            },
            gt_type="dual_part",
            source_files=source_files
        )

    def _load_per_contract_type(
        self,
        contract: str,
        contract_type: Optional[str] = None
    ) -> GTLoadResult:
        """Load GT file for contract type (rules, rules_stacking, guidelines)."""
        gt_dir = self.mode_dir / self.paths_config.get("ground_truth", "ground_truth")

        # Determine contract type if not provided
        if not contract_type:
            contract_type = self._infer_contract_type(contract)

        # Find matching GT file
        gt_files = self.gt_structure.get("files", [f"{contract_type}.json"])
        gt_path = None
        for f in gt_files:
            if contract_type.lower() in f.lower():
                gt_path = gt_dir / f
                break

        if not gt_path or not gt_path.exists():
            raise FileNotFoundError(
                f"GT file not found for contract_type '{contract_type}'. "
                f"Searched in: {gt_dir}"
            )

        data = self._load_file(gt_path)
        return GTLoadResult(data=data, gt_type="per_contract_type", source_files=[gt_path])

    def _infer_contract_type(self, contract: str) -> str:
        """Infer contract type from contract ID prefix."""
        contract_types = self.config.get("contract_types", [])
        contract_lower = contract.lower()

        for ct in contract_types:
            if contract_lower.startswith(ct.lower()):
                return ct.lower()

        # Fallback: check contains
        for ct in contract_types:
            if ct.lower() in contract_lower:
                return ct.lower()

        raise ValueError(
            f"Cannot determine contract_type for '{contract}'. "
            f"Expected prefix from: {contract_types}"
        )


def load_gt_for_mode(
    mode_dir: Path,
    config: dict,
    contract: str,
    contract_type: Optional[str] = None
) -> GTLoadResult:
    """Convenience function for GT loading."""
    loader = GTLoader(mode_dir, config)
    return loader.load(contract, contract_type)
