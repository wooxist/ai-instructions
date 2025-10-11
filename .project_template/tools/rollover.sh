#!/usr/bin/env bash
# Maintenance helper for TODO/ROADMAP/Session
# Usage examples:
#   ./.project_template/tools/rollover.sh todo [--week YYYY-WW] [--archive-dir .work/archive/todo]
#   ./.project_template/tools/rollover.sh sessions [--days 14] [--dest .session/archive]
#   ./.project_template/tools/rollover.sh roadmap [--dest .work/roadmap]
#   ./.project_template/tools/rollover.sh check

set -euo pipefail

OS_IS_DARWIN=false
[[ "$OSTYPE" == darwin* ]] && OS_IS_DARWIN=true

ROOT_DIR=$(pwd)

die() { echo "[error] $*" >&2; exit 1; }
info() { echo "[info]  $*"; }

usage() {
  cat << EOF
rollover.sh <command> [options]

Commands
  todo        Archive completed items from .work/TODO.md into weekly files
  sessions    Move old .session/*.md into monthly archives and build INDEX
  roadmap     Split ROADMAP.md phases into .work/roadmap/phase-XX.md
  check       Show size/line counts and simple recommendations

Examples
  ./.project_template/tools/rollover.sh todo
  ./.project_template/tools/rollover.sh sessions --days 14
  ./.project_template/tools/rollover.sh roadmap
EOF
}

ensure_paths() {
  [[ -f "$ROOT_DIR/.work/TODO.md" ]] || info "(note) .work/TODO.md not found; some commands may be skipped"
  [[ -f "$ROOT_DIR/ROADMAP.md" ]] || info "(note) ROADMAP.md not found; roadmap split will be skipped"
  mkdir -p "$ROOT_DIR/.work/archive/todo" "$ROOT_DIR/.session/archive" "$ROOT_DIR/.work/roadmap"
}

iso_week() {
  if $OS_IS_DARWIN; then date +%G-W%V; else date +%G-W%V; fi
}

today() {
  if $OS_IS_DARWIN; then date +%Y-%m-%d; else date +%Y-%m-%d; fi
}

month_from_date() {
  # input: YYYY-MM-DD
  local d="$1"
  echo "${d:0:7}"
}

cmd_todo() {
  local week="$(iso_week)"
  local archive_dir=".work/archive/todo"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --week) week="$2"; shift 2 ;;
      --archive-dir) archive_dir="$2"; shift 2 ;;
      *) die "unknown option for todo: $1" ;;
    esac
  done
  [[ -f ".work/TODO.md" ]] || { info "skip: .work/TODO.md not found"; return 0; }
  mkdir -p "$archive_dir"

  local src=".work/TODO.md"
  local tmp=".work/.TODO.tmp"
  local done_file="$archive_dir/$(date +%Y)-${week}-done.md"

  info "Archiving completed tasks from $src to $done_file"

  # Extract '## ✅ 완료된 작업' section
  # Keep only the most recent date block in TODO; archive the full section
  # Identify line numbers for the section
  local start_line end_line
  start_line=$(grep -n "^##[[:space:]]*✅[[:space:]]*완료된 작업" "$src" | head -1 | cut -d: -f1 || true)
  if [[ -z "${start_line:-}" ]]; then
    info "No '완료된 작업' section found; nothing to archive"
    return 0
  fi
  # end_line = next top-level heading or EOF
  end_line=$(awk -v s="$start_line" 'NR>s && /^##[[:space:]]/ {print NR; exit}' "$src")
  [[ -z "$end_line" ]] && end_line=$(wc -l < "$src")

  # Archive full completed section
  sed -n "${start_line},${end_line}p" "$src" > "$done_file"

  # Keep only the first date block within completed section (latest)
  # Build new completed section with just first date block (first '### ' occurrence)
  local first_date_line rel_end
  first_date_line=$(sed -n "${start_line},${end_line}p" "$src" | grep -n "^###[[:space:]][0-9]{4}-[0-9]{2}-[0-9]{2}$" | head -1 | cut -d: -f1 || true)
  # Fallback: if regex class not supported in grep on some shells, match YYYY-
  if [[ -z "$first_date_line" ]]; then
    first_date_line=$(sed -n "${start_line},${end_line}p" "$src" | grep -n "^###[[:space:]][0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}$" | head -1 | cut -d: -f1 || true)
  fi
  if [[ -z "$first_date_line" ]]; then
    # If no date subsections, leave only the section header
    sed "${start_line},${end_line}d" "$src" > "$tmp"
    { sed -n "1,$((start_line-1))p" "$src"; echo "## ✅ 완료된 작업"; } > "$tmp"
  else
    # Determine end of first date block (next ### or end_line)
    rel_end=$(sed -n "${start_line},${end_line}p" "$src" | awk -v s="$first_date_line" 'NR>s && /^###[[:space:]]/ {print NR; exit}')
    if [[ -z "$rel_end" ]]; then rel_end=$((end_line - start_line + 1)); fi
    # Compose new file: content before section + section header + first date block + content after section
    sed -n "1,$((start_line-1))p" "$src" > "$tmp"
    sed -n "${start_line},$((start_line))p" "$src" >> "$tmp"     # the section header line
    sed -n "$((start_line+first_date_line-1)),$((start_line+rel_end-1))p" "$src" >> "$tmp"
    sed -n "$((end_line+1)),\$p" "$src" >> "$tmp"
  fi

  mv "$tmp" "$src"

  # Update "마지막 업데이트" date if present
  if $OS_IS_DARWIN; then
    sed -i '' "s/^\*\*마지막 업데이트\*\*:.*/**마지막 업데이트**: $(today)/" "$src" || true
  else
    sed -i "s/^\*\*마지막 업데이트\*\*:.*/**마지막 업데이트**: $(today)/" "$src" || true
  fi

  info "TODO rollover complete → archived at $done_file"
}

cmd_sessions() {
  local days=14 dest=".session/archive"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --days) days="$2"; shift 2 ;;
      --dest) dest="$2"; shift 2 ;;
      *) die "unknown option for sessions: $1" ;;
    esac
  done
  [[ -d ".session" ]] || { info "skip: .session not found"; return 0; }
  mkdir -p "$dest"
  info "Archiving session files older than ${days}d into $dest"
  # Find session files YYYY-MM-DD.md not in archive
  shopt -s nullglob
  local moved=0
  for f in .session/*.md; do
    [[ "$f" =~ _template.md$ ]] && continue
    # Skip if under archive already
    [[ "$f" == .session/archive/* ]] && continue
    # Skip if modified within N days
    if [[ $(find "$f" -mtime -$days -print 2>/dev/null) ]]; then continue; fi
    # Determine month folder
    local base=$(basename "$f" .md)
    if [[ ! "$base" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then continue; fi
    local month=$(month_from_date "$base")
    mkdir -p "$dest/$month"
    git mv -f "$f" "$dest/$month/" 2>/dev/null || mv "$f" "$dest/$month/"
    moved=$((moved+1))
  done
  shopt -u nullglob

  # Rebuild INDEX.md with latest 10 sessions (including archived)
  info "Building .session/archive/INDEX.md"
  {
    echo "# Session Index"
    echo ""
    echo "최근 10개 세션 링크:"
    echo ""
    # Collect paths, sort desc
    ls -1 .session/*.md 2>/dev/null; ls -1 .session/archive/*/*.md 2>/dev/null
  } | awk '/^#|^$/{print;next} {print}' > .session/archive/.all.list
  sort -r .session/archive/.all.list | head -10 > .session/archive/.latest.list
  {
    echo "# Session Index"
    echo ""
    echo "최근 10개 세션 링크:"
    echo ""
    while read -r p; do
      # normalize path for markdown link
      echo "- [$(basename "$p" .md)]($p)"
    done < .session/archive/.latest.list
  } > .session/archive/INDEX.md
  rm -f .session/archive/.all.list .session/archive/.latest.list

  info "Session rollover complete (moved: $moved)"
}

cmd_roadmap() {
  local dest=".work/roadmap" rewrite_root=false
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dest) dest="$2"; shift 2 ;;
      --rewrite-root) rewrite_root=true; shift 1 ;;
      *) die "unknown option for roadmap: $1" ;;
    esac
  done
  [[ -f "ROADMAP.md" ]] || { info "skip: ROADMAP.md not found"; return 0; }
  mkdir -p "$dest"
  info "Splitting ROADMAP phases into $dest"

  # Extract Phase sections starting with '### Phase'
  # Generate files phase-XX.md and an index
  local index_file="$dest/index.md"; : > "$index_file"
  echo "# Roadmap Phases" >> "$index_file"
  echo "" >> "$index_file"

  # Phase counter
  local phases
  mapfile -t phases < <(grep -n "^###[[:space:]]*Phase[[:space:]]\([0-9][0-9]*\)\|^###[[:space:]]*Phase" ROADMAP.md | cut -d: -f1)
  if [[ ${#phases[@]} -eq 0 ]]; then
    info "No '### Phase' headings found; nothing to split"
    return 0
  fi
  phases+=( $(wc -l < ROADMAP.md) )

  local i; for ((i=0; i<${#phases[@]}-1; i++)); do
    local start=${phases[$i]}
    local end=${phases[$((i+1))]}
    local block
    block=$(sed -n "${start},$((end-1))p" ROADMAP.md)
    # Determine phase number and name
    local header
    header=$(echo "$block" | head -1)
    local phase_num phase_name
    phase_num=$(echo "$header" | sed -E 's/^###[ ]*Phase[ ]*([0-9]+).*/\1/' )
    [[ -z "$phase_num" ]] && phase_num=$(printf "%02d" $((i+1))) || phase_num=$(printf "%02d" "$phase_num")
    phase_name=$(echo "$header" | sed -E 's/^###[ ]*Phase[ ]*[0-9]+:[ ]*//')
    [[ -z "$phase_name" ]] && phase_name="Phase ${phase_num}"
    local out="$dest/phase-${phase_num}.md"
    echo "$block" > "$out"
    echo "- [Phase ${phase_num} — ${phase_name}]($(basename "$out"))" >> "$index_file"
  done

  info "Generated: $index_file and $(ls -1 $dest/phase-*.md 2>/dev/null | wc -l) phase files"

  if $rewrite_root; then
    info "Rewriting ROADMAP.md to point to phase files (keeping overview)"
    # Keep top part until first phase header; then insert links to index
    local first_phase_line
    first_phase_line=$(grep -n "^###[[:space:]]*Phase" ROADMAP.md | head -1 | cut -d: -f1)
    if [[ -n "$first_phase_line" ]]; then
      {
        sed -n "1,$((first_phase_line-1))p" ROADMAP.md
        echo ""
        echo "## 📅 Phase 문서"
        echo "자세한 Phase 내용은 [.work/roadmap/index.md]($dest/index.md)을 참고하세요."
      } > ROADMAP.md.tmp
      mv ROADMAP.md.tmp ROADMAP.md
    fi
  fi
}

cmd_check() {
  local todo_lines="-" roadmap_lines="-" sessions_count="-"
  [[ -f .work/TODO.md ]] && todo_lines=$(wc -l < .work/TODO.md)
  [[ -f ROADMAP.md ]] && roadmap_lines=$(wc -l < ROADMAP.md)
  sessions_count=$(ls -1 .session/*.md 2>/dev/null | wc -l | tr -d ' ')
  cat << EOF
Health check
- TODO.md lines:    $todo_lines (target <= 200)
- ROADMAP.md lines: $roadmap_lines (target <= 150)
- Sessions active:  $sessions_count (older ones should be archived)
EOF
}

main() {
  local cmd="${1:-}"; shift || true
  [[ -z "$cmd" ]] && { usage; exit 1; }
  ensure_paths
  case "$cmd" in
    todo)     cmd_todo "$@" ;;
    sessions) cmd_sessions "$@" ;;
    roadmap)  cmd_roadmap "$@" ;;
    check)    cmd_check  "$@" ;;
    -h|--help|help) usage ;;
    *) die "unknown command: $cmd" ;;
  esac
}

main "$@"

