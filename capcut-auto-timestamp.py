#!/usr/bin/env python3
"""
CapCut → YouTube Chapter Extractor
Automatically finds CapCut draft_content.json and generates formatted chapter timestamps.
"""

import os, sys, json, math

# Try optional import of psutil
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

TARGET_COLOR = "#00c1cd"

def fmt(us):
    s = int(us // 1_000_000)
    h = s // 3600
    m = (s % 3600) // 60
    sec = s % 60
    return f"{h:02d}:{m:02d}:{sec:02d}"

def collect_materials(o, mats):
    if isinstance(o, dict):
        if o.get("id") and isinstance(o.get("mark_items") or o.get("markItems") or o.get("time_marks"), list):
            mats[o["id"]] = o
        for v in o.values():
            collect_materials(v, mats)
    elif isinstance(o, list):
        for e in o:
            collect_materials(e, mats)

def get_latest_project_folder(base_path):
    """Return name of the most recently modified CapCut project folder."""
    try:
        subdirs = [os.path.join(base_path, d) for d in os.listdir(base_path)
                   if os.path.isdir(os.path.join(base_path, d))]
        if not subdirs:
            return None
        latest = max(subdirs, key=os.path.getmtime)
        return os.path.basename(latest)
    except Exception:
        return None

def is_capcut_running():
    """Check if CapCut.exe is running."""
    if not PSUTIL_AVAILABLE:
        return False
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and "CapCut" in proc.info['name']:
            return True
    return False

def process_capcut_json(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        doc = json.load(f)

    materials = {}
    collect_materials(doc.get("materials", {}), materials)

    segments = []
    for tr in doc.get("tracks", []):
        for s in tr.get("segments", []):
            segments.append(s)

    by_material = {}
    for s in segments:
        mid = s.get("material_id") or s.get("materialId")
        if mid:
            by_material.setdefault(mid, []).append(s)

    project_map = {}
    for mid, mat in materials.items():
        marks = mat.get("mark_items") or mat.get("markItems") or mat.get("time_marks") or []
        for mk in marks:
            if (mk.get("color") or "").lower() != TARGET_COLOR:
                continue
            title = mk.get("title") or mk.get("name") or "unknown"
            tr = mk.get("time_range") or mk.get("timeRange") or {}
            m_start = tr.get("start") if isinstance(tr, dict) else mk.get("time")
            if m_start is None:
                continue
            m_start = int(m_start)
            segs = list(by_material.get(mid, []))
            for s in segments:
                refs = s.get("extra_material_refs") or []
                if isinstance(refs, list) and mid in refs and s not in segs:
                    segs.append(s)
            for s in segs:
                src = s.get("source_timerange") or s.get("material_timerange") or {}
                src_start = int(src.get("start", 0))
                src_dur = int(src.get("duration", 0))
                if not (src_start <= m_start <= src_start + src_dur):
                    continue
                targ = s.get("target_timerange") or {}
                targ_start = int(targ.get("start", 0))
                proj_us = targ_start + (m_start - src_start)
                proj_dur = doc.get("duration")
                if proj_dur and not (0 <= proj_us <= int(proj_dur)):
                    continue
                prev = project_map.get(title)
                if prev is None or proj_us < prev:
                    project_map[title] = proj_us

    # Build output list
    output = [(0, "Einleitung")]  # Always add introduction
    for t, us in project_map.items():
        output.append((us, t))
    output.sort(key=lambda x: x[0])

    out_lines = ["Timecodes:"]
    for us, title in output:
        out_lines.append(f"{fmt(us)} - {title}")
    return "\n".join(out_lines)

def main():
    user_profile = os.getenv("USERPROFILE")
    capcut_base = os.path.join(user_profile, "AppData", "Local", "CapCut", "User Data", "Projects", "com.lveditor.draft")

    print("🟢 CapCut Auto Timestamp")
    print("------------------------")

    detected_project = None
    if PSUTIL_AVAILABLE and is_capcut_running():
        detected_project = get_latest_project_folder(capcut_base)
        if detected_project:
            print(f"Detected open project: {detected_project}")
    else:
        if not PSUTIL_AVAILABLE:
            print("⚠️ psutil not installed → skipping auto-detect.")
            print("   To enable this feature later, run:")
            print("   pip install psutil")

    project_name = input(f"Enter CapCut project name [{detected_project or 'None'}]: ").strip() or detected_project
    if not project_name:
        print("❌ No project name provided.")
        return

    json_path = os.path.join(capcut_base, project_name, "draft_content.json")
    if not os.path.exists(json_path):
        print(f"❌ draft_content.json not found:\n{json_path}")
        return

    print(f"📁 Processing project: {project_name}...")
    result = process_capcut_json(json_path)

    output_path = os.path.join(os.path.dirname(__file__), "YouTube_Chapters.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"\n✅ Done! Exported to:\n{output_path}")
    print("\nPreview:\n")
    print(result)
    input("\nPress ENTER to close...")

if __name__ == "__main__":
    main()