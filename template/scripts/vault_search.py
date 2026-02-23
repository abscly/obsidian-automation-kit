"""
🔍 Vault Semantic Search (Gemini Embedding)

Build a search index and perform natural language search
across your Obsidian vault using Gemini Embeddings.

Usage:
  python vault_search.py --build     # Build/update index
  python vault_search.py --search "query"  # Search
"""

import json
import sys
from pathlib import Path

VAULT_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = Path(__file__).parent
INDEX_DIR = SCRIPTS_DIR / ".search_index"
INDEX_PATH = INDEX_DIR / "index.json"
CONFIG_PATH = SCRIPTS_DIR / "config.json"
IGNORE_DIRS = {".git", ".obsidian", "node_modules", "__pycache__", "scripts", ".github", "exports"}


def load_config():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {}


def get_all_notes():
    """Get all markdown files"""
    notes = []
    for md in VAULT_DIR.rglob("*.md"):
        if any(part in IGNORE_DIRS for part in md.parts):
            continue
        notes.append(md)
    return notes


def build_index():
    """Build search index using Gemini Embeddings"""
    config = load_config()
    api_key = config.get("gemini_api_key", "")
    
    if not api_key:
        print("  ⚠️ Gemini API key required for semantic search")
        return False
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
    except ImportError:
        print("  ⚠️ google-generativeai not installed")
        return False
    
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    
    notes = get_all_notes()
    print(f"  📊 Indexing {len(notes)} notes...")
    
    # Load existing index
    existing = {}
    if INDEX_PATH.exists():
        existing = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    
    index = {}
    updated = 0
    
    for note in notes:
        rel_path = str(note.relative_to(VAULT_DIR))
        mtime = note.stat().st_mtime
        
        # Skip if not modified
        if rel_path in existing and existing[rel_path].get("mtime") == mtime:
            index[rel_path] = existing[rel_path]
            continue
        
        content = note.read_text(encoding="utf-8", errors="ignore")
        # Truncate to avoid token limits
        content_trimmed = content[:2000]
        
        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content=content_trimmed,
                task_type="retrieval_document"
            )
            index[rel_path] = {
                "name": note.stem,
                "embedding": result["embedding"],
                "mtime": mtime,
                "preview": content[:200].replace("\n", " ")
            }
            updated += 1
        except Exception as e:
            print(f"  ⚠️ Failed to embed {note.stem}: {e}")
            if rel_path in existing:
                index[rel_path] = existing[rel_path]
    
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    print(f"  ✅ Index built: {len(index)} notes ({updated} updated)")
    return True


def search(query, top_k=5):
    """Search the vault using natural language"""
    config = load_config()
    api_key = config.get("gemini_api_key", "")
    
    if not api_key:
        print("  ⚠️ Gemini API key required")
        return []
    
    if not INDEX_PATH.exists():
        print("  ⚠️ Search index not found. Run: python vault_search.py --build")
        return []
    
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    
    # Embed query
    result = genai.embed_content(
        model="models/embedding-001",
        content=query,
        task_type="retrieval_query"
    )
    query_embedding = result["embedding"]
    
    # Load index
    index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    
    # Compute similarities
    import math
    
    def cosine_sim(a, b):
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0
    
    scores = []
    for path, data in index.items():
        if "embedding" in data:
            sim = cosine_sim(query_embedding, data["embedding"])
            scores.append((sim, path, data))
    
    scores.sort(reverse=True)
    
    print(f"\n🔍 Search results for: \"{query}\"\n")
    for score, path, data in scores[:top_k]:
        print(f"  📄 {data['name']} ({score:.3f})")
        print(f"     {data.get('preview', '')[:80]}...")
        print()
    
    return scores[:top_k]


def main():
    if "--build" in sys.argv:
        build_index()
    elif "--search" in sys.argv:
        idx = sys.argv.index("--search")
        if idx + 1 < len(sys.argv):
            search(sys.argv[idx + 1])
        else:
            print("Usage: python vault_search.py --search \"query\"")
    else:
        print("Usage:")
        print("  python vault_search.py --build          # Build index")
        print("  python vault_search.py --search \"query\" # Search")


if __name__ == "__main__":
    main()
