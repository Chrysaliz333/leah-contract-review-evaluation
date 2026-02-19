# Learning Log — Leah Evaluation Framework

A reflection log for capturing insights, patterns, and questions while developing the evaluation framework.

---

## 2026-02-17 — Architecting Large Refactoring Projects

### Context
Implemented foundation for framework improvements: JSON schema validation, pipeline orchestration, CLI interface, and comprehensive test infrastructure. Completed ~25% of a 9-11 day plan in one focused session.

### What I Should Have Learned

#### 1. **Flexible Design Beats Perfect Design**
The JSON schema could have been strict (enforcing identical structure across all 5 modes) but instead was made flexible to accommodate existing variations. Only core fields are required; mode-specific fields are optional.

**Key insight**: When retrofitting validation to existing systems, accommodate reality rather than forcing uniformity. The schema still catches genuine errors (missing required fields, invalid JSON) while allowing valid structural differences.

**Pattern to remember**:
```python
# Strict approach (would break existing configs):
required: ["mode", "display_name", "models", "detection_points", ...]

# Flexible approach (works with reality):
required: ["mode", "display_name", "paths", "gt_structure"]
# Everything else is optional, validated where present
```

#### 2. **Orchestration Should Delegate, Not Duplicate**
The `EvaluationPipeline` class doesn't reimplement scoring logic, validation logic, or GT loading. It coordinates existing modules through a clean API.

**Key insight**: Orchestration code is about sequencing and error handling, not business logic. Keep it thin. Delegate to specialized modules.

**Anti-pattern avoided**:
```python
# DON'T: Reimplement scoring in pipeline
class EvaluationPipeline:
    def score_evaluation(self, ...):
        # 200 lines of scoring logic here
```

**Better pattern**:
```python
# DO: Delegate to existing modules
class EvaluationPipeline:
    def score_evaluation(self, ...):
        gt = self.gt_loader.load(contract)
        canonical = load_json(path)
        return score_freeform(gt, canonical, self.config)  # Delegate
```

#### 3. **Testing Patterns Scale Through Templates**
Creating 19 tests for pre_eval validator established a clear pattern that can be replicated 5 more times. The test structure (TestValidatorFunction + TestValidationResultStructure) and fixture organization make the remaining work mechanical.

**Key insight**: When facing repetitive work, invest time upfront to create one excellent example. The time spent perfecting the pattern pays back exponentially.

**Test pattern established**:
```
tests/fixtures/validators/{name}/
  ├── valid_case/          # Should pass
  ├── error_case_1/        # Should fail (ERROR)
  ├── warning_case_1/      # Should warn (WARNING)
  └── edge_case_1/         # Boundary conditions

tests/test_validators_{name}.py
  class TestValidatorFunction:
      def test_valid_case(): ...
      def test_error_case(): ...
  class TestValidationResultStructure:
      def test_result_structure(): ...
```

#### 4. **Placeholders Enable Parallel Progress**
The pipeline class has placeholder implementations for `score_evaluation()`, `aggregate_results()`, and `generate_workbook()`. This seems incomplete, but it's strategic: the orchestration layer can now be tested independently while implementation details are filled in later.

**Key insight**: Don't block on implementation details when you can establish interfaces. Placeholders with clear TODOs are better than waiting for perfect implementations.

**Pattern**:
```python
def score_evaluation(self, ...):
    # Load data
    gt = self.load_ground_truth(contract)
    canonical = load_json(path)

    # PLACEHOLDER: Delegate to mode-specific scoring
    # TODO: Integrate with framework/scoring modules
    return {"scoring": "not_implemented", "gt_count": len(gt)}
```

This lets you test:
- Config loading
- GT loading
- Validation gates
- Error handling
- CLI interface

...while deferring mode-specific scoring logic.

#### 5. **Documentation That's Actually Useful**
Created two docs: `IMPLEMENTATION_STATUS.md` (where we are) and `CONTINUE_IMPLEMENTATION.md` (how to continue). The latter includes code templates, commands to run, and patterns to follow.

**Key insight**: Documentation should reduce cognitive load for future-you. Don't just describe what's done—show exactly how to continue with copy-pasteable examples.

**Template that helps**:
```markdown
### Immediate: Complete Validator Tests (2-3 days)

**Copy the pre_eval pattern**:
```bash
cp tests/test_validators_pre_eval.py tests/test_validators_pre_aggregate.py
# Edit: update imports, test names
# Run: pytest tests/test_validators_pre_aggregate.py -v
```

**Test pattern**:
```python
class TestValidatorFunction:
    def test_valid_case(self):
        fixture = Path("tests/fixtures/validators/pre_aggregate/valid")
        result = validate_pre_aggregation(...)
        assert result.valid is True
```
```

This is infinitely more useful than "Write tests for pre_aggregate validator."

### Reflection Questions

#### On Design Decisions
1. **When should I choose flexible design over strict design?**
   - When retrofitting to existing systems?
   - When requirements are still evolving?
   - What's the cost of being too flexible? (Less validation, harder to catch errors)

2. **How do I know when orchestration code is doing too much?**
   - If it has business logic, it's doing too much
   - If tests require mocking domain concepts, it's doing too much
   - Should orchestration ever do anything beyond: load config → call module → handle errors → log results?

3. **What makes a good "placeholder" implementation?**
   - This session used placeholders that return valid structure but say "not_implemented"
   - When is a placeholder good enough to commit?
   - How do you prevent placeholders from becoming permanent?

#### On Implementation Strategy
4. **Should I have completed one vertical slice instead of three horizontal layers?**
   - Horizontal: schema + pipeline + tests (foundation)
   - Vertical: complete one mode end-to-end (freeform only)
   - Which approach validates assumptions faster?
   - Which approach is easier to demonstrate progress?

5. **When should common utilities be extracted?**
   - This plan says: after tests, before refactoring
   - Why not extract utilities first, then write tests against them?
   - Does it matter if you extract utilities based on 2 examples vs 5 examples?

6. **How much testing is enough before committing?**
   - Committed with 19 tests for 1 validator, 5 validators remain untested
   - Config validation complete but no tests for config_loader.py
   - Pipeline class has no tests yet
   - Is this "foundation complete" or "proof of concept"?

#### On Managing Scope
7. **How do you decide what's "core complete" vs "fully done"?**
   - Marked Task 5 as "core complete" with placeholders
   - What's the risk of calling something "complete" when it has TODOs?
   - How do you communicate incomplete work without it sounding like failure?

8. **Should the 9-11 day plan have been sequenced differently?**
   - Started with Task 3 (schema) + Task 5 (pipeline) + partial Task 1 (tests)
   - Original plan said: Task 1 → Task 4 → Task 2 → Task 5
   - Does establishing the API first make implementation easier?
   - Or does implementing first make the API design more informed?

#### On Code Quality
9. **What's the line between "good enough" and "production ready"?**
   - EvaluationPipeline works but has placeholders
   - Config validation works but gracefully degrades if schema is missing
   - Tests pass but coverage is ~20% of what's planned
   - For an internal tool (evaluation framework), what's the bar?

10. **How should error messages balance helpfulness with brevity?**
    - Config loader includes field paths, allowed values, checked paths
    - Is there such a thing as too much error context?
    - Compare: "Invalid config" vs "Field 'mode' must be one of: [freeform, rules, ...]"

### Patterns I Want to Remember

**Pattern: Flexible Schema Design**
```json
{
  "required": ["essential_fields"],
  "properties": {
    "optional_field": {
      "type": "string",
      "description": "Only validated if present"
    }
  },
  "additionalProperties": false  // Catches typos but allows new fields
}
```

**Pattern: Orchestration Class Structure**
```python
class Pipeline:
    def __init__(self, config):
        # Load and validate config
        # Initialize delegates (loaders, validators)

    def validate_prerequisites(self, stage):
        # Call validator, handle errors

    def run_full_pipeline(self):
        # Sequence: validate → process → output
        # Error handling at orchestration level
```

**Pattern: Test Fixture Organization**
```
tests/fixtures/{module}/{validator}/
  ├── valid_case/          # Positive case
  ├── error_case_X/        # Each error condition
  ├── warning_case_X/      # Each warning condition
  └── edge_case_X/         # Boundaries
```

### Questions for Next Session

1. **Integration strategy**: Should I complete validator tests first (establish confidence in validation layer) or implement pipeline methods first (establish confidence in orchestration)?

2. **Common utilities**: The plan says extract shared code from 3 validators. But should I wait until all validator tests are done to see the full pattern? Or extract early and risk having to revise?

3. **Testing philosophy**: What's the right level of testing for orchestration code? Mock everything? Use real fixtures? How do you test error paths without making tests brittle?

4. **Incremental delivery**: Could I deliver this in smaller chunks? For example: schema validation → merge → pipeline framework → merge → implementation → merge? Or does the foundation need to be complete first?

5. **Documentation maintenance**: IMPLEMENTATION_STATUS.md is already 250 lines. How do you keep status docs from becoming stale as work progresses?

### What Surprised Me

- **Config variation across modes**: Assumed configs would be more uniform. Turns out rules_stacking uses "scoring" instead of "detection_points", guidelines doesn't require "models" at the top level. Reality is messy.

- **How quickly patterns solidify**: After writing pre_eval tests, the remaining 5 validator test files feel mechanical. The hard part was figuring out the pattern, not implementing it.

- **Value of placeholder implementations**: Initially felt wrong to commit methods that return `{"scoring": "not_implemented"}`. But it unblocks testing the orchestration layer, which is valuable.

- **Documentation as implementation guide**: Wrote CONTINUE_IMPLEMENTATION.md as a "how to continue" guide. Realized it's more valuable than typical docs because it shows exactly what to do next with code templates.

### Action Items

- [ ] Decide implementation order for remaining work (tests first vs implementation first)
- [ ] Consider whether config_loader needs tests or if validation by usage is sufficient
- [ ] Review scoring module to understand current patterns before implementing pipeline.score_evaluation()
- [ ] Check if similar orchestration patterns exist elsewhere in framework to maintain consistency

---
