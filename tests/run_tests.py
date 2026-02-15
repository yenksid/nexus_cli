import os
import shutil
import json
from pathlib import Path

# Save the base directory so we can always return to it safely
BASE_DIR = Path.cwd()
TEST_DIR = BASE_DIR / "test_output"

def setup_environment():
    """Cleans up previous test runs and prepares the test directory."""
    print("🧹 Cleaning previous test data...")
    if TEST_DIR.exists(): 
        shutil.rmtree(TEST_DIR)
    TEST_DIR.mkdir()

def test_route_a_new_project():
    """
    ROUTE A: The 'From Scratch' User
    Workflow: nexus scaffold -> nexus init -> nexus scan
    """
    print("\n" + "="*50)
    print("🚀 ROUTE A: NEW PROJECT WORKFLOW")
    print("="*50)
    
    # 1. Provide the tree file
    tree_file = BASE_DIR / "tree.txt"
    if not tree_file.exists():
        print("❌ Error: tree.txt not found in the root directory.")
        return False

    # 2. Scaffold the project
    print("\n[Step 1/3] Running 'nexus scaffold'...")
    cmd_scaffold = f"nexus scaffold -f {tree_file} -o {TEST_DIR} --yes --json"
    if os.system(cmd_scaffold) != 0 or not (TEST_DIR / "api_project/src/main.py").exists():
        print("❌ Scaffold FAILED")
        return False

    # Navigate into the newly scaffolded project
    os.chdir(TEST_DIR / "api_project")

    # 3. Initialize the project
    print("\n[Step 2/3] Running 'nexus init'...")
    cmd_init = "nexus init --yes"
    if os.system(cmd_init) != 0 or not Path("nexus.json").exists():
        print("❌ Init FAILED")
        return False

    # 4. Scan the project
    print("\n[Step 3/3] Running 'nexus scan'...")
    cmd_scan = "nexus scan -o NEXUS_REPORT.md"
    if os.system(cmd_scan) != 0 or not Path("NEXUS_REPORT.md").exists():
        print("❌ Scan FAILED")
        return False

    # Return to base directory
    os.chdir(BASE_DIR)
    print("\n✅ ROUTE A (New Project Workflow): PASSED")
    return True

def test_route_b_legacy_project():
    """
    ROUTE B: The 'Legacy' User
    Workflow: (Pre-existing files) -> nexus init -> nexus scan
    """
    print("\n" + "="*50)
    print("🕰️  ROUTE B: EXISTING PROJECT WORKFLOW")
    print("="*50)

    legacy_dir = TEST_DIR / "legacy_app"
    legacy_dir.mkdir()
    
    # 1. Simulate a user who already has files (e.g., a Node.js / Data project)
    print("\n[Setup] Creating pre-existing files (app.js, styles.css, users.csv)...")
    (legacy_dir / "app.js").write_text("console.log('Hello Legacy');", encoding="utf-8")
    (legacy_dir / "styles.css").write_text("body { color: red; }", encoding="utf-8")
    (legacy_dir / "users.csv").write_text("id,name\n1,Laura\n2,Nexus", encoding="utf-8")

    # Navigate into the legacy project
    os.chdir(legacy_dir)

    # 2. Initialize the project (Should automatically detect js, css, csv)
    print("\n[Step 1/2] Running 'nexus init'...")
    cmd_init = "nexus init --yes"
    if os.system(cmd_init) != 0 or not Path("nexus.json").exists():
        print("❌ Init FAILED")
        return False

    # Validate that init detected the correct legacy extensions
    with open("nexus.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        exts = data.get("translators", {})
        if "js" not in exts or "csv" not in exts:
            print("❌ Init FAILED: Did not detect legacy extensions correctly.")
            return False

    # 3. Scan the project
    print("\n[Step 2/2] Running 'nexus scan'...")
    cmd_scan = "nexus scan -o CONTEXT.md"
    if os.system(cmd_scan) != 0 or not Path("CONTEXT.md").exists():
        print("❌ Scan FAILED")
        return False

    # Return to base directory
    os.chdir(BASE_DIR)
    print("\n✅ ROUTE B (Legacy Project Workflow): PASSED")
    return True

def main():
    print("🧪 STARTING COMPREHENSIVE E2E TEST SUITE...\n")
    setup_environment()
    
    route_a_success = test_route_a_new_project()
    route_b_success = test_route_b_legacy_project()
    
    print("\n" + "="*50)
    if route_a_success and route_b_success:
        print("🏆 ALL ROUTES PASSED! YOUR CLI IS PRODUCTION-READY.")
    else:
        print("💥 SOME TESTS FAILED. CHECK THE LOGS ABOVE.")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()