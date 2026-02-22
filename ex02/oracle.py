#!/usr/bin/env python3
"""
ex02 - oracle.py
Loads configuration using environment variables and .env (python-dotenv).
Authorized: os, sys, python-dotenv modules, file operations
"""

import os

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None


REQUIRED_KEYS = (
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
)


def _env_paths() -> tuple[str, str]:
    """
    Return absolute paths for .env and .env.example inside ex02 directory,
    regardless of current working directory.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(base_dir, ".env")
    example_path = os.path.join(base_dir, ".env.example")
    return env_path, example_path


def load_config() -> bool:
    """
    Load .env if python-dotenv exists.
    Environment variables override values from .env automatically because
    load_dotenv does not overwrite existing variables by default.
    Returns True if .env exists, False otherwise.
    """
    env_path, _ = _env_paths()
    env_exists = os.path.exists(env_path)

    if load_dotenv is None:
        return env_exists

    if env_exists:
        load_dotenv(env_path)  # override=False by default

    return env_exists


def mask_secret(value: str) -> str:
    """Mask secret for display."""
    if not value:
        return ""
    if len(value) <= 4:
        return "*" * len(value)
    return value[:2] + "*" * (len(value) - 4) + value[-2:]


def main() -> None:
    print("ORACLE STATUS: Reading the Matrix...")
    print()

    env_path, example_path = _env_paths()

    if load_dotenv is None:
        print("[WARNING] python-dotenv is not installed.")
        print("Install it with:")
        print("  pip install python-dotenv")
        print("or (Poetry):")
        print("  poetry add python-dotenv")
        print("Continuing with OS environment variables only...")
        print()

    env_exists = load_config()

    print("Configuration loaded:")
    mode = os.environ.get("MATRIX_MODE", "development")
    db = os.environ.get("DATABASE_URL", "")
    api_key = os.environ.get("API_KEY", "")
    log_level = os.environ.get("LOG_LEVEL", "INFO")
    zion = os.environ.get("ZION_ENDPOINT", "")

    print(f"Mode: {mode}")

    if db:
        print("Database: Connected to local instance")
    else:
        print("Database: Missing DATABASE_URL")

    if api_key:
        print("API Access: Authenticated")
    else:
        print("API Access: Missing API_KEY")

    print(f"Log Level: {log_level}")

    if zion:
        print("Zion Network: Online")
    else:
        print("Zion Network: Missing ZION_ENDPOINT")

    print()
    print("Environment security check:")

    if api_key:
        print(f"[OK] API_KEY masked: {mask_secret(api_key)}")
    else:
        print("[WARN] API_KEY not set (use .env.example as a template)")

    if env_exists:
        print("[OK] .env file detected")
    else:
        print("[WARN] .env not found (create it from .env.example)")

    if os.path.exists(example_path):
        print("[OK] .env.example present")
    else:
        print("[WARN] .env.example missing")

    missing = [k for k in REQUIRED_KEYS if not os.environ.get(k)]
    if missing:
        print("[WARN] Missing configuration keys:")
        for key in missing:
            print(f"- {key}")
    else:
        print("[OK] All required keys configured")

    print()
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()
