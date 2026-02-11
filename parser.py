import re
import bisect
import pandas as pd
from pathlib import Path
import pdfplumber


# -----------------------------
# Conversores robustos
# -----------------------------
def to_float_or_none(s: str):
    s = (s or "").strip()
    if s in {"-", ""}:
        return None
    # normaliza negativos que vêm como "- 24.035"
    s = re.sub(r"^\-\s+", "-", s)
    # menos unicode
    s = s.replace("−", "-")
    # remove espaços internos
    s = s.replace(" ", "")
    return float(s)


def to_int_or_none(s: str):
    s = (s or "").strip()
    if s in {"-", ""}:
        return None
    s = s.replace("−", "-").replace(" ", "")
    return int(s)


# -----------------------------
# Regex (ancoradas em linha)
# -----------------------------
# Ex: "1.1.1 CAMPUS DARCY RIBEIRO – DIURNO"
CAMPUS_TURNO_LINE_RX = re.compile(
    r"(?m)^\s*(?:\d+(?:\.\d+)*\s+)?CAMPUS\s+(.+?)\s*[-–—]\s*(DIURNO|NOTURNO|MATUTINO|VESPERTINO|INTEGRAL)\s*$",
    flags=re.IGNORECASE
)

# Ex: "ADMINISTRAÇÃO (BACHARELADO)"
COURSE_LINE_RX = re.compile(
    r"(?m)^\s*([A-ZÁÉÍÓÚÂÊÔÃÕÇ][A-ZÁÉÍÓÚÂÊÔÃÕÇ\s\-–—/\.]{2,}?)\s*\((BACHARELADO|LICENCIATURA)\)\s*$"
)

# Aluno: inscrição de 8 dígitos até a próxima inscrição ou fim
STUDENT_RX = re.compile(r"(?m)(\d{8},.*?)(?=\s*\d{8},|$)")


def normalize_text_keep_lines(text: str) -> str:
    # mantém \n para regex de linha funcionar, mas normaliza espaços demais
    t = text.replace("\u00ad", "").replace("−", "-")
    # separa registros que vêm como " / "
    t = re.sub(r"\s*/\s*", "\n", t)
    # normaliza espaços dentro de cada linha, preservando quebras
    t = "\n".join(re.sub(r"[ \t]+", " ", ln).strip() for ln in t.splitlines())
    return t


# -----------------------------
# Extração de texto do PDF
# -----------------------------
def extract_text_from_pdf(pdf_path: Path) -> str:
    pages_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # tenta preservar layout/colunas
            txt = page.extract_text(layout=True, x_tolerance=1, y_tolerance=1) or ""
            # fallback: às vezes extract_text vem ruim
            if len(txt.strip()) < 30:
                words = page.extract_words(use_text_flow=True) or []
                txt = " ".join(w["text"] for w in words)
            pages_text.append(txt)
    return "\n".join(pages_text)


# -----------------------------
# Construir "linha do tempo" de cabeçalhos
# -----------------------------
def build_header_timeline(text: str):
    """
    Retorna uma lista ordenada de eventos:
    (posicao_no_texto, campus, turno, curso)
    onde cada evento representa o "estado" a partir daquele ponto.
    """
    events = []

    # campus/turno
    for m in CAMPUS_TURNO_LINE_RX.finditer(text):
        campus = m.group(1).strip(" -–—:;,.").upper()
        turno = m.group(2).strip().upper()
        events.append((m.start(), ("campus", campus, turno)))

    # curso
    for m in COURSE_LINE_RX.finditer(text):
        curso_nome = m.group(1).strip(" -–—:;,.")
        tipo = m.group(2).strip().upper()  # não usamos no CSV, mas poderia guardar
        # guarda apenas o nome do curso
        events.append((m.start(), ("curso", curso_nome, tipo)))

    # ordena por posição
    events.sort(key=lambda x: x[0])

    # caminha e cria estados
    timeline = []
    campus = None
    turno = None
    curso = None

    for pos, ev in events:
        if ev[0] == "campus":
            campus, turno = ev[1], ev[2]
        else:
            curso = ev[1]  # nome do curso
        timeline.append((pos, campus, turno, curso))

    # garante pelo menos um estado inicial
    if not timeline:
        timeline = [(0, None, None, None)]

    return timeline


def get_state_for_position(timeline, pos: int):
    """
    Pega o último estado cujo start_pos <= pos.
    """
    starts = [t[0] for t in timeline]
    idx = bisect.bisect_right(starts, pos) - 1
    idx = max(idx, 0)
    _, campus, turno, curso = timeline[idx]
    return campus, turno, curso


# -----------------------------
# Parser principal
# -----------------------------
def parse_unb(texto: str) -> pd.DataFrame:
    t = normalize_text_keep_lines(texto)
    timeline = build_header_timeline(t)

    rows = []

    for m in STUDENT_RX.finditer(t):
        bloco = m.group(1).strip(" ,/ \n")
        start_pos = m.start(1)

        campus, turno, curso = get_state_for_position(timeline, start_pos)

        parts = [p.strip() for p in bloco.split(",")]
        if len(parts) < 7:
            continue

        row = {
            "campus": campus,
            "turno": turno,
            "curso": curso,
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

    return pd.DataFrame(rows)


def generate_csv_from_pdf(pdf_path: Path, output_csv: Path, ano: int):
    raw_text = extract_text_from_pdf(pdf_path)
    df = parse_unb(raw_text)

    df.insert(0, "ano", ano)
    df["inscricao"] = df["inscricao"].astype(str)

    output_csv.parent.mkdir(parents=True, exist_ok=True)

    # Excel PT-BR friendly
    df.to_csv(output_csv, index=False, sep=";", encoding="utf-8-sig")

    # resumo pra validar
    print("[OK] CSV:", output_csv)
    print("Linhas:", len(df))
    print("Cursos (amostra):", df["curso"].dropna().unique()[:10])


if __name__ == "__main__":
    pdf_path = Path("data/raw/vest2023.pdf")
    output_csv = Path("data/processed/vest2023.csv")
    generate_csv_from_pdf(pdf_path, output_csv, ano=2023)