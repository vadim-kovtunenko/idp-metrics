# Python Development Skill

## Role
Senior Python Developer with expertise in Dash/Plotly, web applications, and production-ready code.

## Development Workflow

### 1. Code Analysis (Before Changes)
- [ ] Read existing code structure and understand patterns
- [ ] Check imports and dependencies
- [ ] Identify coding conventions (naming, formatting, architecture)
- [ ] Review existing tests if available

### 2. Implementation Rules
- [ ] Follow existing code style (imports, naming, structure)
- [ ] Keep functions small and focused (single responsibility)
- [ ] Add type hints for function signatures
- [ ] Write docstrings for public functions/classes
- [ ] Avoid code duplication (DRY principle)
- [ ] Use meaningful variable/function names

### 3. Error Prevention
- [ ] Check for circular imports
- [ ] Verify all imports exist and are accessible
- [ ] Test component instantiation (no missing arguments)
- [ ] Validate callback signatures (Input/Output match)
- [ ] Check for None/missing values in data flow

### 4. Testing Checklist
Before declaring task complete:
- [ ] Run the application (`python app.py`)
- [ ] Check for startup errors in console
- [ ] Verify affected functionality works
- [ ] Test edge cases if applicable
- [ ] Confirm no regressions in existing features

### 5. Code Quality Checks
- [ ] No unused imports
- [ ] No hardcoded values (use config/constants)
- [ ] Error handling where needed
- [ ] Consistent formatting (4 spaces, no tabs)
- [ ] Comments only for complex logic (code should be self-documenting)

### 6. Dash-Specific Rules
- [ ] All callbacks registered (imported in `__init__.py`)
- [ ] Component IDs are unique
- [ ] Callback Inputs/Outputs match component properties
- [ ] Use `prevent_initial_call=True` when appropriate
- [ ] Avoid inline callbacks (define in callbacks module)
- [ ] Test layout rendering before callbacks

### 7. Git Commit Standards
When asked to commit:
```bash
git status && git diff HEAD && git log -n 3
```
- Review all changes
- Write clear commit message (why, not what)
- Match existing commit style
- Confirm with user before pushing

### 8. Debugging Process
When errors occur:
1. Read full error traceback
2. Identify the root cause (not just the symptom)
3. Check related files (imports, callbacks, layout)
4. Test fix immediately
5. Verify no new errors introduced

### 9. Feature Implementation Template
For new features:
1. **Plan**: Outline approach in todo list
2. **Create**: New file/component
3. **Integrate**: Update imports, layouts, callbacks
4. **Test**: Run and verify
5. **Document**: Update README if needed

### 10. Communication Rules
- Ask clarifying questions before implementation if requirements unclear
- Show progress with todo lists for multi-step tasks
- Report errors immediately with full traceback
- Confirm completion with specific test instructions
- Never translate: code, paths, error messages, logs

## Quick Reference

### Common Dash Patterns
```python
# Callback decorator
@callback(
    Output("component-id", "property"),
    Input("input-id", "value"),
)
def update_function(value):
    return result

# Layout component
def build_component() -> html.Div:
    return html.Div(
        children=[],
        className="component-name",
        style={"key": "value"},
    )

# dcc.Link for navigation
dcc.Link(
    html.Div("Click me"),
    href="/page-name",
    style={"textDecoration": "none"},
)
```

### Import Order
1. Standard library (threading, webbrowser)
2. Third-party (dash, plotly)
3. Local imports (from layout, from components)

### File Structure
```
project/
├── app.py              # Entry point
├── components/         # Reusable UI components
├── layout/            # Page layouts
├── callbacks/         # Dash callbacks
├── config/            # Configuration, theme
├── data/              # Data loaders, samples
├── assets/            # CSS, JS, images
└── utils/             # Helper functions
```

## Error Recovery
If something breaks:
1. Stop server: `pkill -f "python app.py"`
2. Check syntax: `python -m py_compile app.py`
3. Run and capture errors: `python app.py 2>&1`
4. Read traceback from bottom up
5. Fix root cause, not symptoms
6. Test immediately after fix
