"""
🏥 Vault Health Check

Diagnose and report on the health of your Obsidian vault.
Detects broken links, orphan notes, missing tags, and more.

Usage:
  python vault_health.py
"""

import re
from pathlib import Path
from collections import Counter

VAULT_DIR = Path(__file__).parent.parent
IGNORE_DIRS = {".git", ".obsidian", "node_modules", "__pycache__", "scripts", ".github", "exports"}


def get_all_notes():
    """Get all markdown files in the vault"""
    notes = {}
    for md in VAULT_DIR.rglob("*.md"):
        if any(part in IGNORE_DIRS for part in md.parts):
            continue
        rel = md.relative_to(VAULT_DIR)
        notes[md.stem] = {"path": rel, "full_path": md}
    return notes


def extract_links(content):
    """Extract [[wiki links]] from content"""
    return re.findall(r'\[\[([^\]|#]+?)(?:\|[^\]]*?)?\]\]', content)


def extract_tags(content):
    """Extract #tags from content"""
    return re.findall(r'#([a-zA-Z0-9_/\-\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff]+)', content)


def check_health():
    """Run full health check"""
    print("🏥 Vault Health Check")
    print("=" * 50)
    
    notes = get_all_notes()
    print(f"\n📊 Total notes: {len(notes)}")
    
    all_links = {}
    all_tags = Counter()
    broken_links = []
    orphan_notes = set(notes.keys())
    notes_without_tags = []
    empty_notes = []
    
    for name, info in notes.items():
        content = info["full_path"].read_text(encoding="utf-8", errors="ignore")
        
        # Check links
        links = extract_links(content)
        all_links[name] = links
        for link in links:
            link_base = link.split("/")[-1]
            if link_base not in notes and link_base not in [d.name for d in VAULT_DIR.iterdir() if d.is_dir()]:
                broken_links.append({"from": name, "to": link})
            if link_base in orphan_notes:
                orphan_notes.discard(link_base)
        
        # Track referencing notes
        if name in orphan_notes and links:
            pass  # Will be removed if referenced
        
        # Check tags
        tags = extract_tags(content)
        all_tags.update(tags)
        if not tags:
            notes_without_tags.append(name)
        
        # Check empty
        content_lines = [l.strip() for l in content.split("\n") if l.strip() and not l.startswith("---") and not l.startswith("#")]
        if len(content_lines) < 2:
            empty_notes.append(name)
    
    # Remove Home and templates from orphans
    for special in ["Home", "Daily テンプレート", "Weekly テンプレート", "Project テンプレート", "Quick Capture"]:
        orphan_notes.discard(special)
    
    # Report
    print(f"\n🔗 Broken Links: {len(broken_links)}")
    for bl in broken_links[:10]:
        print(f"  ❌ {bl['from']} → [[{bl['to']}]]")
    if len(broken_links) > 10:
        print(f"  ... and {len(broken_links) - 10} more")
    
    print(f"\n🏝️ Orphan Notes (not linked anywhere): {len(orphan_notes)}")
    for orphan in sorted(orphan_notes)[:10]:
        print(f"  📄 {orphan}")
    if len(orphan_notes) > 10:
        print(f"  ... and {len(orphan_notes) - 10} more")
    
    print(f"\n🏷️ Notes without tags: {len(notes_without_tags)}")
    for nt in notes_without_tags[:5]:
        print(f"  📄 {nt}")
    
    print(f"\n📭 Nearly empty notes: {len(empty_notes)}")
    for en in empty_notes[:5]:
        print(f"  📄 {en}")
    
    print(f"\n🏷️ Top tags:")
    for tag, count in all_tags.most_common(10):
        print(f"  #{tag}: {count}")
    
    # Health score
    total = len(notes)
    if total == 0:
        score = 100
    else:
        issues = len(broken_links) + len(orphan_notes) + len(empty_notes)
        score = max(0, 100 - (issues / total * 100))
    
    print(f"\n{'='*50}")
    print(f"🏥 Health Score: {score:.0f}/100")
    
    if score >= 90:
        print("  🟢 Excellent! Your vault is very healthy.")
    elif score >= 70:
        print("  🟡 Good. Some maintenance recommended.")
    elif score >= 50:
        print("  🟠 Fair. Consider fixing broken links and organizing orphans.")
    else:
        print("  🔴 Needs attention. Many issues detected.")
    
    return {
        "total_notes": total,
        "broken_links": len(broken_links),
        "orphan_notes": len(orphan_notes),
        "empty_notes": len(empty_notes),
        "health_score": score
    }


def main():
    return check_health()


if __name__ == "__main__":
    main()
