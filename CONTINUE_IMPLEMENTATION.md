# Quick Start: Continuing Implementation

Use this guide to pick up where we left off.

## What's Done

✅ **Task 3** (JSON Schema) - Complete
✅ **Task 5** (Pipeline Core) - Framework complete, needs implementation
✅ **Task 1** (Validators) - Pre-eval complete (19 tests passing)

## What's Next

### Immediate: Complete Validator Tests (2-3 days)

**Copy the pre_eval pattern** to create remaining test files:

```bash
# 1. Create test file from template
cp tests/test_validators_pre_eval.py tests/test_validators_pre_aggregate.py

# 2. Update imports and test names
# 3. Read the validator to understand what it tests
# 4. Create fixtures in tests/fixtures/validators/pre_aggregate/
# 5. Write tests following established patterns

# Repeat for:
# - pre_workbook
# - rules_validators
# - guidelines_validators
# - stacking_validators
```

**Test Pattern**:
```python
class TestValidatorFunction:
    def test_valid_case(self):
        fixture_path = Path("tests/fixtures/validators/{name}/valid_case")
        result = validate_function(fixture_path, ...)
        assert result.valid is True

    def test_error_case(self):
        result = validate_function(...)
        assert result.valid is False
        errors = [i for i in result.issues if i.severity == Severity.ERROR]
        assert len(errors) > 0

class TestValidationResultStructure:
    def test_result_has_valid_flag(self): ...
    def test_result_has_issues_list(self): ...
```

**Run tests**:
```bash
~/.pyenv/shims/python -m pytest tests/test_validators_*.py -v
```

---

### Implement Pipeline Methods (2-3 days)

**Edit `framework/pipeline.py`** and replace placeholders:

#### 1. `score_evaluation()` method

```python
def score_evaluation(self, contract, model, canonical_json_path, contract_type=None):
    # Load GT
    gt_result = self.load_ground_truth(contract, contract_type)

    # Load canonical JSON
    with open(canonical_json_path) as f:
        canonical = json.load(f)

    # Mode-specific scoring
    if self.config['mode'] == 'freeform':
        from framework.scoring import calculate_detection_points
        # Use existing scoring functions
        scored = score_freeform(gt_result['data'], canonical, self.config)
    elif self.config['mode'] == 'rules':
        scored = score_rules(gt_result['data'], canonical, self.config)
    # ... etc for other modes

    return scored
```

**Note**: You may need to look at the notebook or existing scoring code to see exactly how scoring is currently done. The scoring functions already exist in `framework/scoring/`.

#### 2. `aggregate_results()` method

```python
def aggregate_results(self, run_dirs, output_dir):
    aggregated = {}

    # Read all evaluations
    for run_dir in run_dirs:
        eval_dir = run_dir / "evaluations"
        for contract_dir in eval_dir.iterdir():
            if not contract_dir.is_dir():
                continue
            contract = contract_dir.name

            for model_file in contract_dir.glob("*.json"):
                model = model_file.stem
                key = f"{contract}_{model}"

                with open(model_file) as f:
                    data = json.load(f)

                if key not in aggregated:
                    aggregated[key] = []
                aggregated[key].append(data)

    # Write aggregated results
    output_dir.mkdir(parents=True, exist_ok=True)
    for key, runs in aggregated.items():
        with open(output_dir / f"{key}.json", "w") as f:
            json.dump({"runs": runs, "summary": compute_summary(runs)}, f, indent=2)

    return {"files_written": len(aggregated)}
```

#### 3. `generate_workbook()` method

```python
def generate_workbook(self, aggregated_dir, output_path, env):
    import openpyxl

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Summary"

    # Read aggregated files and create worksheets
    for json_file in aggregated_dir.glob("*.json"):
        with open(json_file) as f:
            data = json.load(f)

        # Create worksheet for this contract/model
        # Add headers, data, formatting
        # (Look at existing workbook generation code for patterns)

    wb.save(output_path)
    return output_path
```

**Test it**:
```bash
~/.pyenv/shims/python -c "
from pathlib import Path
from framework.pipeline import EvaluationPipeline

pipeline = EvaluationPipeline('freeform')
# Test with your actual evaluation data
"
```

---

### Add Common Utilities (1.5 days)

**Edit `framework/validators/base.py`**, add to end:

```python
def normalise_clause_ref(clause_ref: str) -> str:
    """Strip common prefixes from clause references."""
    import re
    # Remove "Section ", "Clause ", "Article ", "§ " prefixes
    patterns = [r'^Section\s+', r'^Clause\s+', r'^Article\s+', r'^§\s*']
    result = clause_ref
    for pattern in patterns:
        result = re.sub(pattern, '', result, flags=re.IGNORECASE)
    return result.strip()

def clause_refs_match(clause1: str, clause2: str) -> bool:
    """Check if two clause references match after normalisation."""
    return normalise_clause_ref(clause1) == normalise_clause_ref(clause2)

def extract_significant_words(text: str, min_length: int = 3) -> set[str]:
    """Extract words longer than min_length from text."""
    import re
    words = re.findall(r'\b\w+\b', text.lower())
    return {w for w in words if len(w) >= min_length}

def calculate_word_overlap_ratio(text1: str, text2: str, min_word_length: int = 3) -> float:
    """Calculate ratio of overlapping words between two texts."""
    words1 = extract_significant_words(text1, min_word_length)
    words2 = extract_significant_words(text2, min_word_length)

    if not words1 or not words2:
        return 0.0

    overlap = words1 & words2
    return len(overlap) / min(len(words1), len(words2))
```

**Create `tests/test_validators_base_utils.py`**:
```python
def test_normalise_clause_ref():
    assert normalise_clause_ref("Section 5.1") == "5.1"
    assert normalise_clause_ref("Clause 3.2") == "3.2"
    assert normalise_clause_ref("§ 12.4") == "12.4"

def test_clause_refs_match():
    assert clause_refs_match("Section 5.1", "5.1")
    assert not clause_refs_match("5.1", "5.2")
```

**Refactor validators** to use these utilities:
```python
# In guidelines_validators.py, replace local implementation:
from .base import normalise_clause_ref, clause_refs_match

# Replace this:
def _clause_refs_match(clause1, clause2):
    ...local implementation...

# With this:
# (Just use clause_refs_match directly)
```

**CRITICAL - Regression Test**:
```bash
# Before refactoring
~/.pyenv/shims/python -m pytest tests/test_validators_*.py -v > before.txt

# After refactoring
~/.pyenv/shims/python -m pytest tests/test_validators_*.py -v > after.txt

# Must be identical
diff before.txt after.txt
```

---

### Create Integration Tests (2 days)

**1. Create test dataset**:
```bash
mkdir -p tests/fixtures/integration/test_dataset/freeform/{ground_truth,canonical_json/test_contract_1}
```

**2. Create minimal GT file**:
```json
{
  "ground_truth": [
    {"gt_id": "GT001", "gt_tier": "T1", "clause": "1.1", "issue": "Test T1 issue"},
    {"gt_id": "GT002", "gt_tier": "T2", "clause": "2.1", "issue": "Test T2 issue"}
  ]
}
```

**3. Create canonical JSON** (model output):
```json
{
  "contract": "test_contract_1",
  "model": "test_model",
  "gt_evaluations": [
    {"gt_id": "GT001", "detection": "Y", "points": 8},
    {"gt_id": "GT002", "detection": "N", "points": 0}
  ],
  "summary": {
    "total_points": 8,
    "max_points": 13,
    "pass_fail": "PASS"
  }
}
```

**4. Create golden output file**:
```json
{
  "expected_detection_points": 8,
  "expected_pass_fail": "PASS"
}
```

**5. Write test**:
```python
def test_freeform_pipeline_end_to_end():
    fixture_path = Path("tests/fixtures/integration/test_dataset/freeform")
    golden = Path("tests/fixtures/integration/expected_outputs/freeform/test_contract_1.json")

    # Run scoring
    pipeline = EvaluationPipeline("freeform", mode_dir=fixture_path)
    result = pipeline.score_evaluation(
        "test_contract_1",
        "test_model",
        fixture_path / "canonical_json/test_contract_1/test_model.json"
    )

    # Load golden output
    with open(golden) as f:
        expected = json.load(f)

    # Verify
    assert result['summary']['total_points'] == expected['expected_detection_points']
    assert result['summary']['pass_fail'] == expected['expected_pass_fail']
```

---

## Quick Commands

```bash
# Run all tests
~/.pyenv/shims/python -m pytest tests/ -v

# Run specific test file
~/.pyenv/shims/python -m pytest tests/test_validators_pre_eval.py -v

# Check coverage
~/.pyenv/shims/python -m pytest tests/test_validators_*.py --cov=framework/validators --cov-report=html

# Test CLI
~/.pyenv/shims/python -m framework.cli freeform hotfix --validate-only

# Validate all configs
~/.pyenv/shims/python -c "
from pathlib import Path
from framework.config_loader import validate_all_configs
configs = validate_all_configs(Path('framework/config'))
print(f'✓ {len(configs)} configs validated')
"
```

---

## Files to Reference

- `tests/test_validators_pre_eval.py` - Pattern for validator tests
- `framework/pipeline.py` - Pipeline class to implement
- `framework/validators/base.py` - Add utilities here
- `notebooks/01_evaluation_pipeline.ipynb` - See how scoring currently works

---

## Estimated Time Remaining

- Validator tests: 2-3 days
- Pipeline implementation: 2-3 days
- Common utilities: 1.5 days
- Integration tests: 2 days

**Total: 7.5-9.5 days**

---

## Questions?

Check `IMPLEMENTATION_STATUS.md` for full details on what's done, what remains, and design decisions made.
