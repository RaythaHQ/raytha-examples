#!/usr/bin/env bash
# Scan the repository (or the paths given) for things that must not be committed:
# API keys and tokens, passwords, private keys, connection strings, JWTs, local admin URLs and real-looking emails.
# Exits 1 if anything is found. Fictional addresses on example.com/.org/.net and the reserved .example TLD are allowed.
#
#   bash scripts/scan-secrets.sh            # whole repo
#   bash scripts/scan-secrets.sh my-example # one folder
#   EXTRA_PATTERNS_FILE=... bash scripts/scan-secrets.sh   # one extra literal per line (e.g. your real key), never committed
set -uo pipefail
cd "$(dirname "$0")/.."
paths=("${@:-.}")
found=0
grep_args=(-rInE --exclude-dir=.git --exclude=scan-secrets.sh --binary-files=without-match)
check() {
  local label="$1" pattern="$2" out
  out=$(grep "${grep_args[@]}" -- "$pattern" "${paths[@]}" 2>/dev/null)
  if [[ -n "$out" ]]; then echo "== $label"; echo "$out" | cut -c1-200; found=1; fi
}
check "Private key"            '-----BEGIN [A-Z ]*PRIVATE KEY-----'
check "AWS access key"         'AKIA[0-9A-Z]{16}'
check "GitHub token"           'gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}'
check "Slack token"            'xox[abprs]-[A-Za-z0-9-]{10,}'
check "Generic API key"        '(api[_-]?key|apikey|secret|token)["'"'"' ]*[:=] *["'"'"'][A-Za-z0-9_\-]{20,}["'"'"']'
check "Raytha API key in env"  'RAYTHA_API_KEY=[A-Za-z0-9_\-]{12,}'
check "Password assignment"    '(password|passwd|pwd)["'"'"' ]*[:=] *["'"'"'][^"'"'"' ]{6,}["'"'"']'
check "Connection string"      '(Host|Server|Data Source)=[^;"]+;[^"]*(Password|Pwd)=|postgres(ql)?://[^ "]*:[^ "]*@|mongodb(\+srv)?://[^ "]*:[^ "]*@'
check "JWT"                    'eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}'
check "Azure SAS signature"    '[?&]sig=[A-Za-z0-9%+/=]{20,}'
check "Local instance URL"     'https?://(localhost|127\.0\.0\.1|0\.0\.0\.0):[0-9]{2,5}/raytha'
emails=$(grep "${grep_args[@]}" -oh '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' "${paths[@]}" 2>/dev/null \
  | grep -viE '@(example\.(com|org|net)|[a-z0-9.-]+\.example|raytha\.com|users\.noreply\.github\.com)$' \
  | grep -vE '@[0-9]+(\.[0-9]+)*\.[a-z]+$|@(2x|3x)\.' | sort -u)
if [[ -n "$emails" ]]; then echo "== Email addresses (not example.com)"; echo "$emails"; found=1; fi
if [[ -n "${EXTRA_PATTERNS_FILE:-}" && -f "$EXTRA_PATTERNS_FILE" ]]; then
  out=$(grep "${grep_args[@]}" -F -f "$EXTRA_PATTERNS_FILE" "${paths[@]}" 2>/dev/null)
  if [[ -n "$out" ]]; then echo "== Matches from EXTRA_PATTERNS_FILE"; echo "$out" | cut -c1-120; found=1; fi
fi
if [[ $found -eq 0 ]]; then echo "No secrets found."; fi
exit $found
