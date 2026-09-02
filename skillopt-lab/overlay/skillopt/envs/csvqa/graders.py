"""Pluggable graders. Each returns (hard: int, soft: float, detail: str)."""
from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation


def extract_answer(text: str) -> str:
    m = re.findall(r"<answer>(.*?)</answer>", text or "", re.DOTALL | re.IGNORECASE)
    if m:
        return m[-1].strip()
    lines = [ln.strip() for ln in (text or "").strip().splitlines() if ln.strip()]
    return lines[-1] if lines else (text or "").strip()


def _norm(s: str) -> str:
    return " ".join((s or "").strip().lower().split())


def grade_exact(pred: str, expected: str) -> tuple[int, float, str]:
    a = _norm(extract_answer(pred))
    e = _norm(expected)
    hard = int(a == e)
    return hard, float(hard), f"pred={a!r} expected={e!r}"


def _to_decimal(s: str) -> Decimal | None:
    s = (s or "").strip().replace(",", "").replace("$", "")
    s = s.rstrip(".")
    s = re.sub(r"^[=\s]+", "", s)
    if not s:
        return None
    try:
        return Decimal(s)
    except InvalidOperation:
        return None


def grade_arith(pred: str, expected: str) -> tuple[int, float, str]:
    a = extract_answer(pred).strip()
    e = expected.strip()
    detail = f"pred={a!r} expected={e!r}"
    if e.upper().startswith("N/A"):
        ok = a.upper().startswith("N/A") or "no arithmetic" in a.lower()
        return int(ok), float(ok), detail
    if "..." in e:
        lead = e.split("...")[0].strip()
        frac = re.search(r"\(([^)]+)\)", e)
        a_compact = a.replace(" ", "").replace(",", "")
        ok = a_compact.startswith(lead) or bool(frac and frac.group(1).replace(" ", "") in a_compact)
        return int(ok), float(ok), detail
    da, de = _to_decimal(a), _to_decimal(e)
    if da is None or de is None:
        ok = _norm(a) == _norm(e)
        return int(ok), float(ok), detail
    ok = abs(da - de) <= Decimal("1e-12")
    return int(ok), float(ok), detail


GRADERS = {"exact": grade_exact, "arith": grade_arith}


def get_grader(name: str):
    if name not in GRADERS:
        raise ValueError(f"unknown grader {name!r}; available: {sorted(GRADERS)}")
    return GRADERS[name]


# ── Propositional-logic grader (relabeling-invariant, structural) ───────────
# Expected format: "P=text; Q=text => f1; f2 [flag: ...]" | "INVALID: reason"
# | "Block1: ... => .... Block2: ... => ..." | "=> Premises: f; f. Conclusion: f"

_SYM_SUBS = [("<->", "↔"), ("<=>", "↔"), ("->", "→"), ("⇒", "→"), ("⊃", "→"), ("⇔", "↔"),
             ("≡", "↔"), ("&&", "∧"), ("&", "∧"), ("^", "∧"), ("·", "∧"), ("∙", "∧"),
             ("||", "∨"), ("|", "∨"), ("!", "¬"), ("~", "¬"), ("∼", "¬"), ("xor", "⊕"), ("⊻", "⊕")]
_STOP = {"the", "a", "an", "is", "are", "it", "was", "were", "be", "been", "will", "that", "this",
         "of", "to", "in", "on", "has", "have", "had", "does", "do", "did", "there", "its", "s"}


def _stem(w: str) -> str:
    for suf in ("ing", "ed", "es", "s"):
        if len(w) > len(suf) + 2 and w.endswith(suf):
            return w[: -len(suf)]
    return w


def _def_tokens(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9']+", (text or "").lower())
    return {_stem(w.strip("'")) for w in words if w not in _STOP and (len(w) > 1 or w.isdigit())}


def _sim(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _expand_ellipsis(s: str) -> str:
    """Expand shorthand chains like P1∧P2∧...∧P27 into the full chain."""
    def _rep(m):
        sym, a, op, b = m.group(1), int(m.group(2)), m.group(3), int(m.group(4))
        if b <= a or b - a > 200:
            return m.group(0)
        return op.join(f"{sym}{i}" for i in range(a, b + 1))
    return re.sub(r"([A-Za-z])(\d+)([∧∨])(?:\1\d+\3)*(?:\.\.\.|…)\3(?:\1\d+\3)*\1(\d+)", _rep, s)


def _norm_formula_text(s: str) -> str:
    s = s.strip()
    for old, new in _SYM_SUBS:
        s = s.replace(old, new)
    s = re.sub(r"\s+", "", s)
    return _expand_ellipsis(s)


class _PLParseError(Exception):
    pass


def _tokenize(f: str) -> list[str]:
    toks = re.findall(r"[A-Za-z]\d*|[∧∨¬→↔⊕()]|.", f)
    for t in toks:
        if not re.fullmatch(r"[A-Za-z]\d*|[∧∨¬→↔⊕()]", t):
            raise _PLParseError(f"bad token {t!r} in {f!r}")
    return toks


def _parse(tokens: list[str]):
    """Recursive descent -> canonical string with commutative ops sorted.
    Precedence: ¬ > ∧ > ∨,⊕ > → > ↔."""
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def take():
        nonlocal pos
        t = tokens[pos]
        pos += 1
        return t

    def atom():
        t = peek()
        if t is None:
            raise _PLParseError("unexpected end")
        if t == "(":
            take()
            node = iff()
            if peek() != ")":
                raise _PLParseError("missing )")
            take()
            return node
        if t == "¬":
            take()
            return ("¬", atom())
        if re.fullmatch(r"[A-Za-z]\d*", t):
            take()
            return ("atom", t)
        raise _PLParseError(f"unexpected {t}")

    def binary(sub, ops, commutative):
        left = sub()
        items = [left]
        op_seen = None
        while peek() in ops:
            op = take()
            if op_seen is not None and op != op_seen:
                # mixed ∨/⊕ without parens: treat left-assoc
                items = [(op_seen, tuple(items))]
                op_seen = op
                items.append(sub())
                continue
            op_seen = op
            items.append(sub())
        if op_seen is None:
            return left
        if commutative:
            return (op_seen, tuple(sorted(items, key=_key)))
        # right-assoc for → : A→B→C = A→(B→C)
        node = items[-1]
        for it in reversed(items[:-1]):
            node = (op_seen, (it, node))
        return node

    def conj():
        return binary(atom, {"∧"}, True)

    def disj():
        return binary(conj, {"∨", "⊕"}, True)

    def impl():
        return binary(disj, {"→"}, False)

    def iff():
        return binary(impl, {"↔"}, True)

    node = iff()
    if pos != len(tokens):
        raise _PLParseError("trailing tokens")
    return node


def _key(node) -> str:
    if node[0] == "atom":
        return node[1]
    if node[0] == "¬":
        return "¬" + _key(node[1])
    return "(" + node[0].join(_key(c) for c in node[1]) + ")"


def _canon(formula: str, mapping: dict[str, str] | None = None) -> str:
    toks = _tokenize(_norm_formula_text(formula))
    if mapping is not None:
        toks = [mapping.get(t, t) if re.fullmatch(r"[A-Za-z]\d*", t) else t for t in toks]
    return _key(_parse(toks))


def _split_formulas(part: str) -> tuple[list[str], list[str] | None]:
    """Return (premises_or_all, conclusion or None)."""
    part = part.strip().replace("...", "…")  # protect ellipsis shorthand from the '.' splitter
    # Drop trailing commentary lines ("Note: ...", "Excluded: ...") that some
    # models append inside the answer tags; they are not part of the formulas.
    kept: list[str] = []
    for ln in part.splitlines():
        if kept and re.match(r"^\s*(note|excluded|explanation|reasoning|comment)s?\b", ln, re.IGNORECASE):
            break
        kept.append(ln)
    part = "\n".join(kept).strip()
    m = re.search(r"premises?\s*:(.*?)conclusion\s*:(.*)$", part, re.IGNORECASE | re.DOTALL)
    if m:
        prem = [f for f in re.split(r"[;.\n]", m.group(1)) if f.strip()]
        conc = [f for f in re.split(r"[;.\n]", m.group(2)) if f.strip()]
        return prem, conc
    return [f for f in re.split(r"[;.\n]", part) if f.strip()], None


def _parse_unit(text: str) -> dict:
    """One scope: legend + formulas. Raises _PLParseError."""
    text = text.strip()
    text = re.sub(r"^[A-Za-z]+\s?\w*\s*:\s*(?=[A-Za-z]\d*\s*[=:])", "", text)  # drop "Block1:" label
    if "=>" in text:
        legend_txt, formula_txt = text.split("=>", 1)
    else:
        legend_txt, formula_txt = "", text
    legend: dict[str, str] = {}
    for chunk in re.split(r"[;\n]", legend_txt):
        chunk = chunk.strip().strip(",")
        if not chunk:
            continue
        m = re.match(r"^\s*([A-Za-z]\d*)\s*(?:=|:|—|–|-)\s*(.+)$", chunk)
        if not m:
            raise _PLParseError(f"bad legend entry {chunk!r}")
        legend[m.group(1)] = m.group(2).strip().strip('"\'')
    formula_txt = re.sub(r"\(equivalently.*$", "", formula_txt, flags=re.IGNORECASE | re.DOTALL)
    prem, conc = _split_formulas(formula_txt)
    return {"legend": legend, "premises": prem, "conclusion": conc}


def _split_blocks(text: str) -> list[str]:
    text = text.strip()
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if len(lines) > 1 and sum("=>" in ln for ln in lines) > 1:
        return lines
    parts = re.split(r"(?<=\S)\.\s+(?=[A-Za-z]+\s?\w*\s*:\s*[A-Za-z]\d*\s*[=:])", text)
    return [p for p in parts if p.strip()]


def _expected_alternatives(expected: str) -> list[str]:
    flag = ""
    m = re.search(r"\[(?:flag|note):(.*)\]\s*$", expected, re.DOTALL)
    base = expected
    if m:
        flag = m.group(1)
        base = expected[: m.start()].strip()
    alts = [base]
    fl = flag.lower()
    if "⊕" in flag and "∨" in base and ("both acceptable" in fl or "ambiguous" in fl):
        alts.append(base.replace("∨", "⊕"))
    if "↔" in base and ("→" in flag and "accepted" in fl):
        alts.append(base.replace("↔", "→"))
    pm = re.search(r"\(([A-Za-z]\d*=[^()]*=>[^()]*)\)", flag)
    if pm:
        alts.append(pm.group(1))
    if "(equivalently" in base:
        em = re.search(r"\(equivalently\s+(.*)\)\s*$", base)
        if em:
            core = re.sub(r"\s*\(equivalently.*$", "", base)
            if "=>" in core:
                legend_txt, _ = core.split("=>", 1)
                alts.append(f"{legend_txt}=> {em.group(1)}")
    return alts


def _compare_units(pred: dict, exp: dict) -> tuple[bool, float]:
    pl, el = pred["legend"], exp["legend"]
    mapping: dict[str, str] = {}
    if el:
        if len(pl) != len(el):
            return False, 0.0
        pairs = sorted(((_sim(_def_tokens(pt), _def_tokens(et)), ps, es)
                        for ps, pt in pl.items() for es, et in el.items()), reverse=True)
        used_p, used_e = set(), set()
        for s, ps, es in pairs:
            if ps in used_p or es in used_e:
                continue
            mapping[ps] = es
            used_p.add(ps)
            used_e.add(es)
        if len(mapping) != len(el):
            return False, 0.0
        exp_map = None
    else:
        # no legend: canonical relabeling by order of first appearance
        def order_map(unit):
            seen: dict[str, str] = {}
            for f in unit["premises"] + (unit["conclusion"] or []):
                for t in re.findall(r"[A-Za-z]\d*", _norm_formula_text(f)):
                    if t not in seen:
                        seen[t] = f"v{len(seen)}"
            return seen
        mapping = order_map(pred)
        exp_map = order_map(exp)
    try:
        pf = sorted(_canon(f, mapping) for f in pred["premises"])
        ef = sorted(_canon(f, exp_map) for f in exp["premises"])
        pc = sorted(_canon(f, mapping) for f in pred["conclusion"]) if pred["conclusion"] is not None else None
        ec = sorted(_canon(f, exp_map) for f in exp["conclusion"]) if exp["conclusion"] is not None else None
    except _PLParseError:
        return False, 0.0
    if (pc is None) != (ec is None):
        return False, 0.0
    matched = len(set(pf) & set(ef)) + (len(set(pc) & set(ec)) if pc else 0)
    total = len(ef) + (len(ec) if ec else 0)
    ok = pf == ef and pc == ec
    return ok, (matched / total if total else 0.0)


def grade_proplogic(pred: str, expected: str) -> tuple[int, float, str]:
    answer = extract_answer(pred).strip()
    alts = _expected_alternatives(expected)
    detail = f"pred={answer[:200]!r} expected={alts[0][:200]!r}"
    best_soft = 0.0
    for alt in alts:
        alt = alt.strip()
        if alt.upper().startswith("INVALID"):
            if answer.upper().startswith("INVALID"):
                return 1, 1.0, detail
            continue
        if answer.upper().startswith("INVALID"):
            continue
        try:
            exp_blocks = [_parse_unit(b) for b in _split_blocks(alt)]
            pred_blocks = [_parse_unit(b) for b in _split_blocks(answer)]
        except _PLParseError as exc:
            detail += f" parse_error={exc}"
            continue
        if len(exp_blocks) != len(pred_blocks):
            continue
        oks, softs = zip(*(_compare_units(p, e) for p, e in zip(pred_blocks, exp_blocks)))
        soft = sum(softs) / len(softs)
        best_soft = max(best_soft, soft)
        if all(oks):
            return 1, 1.0, detail
    return 0, best_soft, detail


GRADERS["proplogic"] = grade_proplogic
