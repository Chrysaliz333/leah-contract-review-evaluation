"""Playbook loader for Guidelines mode evaluation.

Loads playbook files from guidelines/playbooks/ and provides position
hierarchy resolution: Gold Standard > Fallback 1 > Fallback 2 > Red Flag

Position hierarchy determines how to score Leah's response based on
which standard position she achieved.
"""

from pathlib import Path
import json
from typing import Optional
from dataclasses import dataclass


@dataclass
class PlaybookPosition:
    """A position within the playbook hierarchy."""
    name: str  # e.g., "Gold Standard", "Fallback 1", "Red Flag"
    rank: int  # 1 = Gold Standard (best), 4 = Red Flag (worst)
    description: str
    key_elements: list[str]


@dataclass
class PlaybookClause:
    """Playbook guidance for a specific clause type."""
    clause_name: str
    positions: list[PlaybookPosition]


class PlaybookLoader:
    """Loads and provides access to playbook position hierarchy.

    Playbooks define acceptable positions for each clause type:
    - Gold Standard (rank 1): Ideal position
    - Fallback 1 (rank 2): Acceptable alternative
    - Fallback 2 (rank 3): Less preferred but acceptable
    - Red Flag (rank 4): Unacceptable, must be detected
    """

    POSITION_RANKS = {
        "gold standard": 1,
        "gold_standard": 1,
        "gs": 1,
        "fallback 1": 2,
        "fallback_1": 2,
        "fb1": 2,
        "fallback 2": 3,
        "fallback_2": 3,
        "fb2": 3,
        "red flag": 4,
        "red_flag": 4,
        "rf": 4,
    }

    def __init__(self, playbook_dir: Path):
        self.playbook_dir = playbook_dir
        self._playbooks: dict[str, dict] = {}

    def load(self, contract_type: str) -> dict:
        """Load playbook for a contract type.

        Args:
            contract_type: e.g., "nda", "subcontract"

        Returns:
            Playbook data with clause guidance
        """
        if contract_type in self._playbooks:
            return self._playbooks[contract_type]

        # Find playbook file
        playbook_path = self._find_playbook_file(contract_type)
        if not playbook_path:
            raise FileNotFoundError(
                f"Playbook not found for contract_type '{contract_type}' "
                f"in {self.playbook_dir}"
            )

        with open(playbook_path) as f:
            playbook = json.load(f)

        self._playbooks[contract_type] = playbook
        return playbook

    def _find_playbook_file(self, contract_type: str) -> Optional[Path]:
        """Find playbook file for contract type."""
        patterns = [
            f"{contract_type}_playbook.json",
            f"{contract_type}.json",
            f"playbook_{contract_type}.json",
        ]

        for pattern in patterns:
            path = self.playbook_dir / pattern
            if path.exists():
                return path

        return None

    def get_clause_guidance(
        self,
        playbook: dict,
        clause_name: str
    ) -> Optional[dict]:
        """Get guidance for a specific clause from playbook.

        Args:
            playbook: Loaded playbook data
            clause_name: Name of the clause (e.g., "Confidential Information")

        Returns:
            Clause guidance with positions, or None if not found
        """
        clauses = playbook.get("clauses", playbook.get("guidance", []))

        for clause in clauses:
            if clause.get("clause_name", "").lower() == clause_name.lower():
                return clause
            # Also match on clause_type
            if clause.get("clause_type", "").lower() == clause_name.lower():
                return clause

        return None

    def get_position_rank(self, position_name: str) -> int:
        """Get numeric rank for a position name.

        Args:
            position_name: e.g., "Gold Standard", "Red Flag"

        Returns:
            Rank (1-4), defaults to 4 (Red Flag) if unknown
        """
        return self.POSITION_RANKS.get(position_name.lower().strip(), 4)

    def is_red_flag(self, position_name: str) -> bool:
        """Check if position is a Red Flag."""
        return self.get_position_rank(position_name) == 4

    def resolve_achieved_position(
        self,
        playbook: dict,
        clause_name: str,
        leah_text: str,
        leah_action: str
    ) -> Optional[str]:
        """Resolve which playbook position Leah achieved.

        Args:
            playbook: Loaded playbook data
            clause_name: Clause being evaluated
            leah_text: Leah's proposed text/amendment
            leah_action: Leah's recommended action

        Returns:
            Position name achieved, or None if cannot determine
        """
        guidance = self.get_clause_guidance(playbook, clause_name)
        if not guidance:
            return None

        positions = guidance.get("positions", [])

        # Check each position from best to worst
        for position in sorted(positions, key=lambda p: self.get_position_rank(p.get("name", ""))):
            key_elements = position.get("key_elements", [])
            acceptable_actions = position.get("acceptable_actions", [])

            # Check if Leah's text contains key elements
            if key_elements and leah_text:
                text_lower = leah_text.lower()
                elements_found = sum(
                    1 for elem in key_elements
                    if any(word.lower() in text_lower for word in elem.split()[:3] if len(word) > 3)
                )

                if elements_found >= len(key_elements) * 0.5:
                    return position.get("name")

            # Check if action matches
            if acceptable_actions and leah_action:
                if leah_action.upper() in [a.upper() for a in acceptable_actions]:
                    return position.get("name")

        return None


def load_playbook(playbook_dir: Path, contract_type: str) -> dict:
    """Convenience function to load a playbook."""
    loader = PlaybookLoader(playbook_dir)
    return loader.load(contract_type)


def resolve_position_hierarchy(
    playbook_dir: Path,
    contract_type: str,
    clause_name: str,
    leah_text: str,
    leah_action: str
) -> Optional[str]:
    """Convenience function to resolve position hierarchy."""
    loader = PlaybookLoader(playbook_dir)
    playbook = loader.load(contract_type)
    return loader.resolve_achieved_position(playbook, clause_name, leah_text, leah_action)
