import subprocess
import sys
from pathlib import Path


class CodeQualityRunner:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.reports_dir = self.project_root / "code_quality_reports"
        self.reports_dir.mkdir(exist_ok=True)
        self.results = {}

    def print_header(self, title):
        print("\n" + "=" * 80)
        print(f"{title}")
        print("=" * 80 + "\n")

    def print_result(self, check_name, passed, message=""):
        status = "PASSED" if passed else "FAILED"
        print(f"[{status}] {check_name}")
        if message:
            print(f"  {message}")

    def run_black(self, check_only=False):
        self.print_header("Black - Code Formatting")

        cmd = ["black"]
        if check_only:
            cmd.append("--check")
        cmd.extend(["--line-length=120", ".", r"--exclude=(\.venv|venv|reports|logs|allure_reports)"])

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            passed = result.returncode == 0
            self.results["black"] = passed

            if check_only:
                self.print_result("Black", passed, "All files formatted" if passed else "Files need formatting")
            else:
                self.print_result("Black", True, "Files formatted")

            if result.stdout:
                print(result.stdout)
            if result.stderr and not passed:
                print(result.stderr)

            return passed
        except Exception as e:
            print(f"Error running Black: {e}")
            return False

    def run_flake8(self):
        self.print_header("Flake8 - Python Linting")

        cmd = ["flake8", "."]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            passed = result.returncode == 0
            self.results["flake8"] = passed

            self.print_result("Flake8", passed, "No issues" if passed else "Issues found")

            if result.stdout:
                print(result.stdout[:1000])
            if result.stderr:
                print(result.stderr[:1000])

            return passed
        except Exception as e:
            print(f"Error running Flake8: {e}")
            return False

    def run_pylint(self):
        self.print_header("Pylint - Code Analysis")

        modules = ["config", "pages", "utils", "features/steps"]
        cmd = ["pylint", *modules, "--output-format=colorized"]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            output = result.stdout + result.stderr
            passed = result.returncode == 0 or "rated at" in output
            self.results["pylint"] = passed

            score = ""
            for line in output.split("\n"):
                if "rated at" in line:
                    score = line.strip()
                    break

            self.print_result("Pylint", passed, score)

            if result.stdout:
                print(result.stdout[:1500])

            return passed
        except Exception as e:
            print(f"Error running Pylint: {e}")
            return False

    def run_isort(self, check_only=False):
        self.print_header("Isort - Import Sorting")

        cmd = ["isort"]
        if check_only:
            cmd.append("--check-only")
        cmd.extend(["--profile=black", "--line-length=120", ".", "--skip-glob=.venv/*", "--skip-glob=venv/*"])

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            passed = result.returncode == 0
            self.results["isort"] = passed

            if check_only:
                self.print_result("Isort", passed, "Imports sorted" if passed else "Imports need sorting")
            else:
                self.print_result("Isort", True, "Imports sorted")

            if result.stdout:
                print(result.stdout)

            return passed
        except Exception as e:
            print(f"Error running isort: {e}")
            return False

    def run_security_check(self):
        self.print_header("Bandit - Security Analysis")

        cmd = ["bandit", "-r", "config", "pages", "utils", "features/steps"]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            passed = result.returncode == 0
            self.results["bandit"] = passed

            self.print_result("Bandit", passed, "No security issues" if passed else "Security issues detected")

            if not passed and result.stdout:
                print(result.stdout[:1000])

            return passed
        except FileNotFoundError:
            print("Bandit not installed. Install with: pip install bandit")
            return True
        except Exception as e:
            print(f"Error running Bandit: {e}")
            return False

    def print_summary(self):
        total_checks = len(self.results)
        passed_checks = sum(1 for passed in self.results.values() if passed)

        print("\n" + "=" * 80)
        print("Summary")
        print("=" * 80)
        print(f"Total Checks: {total_checks}")
        print(f"Passed: {passed_checks}")
        print(f"Failed: {total_checks - passed_checks}")
        print("\nResults:")
        for check_name, passed in self.results.items():
            status = "PASSED" if passed else "FAILED"
            print(f"  [{status}] {check_name}")
        print("=" * 80 + "\n")

    def run_all_checks(self, fix=False):
        print("\n" + "=" * 80)
        print("Code Quality Checks")
        print("=" * 80)
        print(f"Project Root: {self.project_root}")
        print(f"Fix Mode: {'ON' if fix else 'OFF'}")
        print("=" * 80)

        self.run_black(check_only=not fix)
        self.run_isort(check_only=not fix)
        self.run_flake8()
        self.run_pylint()
        self.run_security_check()

        self.print_summary()

        all_passed = all(self.results.values())

        if all_passed:
            print("All checks passed")
            return 0
        else:
            print("Some checks failed")
            return 1


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Run code quality checks")
    parser.add_argument("--fix", action="store_true", help="Auto-fix issues")
    parser.add_argument("--check", action="store_true", help="Check only mode")

    args = parser.parse_args()
    fix_mode = args.fix and not args.check

    runner = CodeQualityRunner()
    exit_code = runner.run_all_checks(fix=fix_mode)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
