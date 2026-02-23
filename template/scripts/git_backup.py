"""
🔄 Git Auto-Backup

Automatically commits and pushes Vault changes to Git.

Usage:
  python git_backup.py
"""

import subprocess
from pathlib import Path
from datetime import datetime

VAULT_DIR = Path(__file__).parent.parent


def run_git(args, cwd=None):
    """Run a git command and return (success, output)"""
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=cwd or str(VAULT_DIR),
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        return False, str(e)


def main():
    """Auto-backup: pull, add, commit, push"""
    print("🔄 Git Auto-Backup")
    
    # Check if git repo exists
    if not (VAULT_DIR / ".git").exists():
        print("  ⚠️ Not a git repository. Initialize with: git init")
        return False
    
    # Pull latest
    ok, out = run_git(["pull", "--rebase", "--autostash"])
    if ok:
        print(f"  📥 Pull: {out or 'up to date'}")
    else:
        print(f"  ⚠️ Pull failed: {out}")
    
    # Check for changes
    ok, status = run_git(["status", "--porcelain"])
    if not status:
        print("  📋 No changes to commit")
        return True
    
    # Count changes
    changes = [l for l in status.split("\n") if l.strip()]
    print(f"  📝 {len(changes)} file(s) changed")
    
    # Add all
    run_git(["add", "-A"])
    
    # Commit
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    msg = f"vault: auto-backup {timestamp} ({len(changes)} files)"
    ok, out = run_git(["commit", "-m", msg])
    if ok:
        print(f"  ✅ Committed: {msg}")
    else:
        print(f"  ⚠️ Commit: {out}")
        return False
    
    # Push
    ok, out = run_git(["push"])
    if ok:
        print("  🚀 Pushed to remote")
    else:
        print(f"  ⚠️ Push failed: {out}")
        print("  💡 Set remote with: git remote add origin <url>")
    
    return True


if __name__ == "__main__":
    main()
