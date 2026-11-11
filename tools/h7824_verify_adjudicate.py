#!/usr/bin/env python3
"""H7824 close adjudication: DeepSeek cross-family verifier over the merged PR diff.

Sends the acceptance criteria (from the handoff) + the merged diff + grep-proof
to deepseek-chat and prints a one-line verdict for handoff_close --verifier-*.
"""
import json
import subprocess
import sys
import urllib.request

AUTH = "/Users/mac/.local/share/opencode/auth.json"
PR_URL = "https://github.com/gasyoun/SanskritGrammar/pull/1166"


def deepseek_key():
    auth = json.load(open(AUTH))
    for provider, v in auth.items():
        v = v or {}
        tok = v.get("access_token") or v.get("key") or v.get("token")
        if tok and "deepseek" in str(provider).lower():
            return tok
    return None


def gh(path):
    return subprocess.run(["gh", "api", path], capture_output=True, text=True, check=True).stdout


def main():
    diff = gh(f"repos/gasyoun/SanskritGrammar/pulls/1166")
    meta = json.loads(diff)
    files = gh("repos/gasyoun/SanskritGrammar/pulls/1166/files?per_page=10")
    fdata = json.loads(files)
    file_patches = []
    for f in fdata:
        file_patches.append(f"--- {f['filename']} (+{f['additions']}/-{f['deletions']}) ---\n{f.get('patch', '(no patch)')[:14000]}")
    prompt = f"""Ты — кросс-семейный верификатор закрытия хендоффа H7824 (плейбук разбора ДЗ Кочергиной, расширение до v2). Исполнитель — GLM 5.3 (другая семья). Проверь НЕЗАВИСИМО по критериям приёмки и вынеси вердикт.

КРИТЕРИИ ПРИЁМКИ (из хендоффа H7824):
1. Файл KocherginaUchebnik_1998/PLAYBOOK_KOCHERGINA_EXERCISE_PARSE_2026-11-07.md на origin/main несёт v2-слои: шаги 4a/4b/4c (согласование/управление/члены предложения), словообразовательный кейс-инвентарь (ОТДЕЛЬНЫЙ шаг — вето Q3), шаг корпусной пробы DCS, секции «Методические призмы» (ссылочник) и «Генераторы вопросов» №1–6.
2. Регресс: таблицы/вердикты кейсов 1–3 НЕ переписываются — новые слои только добавляются.
3. Анти-энциклопедизация: рост < 2× длины v1 (215 строк) без нового кейса.
4. meta-файл и changelog-фрагмент обновлены тем же PR.

МАШИННЫЕ ФАКТЫ (проверены на origin/main после squash-merge 865d272):
- PR {PR_URL} — state MERGED (squash), merged 2026-11-08T07:55:29Z.
- git show origin/main:...PLAYBOOK...2026-11-07.md | grep -cE "4b|Генераторы вопросов|Методические призмы" = 8 (порог ≥ 3).
- Файл на origin/main: 314 строк (v1 = 215; 314 < 2×215=430).
- Строк, удалённых из таблиц кейсов 1–3 в диффе: 0 (удалены только шапка-строки и старые формулировки шагов 3–6, текст шага 4-согласования сохранён дословно внутри 4a; шаги errata/перевод перенумерованы 5→7, 6→8 с сохранением текста).

ДИФФ PR (patch-фрагменты):
{chr(10).join(file_patches)}

Отвечай СТРОГО одной строкой JSON: {{"verdict": "pass" | "fail", "reason": "<до 200 символов>"}} — verdict=pass только если ВСЕ 4 критерия выполнены по предоставленным фактам и диффу; иначе fail с причиной."""
    body = json.dumps({
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": 300,
    }).encode()
    req = urllib.request.Request(
        "https://api.deepseek.com/chat/completions", data=body,
        headers={"Authorization": f"Bearer {deepseek_key()}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        out = json.load(r)
    print(out["choices"][0]["message"]["content"].strip())


if __name__ == "__main__":
    sys.exit(main())
