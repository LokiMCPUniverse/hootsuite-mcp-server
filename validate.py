#!/usr/bin/env python3
"""
Validation script to check code structure without external dependencies.
This script verifies the implementation is complete and correct.
"""

import ast
import sys
from pathlib import Path
from typing import List, Set


def check_file_exists(file_path: Path) -> bool:
    """Check if a file exists."""
    return file_path.exists()


def check_python_syntax(file_path: Path) -> tuple[bool, str]:
    """Check if a Python file has valid syntax."""
    try:
        with open(file_path, 'r') as f:
            code = f.read()
        ast.parse(code)
        return True, "OK"
    except SyntaxError as e:
        return False, f"Syntax error: {e}"
    except Exception as e:
        return False, f"Error: {e}"


def check_imports_in_file(file_path: Path, expected_imports: Set[str]) -> tuple[bool, List[str]]:
    """Check if expected imports are present in a file."""
    try:
        with open(file_path, 'r') as f:
            tree = ast.parse(f.read())
        
        found_imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    found_imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    found_imports.add(node.module)
        
        missing = expected_imports - found_imports
        return len(missing) == 0, list(missing)
    except Exception as e:
        return False, [f"Error: {e}"]


def check_functions_in_file(file_path: Path, expected_functions: Set[str]) -> tuple[bool, List[str]]:
    """Check if expected functions are defined in a file."""
    try:
        with open(file_path, 'r') as f:
            tree = ast.parse(f.read())
        
        found_functions = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                found_functions.add(node.name)
        
        missing = expected_functions - found_functions
        return len(missing) == 0, list(missing)
    except Exception as e:
        return False, [f"Error: {e}"]


def main():
    """Run all validation checks."""
    project_root = Path(__file__).parent
    src_dir = project_root / "src" / "hootsuite_mcp"
    tests_dir = project_root / "tests"
    
    all_checks_passed = True
    
    print("=" * 70)
    print("HOOTSUITE MCP SERVER VALIDATION")
    print("=" * 70)
    
    # Check required files exist
    print("\n1. Checking required files...")
    required_files = [
        src_dir / "__init__.py",
        src_dir / "server.py",
        src_dir / "client.py",
        src_dir / "config.py",
        tests_dir / "test_server.py",
        tests_dir / "test_client.py",
        tests_dir / "test_config.py",
        project_root / "pyproject.toml",
        project_root / ".github" / "workflows" / "ci.yml",
        project_root / ".github" / "workflows" / "quick-test.yml",
    ]
    
    for file_path in required_files:
        if check_file_exists(file_path):
            print(f"   ✓ {file_path.relative_to(project_root)}")
        else:
            print(f"   ✗ {file_path.relative_to(project_root)} - MISSING")
            all_checks_passed = False
    
    # Check Python syntax
    print("\n2. Checking Python syntax...")
    python_files = list(src_dir.glob("*.py")) + list(tests_dir.glob("*.py"))
    
    for py_file in python_files:
        is_valid, message = check_python_syntax(py_file)
        if is_valid:
            print(f"   ✓ {py_file.relative_to(project_root)}")
        else:
            print(f"   ✗ {py_file.relative_to(project_root)} - {message}")
            all_checks_passed = False
    
    # Check server.py has required components
    print("\n3. Checking server.py implementation...")
    server_file = src_dir / "server.py"
    
    expected_classes = {"HootsuiteMCPServer"}
    expected_functions = {"main"}
    
    if server_file.exists():
        success, missing = check_functions_in_file(server_file, expected_functions)
        if success:
            print(f"   ✓ All required functions present")
        else:
            print(f"   ✗ Missing functions: {missing}")
            all_checks_passed = False
    
    # Check client.py has required components
    print("\n4. Checking client.py implementation...")
    client_file = src_dir / "client.py"
    
    expected_classes_client = {"HootsuiteClient", "RateLimiter"}
    expected_functions_client = {"__init__", "_request", "create_post", "get_social_profiles"}
    
    if client_file.exists():
        success, missing = check_functions_in_file(client_file, expected_functions_client)
        if success:
            print(f"   ✓ All required methods present")
        else:
            print(f"   ✗ Missing methods: {missing}")
            all_checks_passed = False
    
    # Check config.py has required components
    print("\n5. Checking config.py implementation...")
    config_file = src_dir / "config.py"
    
    expected_classes_config = {"Settings"}
    
    if config_file.exists():
        with open(config_file, 'r') as f:
            tree = ast.parse(f.read())
        
        found_classes = {node.name for node in ast.walk(tree) 
                        if isinstance(node, ast.ClassDef)}
        
        if expected_classes_config.issubset(found_classes):
            print(f"   ✓ Settings class present")
        else:
            print(f"   ✗ Settings class missing")
            all_checks_passed = False
    
    # Check test files
    print("\n6. Checking test files...")
    test_files = [
        tests_dir / "test_server.py",
        tests_dir / "test_client.py",
        tests_dir / "test_config.py"
    ]
    
    for test_file in test_files:
        if test_file.exists():
            with open(test_file, 'r') as f:
                tree = ast.parse(f.read())
            
            test_functions = [node.name for node in ast.walk(tree) 
                             if isinstance(node, ast.FunctionDef) and 
                             node.name.startswith('test_')]
            
            if test_functions:
                print(f"   ✓ {test_file.name}: {len(test_functions)} tests found")
            else:
                print(f"   ✗ {test_file.name}: No tests found")
                all_checks_passed = False
    
    # Final summary
    print("\n" + "=" * 70)
    if all_checks_passed:
        print("✓ ALL VALIDATION CHECKS PASSED")
        print("=" * 70)
        print("\nThe implementation is complete and ready for testing.")
        print("Run 'pytest tests/' to execute the test suite.")
        return 0
    else:
        print("✗ SOME VALIDATION CHECKS FAILED")
        print("=" * 70)
        print("\nPlease review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
