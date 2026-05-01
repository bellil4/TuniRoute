#!/usr/bin/env python3
"""
Generate a professional PDF specification document for the TuniRoute project.

Usage:
    python generate_pdf.py

Requirements:
    pip install reportlab Pillow matplotlib

Output:
    TuniRoute_Cahier_des_Charges.pdf  (in the same directory as this script)
"""

import os
import sys

# Ensure the diagrams are present; auto-generate if missing
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USE_CASE_IMG = os.path.join(SCRIPT_DIR, "use_case_diagram.png")
CLASS_IMG    = os.path.join(SCRIPT_DIR, "class_diagram.png")

if not os.path.exists(USE_CASE_IMG) or not os.path.exists(CLASS_IMG):
    print("Diagrams not found – generating them first …")
    import generate_diagrams
    generate_diagrams.generate_use_case_diagram()
    generate_diagrams.generate_class_diagram()

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak,
    Table, TableStyle, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------------------------------------------------------------------------
# Page layout
# ---------------------------------------------------------------------------
PAGE_W, PAGE_H = A4
MARGIN = 2.0 * cm

OUTPUT = os.path.join(SCRIPT_DIR, "TuniRoute_Cahier_des_Charges.pdf")

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------
DARK_BLUE   = colors.HexColor("#1A237E")
MID_BLUE    = colors.HexColor("#1565C0")
LIGHT_BLUE  = colors.HexColor("#E3F2FD")
ACCENT      = colors.HexColor("#F9A825")
GREY        = colors.HexColor("#757575")
LIGHT_GREY  = colors.HexColor("#F5F5F5")
WHITE       = colors.white
BLACK       = colors.black

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

def build_styles():
    base = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=base["Title"],
        fontSize=28,
        textColor=WHITE,
        alignment=TA_CENTER,
        spaceAfter=6,
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=base["Normal"],
        fontSize=14,
        textColor=WHITE,
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    h1 = ParagraphStyle(
        "H1",
        parent=base["Heading1"],
        fontSize=15,
        textColor=WHITE,
        backColor=DARK_BLUE,
        spaceBefore=16,
        spaceAfter=8,
        leftIndent=-0.5 * cm,
        rightIndent=-0.5 * cm,
        leading=22,
        borderPad=6,
    )
    h2 = ParagraphStyle(
        "H2",
        parent=base["Heading2"],
        fontSize=12,
        textColor=DARK_BLUE,
        spaceBefore=10,
        spaceAfter=4,
        borderPadding=(0, 0, 2, 0),
    )
    h3 = ParagraphStyle(
        "H3",
        parent=base["Heading3"],
        fontSize=10,
        textColor=MID_BLUE,
        spaceBefore=6,
        spaceAfter=3,
        leftIndent=0.3 * cm,
    )
    body = ParagraphStyle(
        "Body",
        parent=base["Normal"],
        fontSize=10,
        textColor=BLACK,
        leading=14,
        spaceAfter=4,
        alignment=TA_JUSTIFY,
    )
    bullet = ParagraphStyle(
        "Bullet",
        parent=body,
        leftIndent=0.8 * cm,
        bulletIndent=0.2 * cm,
        spaceAfter=2,
    )
    caption = ParagraphStyle(
        "Caption",
        parent=base["Normal"],
        fontSize=8,
        textColor=GREY,
        alignment=TA_CENTER,
        spaceAfter=8,
    )
    return {
        "title": title_style,
        "subtitle": subtitle_style,
        "h1": h1,
        "h2": h2,
        "h3": h3,
        "body": body,
        "bullet": bullet,
        "caption": caption,
    }


# ---------------------------------------------------------------------------
# Helper flowables
# ---------------------------------------------------------------------------

def hr(color=DARK_BLUE, thickness=1.5):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=6)


def b(text, style):
    return Paragraph(text, style)


def diagram_image(path, caption_text, styles, max_w=16 * cm):
    """Return an image + caption as a list of flowables."""
    from PIL import Image as PILImage
    pil = PILImage.open(path)
    orig_w, orig_h = pil.size
    ratio = orig_h / orig_w
    w = min(max_w, PAGE_W - 2 * MARGIN)
    h = w * ratio
    img = Image(path, width=w, height=h)
    cap = Paragraph(caption_text, styles["caption"])
    return [img, cap, Spacer(1, 0.3 * cm)]


def info_table(rows, styles):
    """Two-column info table."""
    data = [[Paragraph(k, styles["body"]), Paragraph(v, styles["body"])]
            for k, v in rows]
    t = Table(data, colWidths=[5 * cm, 11 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_BLUE),
        ("TEXTCOLOR",  (0, 0), (0, -1), DARK_BLUE),
        ("FONTNAME",   (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE",   (0, 0), (-1, -1), 9),
        ("GRID",       (0, 0), (-1, -1), 0.4, colors.HexColor("#BBDEFB")),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, LIGHT_GREY]),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


# ---------------------------------------------------------------------------
# Title page
# ---------------------------------------------------------------------------

def title_page(styles):
    story = []

    # Blue banner header
    banner_text = (
        "<b>UNIVERSITÉ DE TUNIS EL MANAR</b><br/>"
        "École Nationale d'Ingénieurs de Tunis"
    )
    story.append(Spacer(1, 0.8 * cm))

    banner_data = [[Paragraph(banner_text, styles["subtitle"])]]
    banner = Table(banner_data, colWidths=[PAGE_W - 2 * MARGIN])
    banner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK_BLUE),
        ("TOPPADDING",    (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
    ]))
    story.append(banner)
    story.append(Spacer(1, 1.5 * cm))

    # Main title
    title_data = [[Paragraph("TuniRoute", styles["title"])]]
    title_tbl = Table(title_data, colWidths=[PAGE_W - 2 * MARGIN])
    title_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), MID_BLUE),
        ("TOPPADDING",    (0, 0), (-1, -1), 20),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 20),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
    ]))
    story.append(title_tbl)
    story.append(Spacer(1, 0.4 * cm))

    subtitle_data = [[Paragraph(
        "Cahier des Charges Fonctionnel<br/>"
        "<font size='12'>Application de navigation des transports en commun en Tunisie</font>",
        styles["subtitle"]
    )]]
    sub_tbl = Table(subtitle_data, colWidths=[PAGE_W - 2 * MARGIN])
    sub_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#283593")),
        ("TOPPADDING",    (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
    ]))
    story.append(sub_tbl)
    story.append(Spacer(1, 2.0 * cm))

    # Project info table
    story.append(info_table([
        ("<b>Encadrant</b>",   "M. Mansouri Oussema"),
        ("<b>Équipe</b>",      "Projet de fin d'études – Génie Logiciel"),
        ("<b>Année</b>",       "2025 – 2026"),
        ("<b>Version</b>",     "1.0"),
        ("<b>Date</b>",        "Mai 2026"),
    ], styles))

    story.append(Spacer(1, 1.5 * cm))
    story.append(hr())

    abstract = (
        "Ce document présente le cahier des charges fonctionnel de l'application "
        "<b>TuniRoute</b>, une solution de navigation dédiée aux transports en commun "
        "en Tunisie (métro, bus, TGM, louage). Il décrit le contexte du projet, les "
        "acteurs impliqués, les exigences fonctionnelles et non-fonctionnelles, ainsi "
        "que les diagrammes UML illustrant l'architecture logicielle."
    )
    story.append(Paragraph(abstract, styles["body"]))
    story.append(PageBreak())
    return story


# ---------------------------------------------------------------------------
# Document sections
# ---------------------------------------------------------------------------

def section_presentation(styles):
    s = styles
    story = []
    story.append(Paragraph("1. Présentation du Projet", s["h1"]))
    story.append(Spacer(1, 0.2 * cm))

    story.append(Paragraph("1.1 Contexte général", s["h2"]))
    story.append(Paragraph(
        "La Tunisie dispose d'un réseau de transports en commun varié — métro léger, "
        "bus urbains, TGM (Train de banlieue Tunis-Goulette-Marsa) et louages interurbains — mais "
        "souffre d'un manque d'outils numériques accessibles permettant aux usagers "
        "de planifier leurs déplacements efficacement. La majorité des applications "
        "existantes ne couvrent pas l'ensemble des modes de transport ou ne proposent "
        "pas d'itinéraires multimodaux.", s["body"]))

    story.append(Paragraph("1.2 Objectifs du projet", s["h2"]))
    objectives = [
        "Proposer une application mobile et web de navigation multimodale pour les "
        "transports en commun tunisiens.",
        "Permettre à l'utilisateur de rechercher un itinéraire entre deux points avec "
        "estimation du temps et des alternatives.",
        "Offrir une interface d'administration pour la gestion des lignes, stations et horaires.",
        "Garantir une expérience utilisateur intuitive, performante et accessible.",
    ]
    for obj in objectives:
        story.append(Paragraph(f"• {obj}", s["bullet"]))

    story.append(Paragraph("1.3 Périmètre", s["h2"]))
    story.append(Paragraph(
        "Le projet couvre les villes et agglomérations desservies par les réseaux "
        "Transtu (métro et bus), SNCFT (TGM) et les lignes de louage nationales. "
        "La première version cible Tunis et sa grande banlieue.", s["body"]))
    story.append(Spacer(1, 0.2 * cm))
    return story


def section_actors(styles):
    s = styles
    story = []
    story.append(Paragraph("2. Acteurs du Système", s["h1"]))
    story.append(Spacer(1, 0.2 * cm))

    actors = [
        ("Utilisateur", "Tout usager souhaitant planifier un déplacement en transport en commun. "
         "Il peut rechercher des itinéraires, consulter son historique et gérer ses favoris."),
        ("Administrateur", "Responsable de la maintenance du système : gestion des lignes, "
         "stations et horaires via un tableau de bord dédié."),
    ]
    for name, desc in actors:
        story.append(Paragraph(name, s["h2"]))
        story.append(Paragraph(desc, s["body"]))
    return story


def section_functional_requirements(styles):
    s = styles
    story = []
    story.append(Paragraph("3. Exigences Fonctionnelles", s["h1"]))
    story.append(Spacer(1, 0.2 * cm))

    story.append(Paragraph("3.1 Authentification", s["h2"]))
    reqs = [
        "Inscription avec email, nom, prénom et mot de passe.",
        "Connexion sécurisée (JWT) pour l'accès à toutes les fonctionnalités.",
        "Gestion des rôles : Utilisateur / Administrateur.",
    ]
    for r in reqs:
        story.append(Paragraph(f"• {r}", s["bullet"]))

    story.append(Paragraph("3.2 Recherche d'itinéraire", s["h2"]))
    reqs2 = [
        "Saisie du point de départ et de la destination.",
        "Calcul automatique des itinéraires optimaux (temps, correspondances).",
        "Estimation de la durée totale du trajet.",
        "Affichage des résultats avec détail des correspondances.",
        "Proposition d'itinéraires alternatifs.",
    ]
    for r in reqs2:
        story.append(Paragraph(f"• {r}", s["bullet"]))

    story.append(Paragraph("3.3 Historique et Favoris", s["h2"]))
    reqs3 = [
        "Consultation de l'historique des recherches.",
        "Ajout, consultation et suppression des itinéraires favoris.",
    ]
    for r in reqs3:
        story.append(Paragraph(f"• {r}", s["bullet"]))

    story.append(Paragraph("3.4 Administration", s["h2"]))
    reqs4 = [
        "Gestion des lignes de transport (ajout, modification, suppression).",
        "Gestion des stations (ajout, modification, suppression).",
        "Gestion des horaires (ajout, modification, suppression).",
    ]
    for r in reqs4:
        story.append(Paragraph(f"• {r}", s["bullet"]))
    return story


def section_non_functional(styles):
    s = styles
    story = []
    story.append(Paragraph("4. Exigences Non-Fonctionnelles", s["h1"]))
    story.append(Spacer(1, 0.2 * cm))

    nfrs = [
        ("Performance",    "Temps de réponse inférieur à 2 secondes pour le calcul d'itinéraire."),
        ("Disponibilité",  "Taux de disponibilité cible : 99,5 % (hors maintenance planifiée)."),
        ("Sécurité",       "Authentification JWT, hachage bcrypt des mots de passe, HTTPS."),
        ("Scalabilité",    "Architecture microservices permettant une montée en charge horizontale."),
        ("Accessibilité",  "Interface responsive, compatible mobile et desktop."),
        ("Maintenabilité", "Code documenté, tests unitaires avec couverture ≥ 80 %."),
    ]
    data = [[Paragraph("<b>" + k + "</b>", s["body"]),
             Paragraph(v, s["body"])] for k, v in nfrs]
    t = Table(data, colWidths=[4 * cm, 12 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_BLUE),
        ("TEXTCOLOR",  (0, 0), (0, -1), DARK_BLUE),
        ("GRID",       (0, 0), (-1, -1), 0.4, colors.HexColor("#BBDEFB")),
        ("ROWBACKGROUNDS", (1, 0), (-1, -1), [WHITE, LIGHT_GREY]),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    return story


def section_tech_stack(styles):
    s = styles
    story = []
    story.append(Paragraph("5. Architecture Technique", s["h1"]))
    story.append(Spacer(1, 0.2 * cm))

    stack = [
        ("Frontend",     "React.js / React Native, TailwindCSS"),
        ("Backend",      "Spring Boot (Java), REST API"),
        ("Base de données", "PostgreSQL + PostGIS"),
        ("Authentification", "Spring Security + JWT"),
        ("Déploiement",  "Docker, Kubernetes, GitHub Actions (CI/CD)"),
        ("Cartographie", "OpenStreetMap, Leaflet.js"),
    ]
    story.append(info_table([(f"<b>{k}</b>", v) for k, v in stack], s))
    return story


def section_uml(styles):
    s = styles
    story = []
    story.append(Paragraph("6. Diagrammes UML", s["h1"]))
    story.append(Spacer(1, 0.2 * cm))

    story.append(Paragraph("6.1 Diagramme de cas d'utilisation", s["h2"]))
    story.append(Paragraph(
        "Ce diagramme présente les interactions entre les acteurs et le système. "
        "L'<b>Utilisateur</b> et l'<b>Administrateur</b> s'authentifient avant d'accéder "
        "à leurs fonctionnalités respectives, toutes liées par des relations "
        "<i>«include»</i>.", s["body"]))
    story.append(Spacer(1, 0.3 * cm))
    story.extend(diagram_image(USE_CASE_IMG,
                               "Figure 1 – Diagramme de cas d'utilisation TuniRoute", s))

    story.append(PageBreak())

    story.append(Paragraph("6.2 Diagramme de classe", s["h2"]))
    story.append(Paragraph(
        "Le diagramme de classe décrit la structure statique du système. "
        "Les classes principales sont : <b>Utilisateur</b>, <b>Trajet</b>, "
        "<b>Itinéraire</b>, <b>LigneTransport</b>, <b>Station</b>, <b>Horaire</b>, "
        "<b>TypeTransport</b>, <b>Role</b>, <b>Favori</b> et <b>Historique</b>. "
        "La classe <i>Trajet</i> est directement reliée à <i>Station</i> via les "
        "rôles <i>départ</i> et <i>arrivée</i>.", s["body"]))
    story.append(Spacer(1, 0.3 * cm))
    story.extend(diagram_image(CLASS_IMG,
                               "Figure 2 – Diagramme de classe TuniRoute", s))
    return story


def section_planning(styles):
    s = styles
    story = []
    story.append(Paragraph("7. Planning Prévisionnel", s["h1"]))
    story.append(Spacer(1, 0.2 * cm))

    phases = [
        ("Phase 1 – Analyse",          "Semaines 1-2",  "Recueil des besoins, rédaction du cahier des charges"),
        ("Phase 2 – Conception",        "Semaines 3-4",  "Diagrammes UML, architecture technique"),
        ("Phase 3 – Développement",     "Semaines 5-10", "Implémentation backend et frontend"),
        ("Phase 4 – Tests & QA",        "Semaines 11-12","Tests unitaires, tests d'intégration"),
        ("Phase 5 – Déploiement",       "Semaine 13",    "Mise en production (Docker / Cloud)"),
        ("Phase 6 – Documentation",     "Semaine 14",    "Rapport final, présentation"),
    ]
    data = [["Phase", "Durée", "Livrables"]] + phases
    col_w = [(PAGE_W - 2 * MARGIN) * f for f in [0.3, 0.18, 0.52]]
    t = Table(data, colWidths=col_w)
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0), DARK_BLUE),
        ("TEXTCOLOR",   (0, 0), (-1, 0), WHITE),
        ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",        (0, 0), (-1, -1), 0.4, colors.HexColor("#BBDEFB")),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",  (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ALIGN",       (1, 0), (1, -1), "CENTER"),
    ]))
    story.append(t)
    return story


# ---------------------------------------------------------------------------
# Header / Footer callbacks
# ---------------------------------------------------------------------------

def _on_first_page(canvas, doc):
    pass  # Title page has its own header


def _on_later_pages(canvas, doc):
    canvas.saveState()
    # Header bar
    canvas.setFillColor(DARK_BLUE)
    canvas.rect(MARGIN, PAGE_H - 1.5 * cm, PAGE_W - 2 * MARGIN, 0.7 * cm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(MARGIN + 0.2 * cm, PAGE_H - 1.1 * cm, "TuniRoute – Cahier des Charges")
    canvas.drawRightString(PAGE_W - MARGIN - 0.2 * cm, PAGE_H - 1.1 * cm, "Confidentiel")

    # Footer
    canvas.setStrokeColor(DARK_BLUE)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 1.5 * cm, PAGE_W - MARGIN, 1.5 * cm)
    canvas.setFillColor(DARK_BLUE)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(MARGIN, 1.1 * cm, "© 2026 TuniRoute – Tous droits réservés")
    canvas.drawRightString(PAGE_W - MARGIN, 1.1 * cm, f"Page {doc.page}")
    canvas.restoreState()


# ---------------------------------------------------------------------------
# Main builder
# ---------------------------------------------------------------------------

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=2.2 * cm,
        bottomMargin=2.2 * cm,
        title="TuniRoute – Cahier des Charges",
        author="Équipe TuniRoute",
        subject="Spécification fonctionnelle – Transport en commun Tunisie",
    )

    styles = build_styles()

    story = []
    story.extend(title_page(styles))
    story.extend(section_presentation(styles))
    story.extend(section_actors(styles))
    story.extend(section_functional_requirements(styles))
    story.extend(section_non_functional(styles))
    story.extend(section_tech_stack(styles))
    story.extend(section_uml(styles))
    story.extend(section_planning(styles))

    doc.build(
        story,
        onFirstPage=_on_first_page,
        onLaterPages=_on_later_pages,
    )
    print(f"\n✅  PDF generated → {OUTPUT}")


if __name__ == "__main__":
    build_pdf()
