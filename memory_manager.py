import json, os, uuid, datetime

MEMORY_FILE = "mentor_memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:  # empty file
                return []
            return json.loads(content)
    except (json.JSONDecodeError, ValueError):
        print("⚠️ Memory file corrupted or empty JSON. Resetting it.")
        return []
    except Exception as e:
        print(f"⚠️ Unexpected error while loading memory: {e}")
        return []

def save_memory(memories):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memories, f, indent=2)

def create_memory_entry(problem_title, user_code, outcome, error_patterns, notes):
    memories = load_memory()
    memory_id = str(uuid.uuid4())[:8]
    entry = {
        "memory_id": memory_id,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "problem_title": problem_title,
        "user_code": user_code[:500],  # avoid huge payloads
        "outcome": outcome,
        "error_patterns": error_patterns,
        "notes": notes,
        "fix_attempts": 1
    }
    memories.append(entry)
    save_memory(memories)
    return memory_id

def update_memory_entry(memory_id, new_error_patterns=None, new_notes=None):
    memories = load_memory()
    for m in memories:
        if m["memory_id"] == memory_id:
            if new_error_patterns:
                m["error_patterns"] = list(set(m["error_patterns"] + new_error_patterns))
            if new_notes:
                m["notes"] = (m.get("notes", "") + "\n" + new_notes).strip()
            m["fix_attempts"] = m.get("fix_attempts", 0) + 1
            m["timestamp"] = datetime.datetime.utcnow().isoformat()
    save_memory(memories)
    return True

def search_similar(problem_title, keywords):
    """Naive text search for similar problems / error patterns"""
    memories = load_memory()
    results = []
    for m in memories:
        if problem_title.lower() in m["problem_title"].lower() or any(k in m["error_patterns"] for k in keywords):
            results.append(m)
    return results


def find_existing_memory(problem_title):
    """ Return memory_id if a memory entry for this problem already exists."""
    memories = load_memory()
    for m in memories:
        if m["problem_title"].strip().lower() == problem_title.strip().lower():
            return m["memory_id"]
    return None


