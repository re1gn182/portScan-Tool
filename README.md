# portScannr (check Repo these can work together) & passwdChckr

Small collection of simple security utilities:

- `portScannr/portScanr.py` — Basic TCP port scanner.
- `passwdChckr/PasswordChecker.py` — Password strength and breach checks (HIBP).

## Requirements

- Python 3.8+
- Optional: internet access for HIBP checks in `PasswordChecker`.

## Quick start

1. Create and activate a virtual environment (optional but recommended):

   python3 -m venv .venv
   source .venv/bin/activate

2. Run the port scanner:

   python3 portScannr/portScanr.py <host> [--ports PORTS] [--threads N] [--timeout S]

   Examples:

   - Scan common ports 1-1024 on `example.com`:
     python3 portScannr/portScanr.py example.com

   - Scan specific ports:
     python3 portScannr/portScanr.py 192.0.2.1 --ports 22,80,443

   - Scan a range:
     python3 portScannr/portScanr.py localhost --ports 1-65535 --threads 200 --timeout 0.5

3. Check passwords with `PasswordChecker`:

   python3 passwdChckr/PasswordChecker.py --file passwords.txt [--pwned] [--workers N] [--json out.json]

   - `--file, -f`: path to a file with one password per line.
   - `--pwned`: check each password against Have I Been Pwned (internet required).
   - `--json`: write results (no raw passwords) to the given JSON path.

   Example:
   python3 passwdChckr/PasswordChecker.py --file my_passwords.txt --pwned --json results.json

## Tests

Run the test suite with `pytest` from the repository root:

   pytest

The repository includes `tests/test_passwordchecker.py` covering password checks.

## Notes

- `PasswordChecker` uses the HIBP k-anonymity API and includes retry/backoff logic; expect slower runtimes when `--pwned` is used.
- These tools are intended for learning and small-scale use. Use responsibly and obey applicable network policies when scanning remote hosts.

## Next steps

- Add a `requirements.txt` or `pyproject.toml` if you want pinned dependencies.
- I can run the tests and/or add badges if you want.
