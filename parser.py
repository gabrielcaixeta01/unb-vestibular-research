import re
import pandas as pd

def to_float_or_none(s):
    s = s.strip()
    if s in {"-", ""}:
        return None
    return float(s)

def to_int_or_none(s):
    s = s.strip()
    if s in {"-", ""}:
        return None
    return int(s)

# Heurísticas de cabeçalho de curso (ajuste se necessário)
COURSE_HINTS = [
    r"\((?:BACHARELADO|LICENCIATURA)\)",  # muito comum em editais
    r"\bENGENHARIA\b",
    r"\bCI[ÊE]NCIA\b",
    r"\bMEDICINA\b",
    r"\bDIREITO\b",
]

def extract_last_course_header(gap_text: str):
    """
    Tenta achar a ÚLTIMA linha/título de curso dentro do trecho entre alunos.
    Como o PDF vira um texto 'achatado', aqui buscamos padrões típicos.
    """
    g = re.sub(r"\s+", " ", gap_text).strip()

    # tenta achar algo com (BACHARELADO|LICENCIATURA) e pegar a "frase" ao redor
    m = None
    for pat in COURSE_HINTS:
        # pega até ~120 chars antes e depois do hint (ajustável)
        rx = re.compile(rf"(.{{0,120}}{pat}.{{0,120}})", re.IGNORECASE)
        for mm in rx.finditer(g):
            m = mm  # fica com o último encontrado

    if not m:
        return None

    candidate = m.group(1).strip(" -–—:;,.")
    # limpeza leve
    candidate = re.sub(r"\s{2,}", " ", candidate)
    return candidate

def parse_unb_with_course(texto: str) -> pd.DataFrame:
    t = re.sub(r"\s+", " ", texto).strip()

    # cada aluno: do "8 dígitos," até a próxima inscrição ou fim
    student_rx = re.compile(r"(?m)(\d{8},.*?)(?=\s*\d{8},|$)")

    rows = []
    curso_atual = None
    last_end = 0

    for m in student_rx.finditer(t):
        start, end = m.start(1), m.end(1)

        # trecho entre o fim do último aluno e o início do atual
        gap = t[last_end:start]
        novo_curso = extract_last_course_header(gap)
        if novo_curso:
            curso_atual = novo_curso

        bloco = m.group(1).strip(" ,/")

        parts = [p.strip() for p in bloco.split(",")]
        if len(parts) < 7:
            last_end = end
            continue

        row = {
            "curso": curso_atual,
            "inscricao": parts[0],
            "nome": parts[1],
            "nota_CI": to_float_or_none(parts[2]),
            "nota_CII": to_float_or_none(parts[3]),
            "nota_CIII": to_float_or_none(parts[4]),
            "nota_redacao": to_float_or_none(parts[5]),
            "argumento_final": to_float_or_none(parts[6]),
            "class_universal": to_int_or_none(parts[7]) if len(parts) > 7 else None,
            "classificacoes_raw": parts[8:] if len(parts) > 8 else [],
        }

        rows.append(row)
        last_end = end

    return pd.DataFrame(rows)