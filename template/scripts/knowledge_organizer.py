"""
📚 Knowledge Organizer

Organizes Knowledge notes by detecting topics, suggesting tags,
and maintaining the Knowledge directory structure.

Usage:
  python knowledge_organizer.py
"""

import re
from pathlib import Path
from collections import Counter

VAULT_DIR = Path(__file__).parent.parent
KNOWLEDGE_DIR = VAULT_DIR / "Knowledge"


def scan_knowledge():
    """Scan and organize Knowledge directory"""
    print("📚 Knowledge Organizer")
    
    if not KNOWLEDGE_DIR.exists():
        KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
        print("  📁 Created Knowledge directory")
        return True
    
    notes = list(KNOWLEDGE_DIR.rglob("*.md"))
    print(f"  📊 Knowledge notes: {len(notes)}")
    
    untagged = []
    topics = Counter()
    
    for note in notes:
        content = note.read_text(encoding="utf-8", errors="ignore")
        
        # Check for tags
        tags = re.findall(r'#([a-zA-Z0-9_/\-\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff]+)', content)
        if not tags:
            untagged.append(note.stem)
        
        # Extract topics from tech tags
        for tag in tags:
            if tag.startswith("tech/"):
                topics[tag] += 1
            elif tag.startswith("type/"):
                topics[tag] += 1
    
    if untagged:
        print(f"  🏷️ Untagged notes: {len(untagged)}")
        for name in untagged[:5]:
            print(f"    📄 {name}")
    
    if topics:
        print(f"  📊 Top topics:")
        for topic, count in topics.most_common(5):
            print(f"    #{topic}: {count}")
    
    return True


def main():
    return scan_knowledge()


if __name__ == "__main__":
    main()
