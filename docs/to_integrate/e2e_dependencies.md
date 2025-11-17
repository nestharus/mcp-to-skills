[ELIDED] existing code [ELIDED]
[dependency-groups]
dev = [
"httpx==0.28.1",
"pytest==9.0.1",
"pytest-asyncio==1.3.0",
"pytest-check==2.5.0",
"ruff==0.14.5",
[ELIDED] existing code [ELIDED]
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
markers = [
"e2e: marks tests as end-to-end (requires running server)",
]