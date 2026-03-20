# Compilador LaTeX → PDF via GitHub Actions

Pipeline automatitzat per compilar exàmens i documents LaTeX amb **XeLaTeX** i publicar el PDF resultant directament al repositori i com a artifact descàrregable.

Fet per **Adrià Santacreu** — Institut Escola Sant Pol de Mar.

---

## Com funciona

```
Tu edites examen.tex
       │
       ▼
   git push
       │
       ▼
┌─────────────────────────────────────┐
│         GitHub Actions              │
│                                     │
│  1. Checkout del codi               │
│  2. XeLaTeX compila examen.tex      │
│     (fonts Noto Sans bundlejades)   │
│  3. PDF commitat al repo [skip ci]  │
│  4. PDF guardat com a Artifact      │
└─────────────────────────────────────┘
       │
       ▼
  examen.pdf disponible a:
  · GitHub repo (sempre actualitzat)
  · Actions > Artifacts (90 dies)
```

---

## Estructura del repo

```
compilate-latex-documents/
├── examen.tex                  ← fitxer actiu (substitueix-lo per compilar)
├── examen.pdf                  ← PDF generat (actualitzat automàticament)
│
├── assets/
│   ├── fonts/                  ← Noto Sans (bundlejat, no cal instal·lar res)
│   │   ├── NotoSans-Regular.ttf
│   │   ├── NotoSans-Bold.ttf
│   │   ├── NotoSans-Italic.ttf
│   │   └── NotoSans-BoldItalic.ttf
│   ├── logo_institut.png       ← Institut Escola Sant Pol de Mar
│   └── logo_generalitat.png    ← Departament d'Educació
│
├── arxius/                     ← historial d'exàmens compilats
│   ├── 1r Batxillerat/
│   │   └── 20260320_algebra_trigonometria/
│   │       └── examen.tex
│   └── 4rt ESO/
│       └── fitxa_equacions_racionals.tex
│
└── .github/workflows/
    └── compila.yml             ← workflow principal
```

---

## Ús

### Compilar un nou document

1. Substitueix `examen.tex` per el teu fitxer LaTeX
2. Fes push:

```bash
git add examen.tex
git commit -m "Examen [curs] - [unitat] - [data]"
git push
```

3. El PDF apareix a `examen.pdf` en ~2 minuts

### Arxivar un examen antic

Mou el `.tex` (i el `.pdf` si vols) a `arxius/[curs]/[YYYYMMDD_nom]/` abans de substituir `examen.tex`.

---

## Plantilla d'examen

La plantilla oficial amb totes les macros i el disseny corporatiu és a:
`C:\projects\examens-latex-2526\templates\plantilla-examen.tex`

### Característiques de la plantilla

| Característica | Detall |
|---|---|
| Font | Noto Sans (sans-serif, accessible) |
| Logos | Institut + Generalitat via `\fancyhdr` |
| Colors rotatius | BrightPurple → BrightGreen → BrightBlue |
| Qüestions test | `multicol`, graella de respostes |
| Problemes | `tcolorbox`, gràfiques TikZ |
| Pàgina | Número circular al peu dret |

### Variables de configuració

```latex
\newcommand{\assignatura}{Matemàtiques I}
\newcommand{\curs}{1r Batxillerat}
\newcommand{\unitat}{Àlgebra i Trigonometria}
\newcommand{\dataexamen}{20 de març del 2026}
\newcommand{\tempsexamen}{90}
\newcommand{\puntstest}{4}
\newcommand{\puntsproblemes}{6}
\newcommand{\encert}{0,4}
\newcommand{\error}{0,13}
```

---

## Workflow en detall

```yaml
# .github/workflows/compila.yml (resum)

- Compilar amb XeLaTeX
  · compiler: xelatex
  · extra_fonts: ./assets/fonts/*.ttf
  · work_in_root_file_dir: true

- Commitar PDF
  · git add examen.pdf
  · git commit -m "PDF compilat automàticament [skip ci]"
  · git push

- Guardar Artifact
  · name: examen-pdf
  · retention-days: 90
```

**Nota**: el `[skip ci]` al missatge del commit evita que el push del bot torni a disparar el workflow.

---

## Dependències

- **Cap dependència local** — tot compila al núvol via [xu-cheng/latex-action@v3](https://github.com/xu-cheng/latex-action) (imatge Docker `texlive-full`)
- Fonts Noto Sans bundlejades al repo (no cal instal·lar-les)
- Logos inclosos a `assets/`

---

## Exemple de PDF generat

[`examen.pdf`](./examen.pdf) — Matemàtiques I, 1r Batxillerat · Àlgebra i Trigonometria
