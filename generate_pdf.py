"""
generate_pdf.py
---------------
Generates a professional PDF document (Cahier des Charges) for the TuniRoute project.

Usage:
    pip install reportlab pillow
    python generate_pdf.py

Optional: place use_case_diagram.png and class_diagram.png in the same directory
to embed the UML diagrams into the PDF.

Output: TuniRoute_Cahier_des_Charges.pdf
"""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image, HRFlowable, ListFlowable, ListItem,
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.pdfgen import canvas

# ---------------------------------------------------------------------------
# Color Palette
# ---------------------------------------------------------------------------
DARK_BLUE = colors.HexColor("#1A3A5C")
MID_BLUE = colors.HexColor("#2B6CB0")
LIGHT_BLUE = colors.HexColor("#EBF4FF")
ACCENT = colors.HexColor("#3182CE")
GRAY = colors.HexColor("#4A5568")
LIGHT_GRAY = colors.HexColor("#F7FAFC")
BORDER_GRAY = colors.HexColor("#CBD5E0")
WHITE = colors.white

PAGE_WIDTH, PAGE_HEIGHT = A4

# ---------------------------------------------------------------------------
# Page numbering canvas callback
# ---------------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    """Canvas subclass that adds page numbers and header/footer to every page."""

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        page_num = self._pageNumber
        # Skip footer on the title page (page 1)
        if page_num == 1:
            return
        self.saveState()
        # Footer line
        self.setStrokeColor(BORDER_GRAY)
        self.setLineWidth(0.5)
        self.line(2 * cm, 1.5 * cm, PAGE_WIDTH - 2 * cm, 1.5 * cm)
        # Footer text
        self.setFont("Helvetica", 8)
        self.setFillColor(GRAY)
        self.drawString(2 * cm, 1.1 * cm, "TuniRoute – Cahier des Charges")
        self.drawRightString(
            PAGE_WIDTH - 2 * cm,
            1.1 * cm,
            f"Page {page_num} / {page_count}",
        )
        self.restoreState()


# ---------------------------------------------------------------------------
# Custom DocTemplate that uses BookmarkDocTemplate for TOC
# ---------------------------------------------------------------------------
class TuniRouteDoc(BaseDocTemplate):
    """BaseDocTemplate with TOC notification support."""

    def __init__(self, filename, **kwargs):
        BaseDocTemplate.__init__(self, filename, **kwargs)
        # Single page template with margins
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="normal",
        )
        self.addPageTemplates([PageTemplate(id="main", frames=frame)])

    def afterFlowable(self, flowable):
        """Called after each flowable is rendered – used to register TOC entries."""
        if isinstance(flowable, Paragraph):
            style_name = flowable.style.name
            text = flowable.getPlainText()
            if style_name == "Heading1":
                key = f"h1_{text}"
                self.canv.bookmarkPage(key)
                self.notify("TOCEntry", (0, text, self.page, key))
            elif style_name == "Heading2":
                key = f"h2_{text}"
                self.canv.bookmarkPage(key)
                self.notify("TOCEntry", (1, text, self.page, key))


# ---------------------------------------------------------------------------
# Style definitions
# ---------------------------------------------------------------------------
def build_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="DocTitle",
        fontName="Helvetica-Bold",
        fontSize=22,
        textColor=WHITE,
        alignment=TA_CENTER,
        spaceAfter=12,
        leading=30,
    ))
    styles.add(ParagraphStyle(
        name="DocSubtitle",
        fontName="Helvetica",
        fontSize=13,
        textColor=LIGHT_BLUE,
        alignment=TA_CENTER,
        spaceAfter=8,
        leading=18,
    ))
    styles.add(ParagraphStyle(
        name="DocMeta",
        fontName="Helvetica",
        fontSize=11,
        textColor=WHITE,
        alignment=TA_CENTER,
        spaceAfter=6,
        leading=16,
    ))
    # Override built-in Heading1 / Heading2
    styles["Heading1"].fontName = "Helvetica-Bold"
    styles["Heading1"].fontSize = 15
    styles["Heading1"].textColor = DARK_BLUE
    styles["Heading1"].spaceBefore = 18
    styles["Heading1"].spaceAfter = 8
    styles["Heading1"].leading = 20

    styles["Heading2"].fontName = "Helvetica-Bold"
    styles["Heading2"].fontSize = 12
    styles["Heading2"].textColor = MID_BLUE
    styles["Heading2"].spaceBefore = 12
    styles["Heading2"].spaceAfter = 6
    styles["Heading2"].leading = 16
    styles["Heading2"].leftIndent = 10
    # Override built-in BodyText
    styles["BodyText"].fontName = "Helvetica"
    styles["BodyText"].fontSize = 10
    styles["BodyText"].textColor = GRAY
    styles["BodyText"].alignment = TA_JUSTIFY
    styles["BodyText"].spaceAfter = 6
    styles["BodyText"].leading = 15
    styles["BodyText"].leftIndent = 10
    styles.add(ParagraphStyle(
        name="BulletItem",
        fontName="Helvetica",
        fontSize=10,
        textColor=GRAY,
        spaceAfter=4,
        leading=14,
        leftIndent=20,
        bulletIndent=10,
    ))
    styles.add(ParagraphStyle(
        name="SubBulletItem",
        fontName="Helvetica",
        fontSize=10,
        textColor=GRAY,
        spaceAfter=3,
        leading=13,
        leftIndent=35,
        bulletIndent=25,
    ))
    styles.add(ParagraphStyle(
        name="TOCEntry0",
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=DARK_BLUE,
        spaceAfter=4,
        leading=14,
    ))
    styles.add(ParagraphStyle(
        name="TOCEntry1",
        fontName="Helvetica",
        fontSize=10,
        textColor=GRAY,
        spaceAfter=3,
        leading=13,
        leftIndent=20,
    ))
    styles.add(ParagraphStyle(
        name="DiagramCaption",
        fontName="Helvetica-Oblique",
        fontSize=9,
        textColor=GRAY,
        alignment=TA_CENTER,
        spaceBefore=4,
        spaceAfter=12,
    ))
    styles.add(ParagraphStyle(
        name="ConclusionText",
        fontName="Helvetica",
        fontSize=10,
        textColor=GRAY,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        leading=15,
        leftIndent=10,
    ))
    return styles


# ---------------------------------------------------------------------------
# Helper: section heading with decorative rule
# ---------------------------------------------------------------------------
def section_heading(text, styles, level=1):
    """Return a list of flowables representing a styled section heading."""
    style = styles["Heading1"] if level == 1 else styles["Heading2"]
    elements = []
    if level == 1:
        elements.append(Spacer(1, 0.3 * cm))
        # Colored background strip via a single-cell table
        data = [[Paragraph(f"➢  {text}", style)]]
        tbl = Table(data, colWidths=[PAGE_WIDTH - 4 * cm])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
            ("ROUNDEDCORNERS", [4, 4, 4, 4]),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ]))
        elements.append(tbl)
        elements.append(Spacer(1, 0.2 * cm))
    else:
        elements.append(Paragraph(text, style))
    return elements


# ---------------------------------------------------------------------------
# Helper: bullet list
# ---------------------------------------------------------------------------
def bullet_list(items, styles, sub=False):
    """Return a ListFlowable for a list of strings or (str, [sub_items]) tuples."""
    style = styles["SubBulletItem"] if sub else styles["BulletItem"]
    list_items = []
    for item in items:
        if isinstance(item, tuple):
            text, sub_items = item
            list_items.append(ListItem(
                Paragraph(text, style),
                bulletColor=ACCENT,
                bulletText="•",
            ))
            for si in sub_items:
                list_items.append(ListItem(
                    Paragraph(si, styles["SubBulletItem"]),
                    bulletColor=MID_BLUE,
                    bulletText="–",
                    leftIndent=35,
                ))
        else:
            list_items.append(ListItem(
                Paragraph(item, style),
                bulletColor=ACCENT,
                bulletText="•",
            ))
    return ListFlowable(list_items, bulletType="bullet", start="•")


# ---------------------------------------------------------------------------
# Title Page
# ---------------------------------------------------------------------------
def build_title_page(styles):
    elements = []

    # Full-width dark-blue banner via a table
    title_data = [[
        Paragraph(
            "TuniRoute",
            ParagraphStyle(
                "BigTitle",
                fontName="Helvetica-Bold",
                fontSize=36,
                textColor=WHITE,
                alignment=TA_CENTER,
                leading=44,
            ),
        )
    ]]
    title_tbl = Table(title_data, colWidths=[PAGE_WIDTH - 4 * cm])
    title_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK_BLUE),
        ("TOPPADDING", (0, 0), (-1, -1), 30),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    elements.append(Spacer(1, 2 * cm))
    elements.append(title_tbl)

    # Subtitle strip
    sub_data = [[
        Paragraph(
            "Système intelligent de navigation pour le transport public en Tunisie",
            ParagraphStyle(
                "SubBanner",
                fontName="Helvetica",
                fontSize=13,
                textColor=WHITE,
                alignment=TA_CENTER,
                leading=18,
            ),
        )
    ]]
    sub_tbl = Table(sub_data, colWidths=[PAGE_WIDTH - 4 * cm])
    sub_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), MID_BLUE),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    elements.append(sub_tbl)
    elements.append(Spacer(1, 1.5 * cm))

    # Document type label
    elements.append(Paragraph(
        "Cahier des Charges",
        ParagraphStyle(
            "DocType",
            fontName="Helvetica-Bold",
            fontSize=16,
            textColor=DARK_BLUE,
            alignment=TA_CENTER,
            spaceAfter=30,
        ),
    ))

    # Horizontal rule
    elements.append(HRFlowable(
        width="80%",
        thickness=2,
        color=ACCENT,
        spaceAfter=20,
        hAlign="CENTER",
    ))
    elements.append(Spacer(1, 1 * cm))

    # Metadata table
    meta_style = ParagraphStyle(
        "MetaVal",
        fontName="Helvetica",
        fontSize=11,
        textColor=GRAY,
        alignment=TA_CENTER,
        leading=16,
    )
    meta_label_style = ParagraphStyle(
        "MetaLabel",
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=DARK_BLUE,
        alignment=TA_CENTER,
        leading=16,
    )

    meta_data = [
        [
            Paragraph("Encadré par :", meta_label_style),
            Paragraph("Mr. Mansouri Oussema", meta_style),
        ],
        [
            Paragraph("Année scolaire :", meta_label_style),
            Paragraph("2025 – 2026", meta_style),
        ],
        [
            Paragraph("Projet :", meta_label_style),
            Paragraph("Application Web / Mobile", meta_style),
        ],
    ]
    meta_tbl = Table(meta_data, colWidths=[6 * cm, 9 * cm])
    meta_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
        ("BOX", (0, 0), (-1, -1), 1, BORDER_GRAY),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(meta_tbl)
    elements.append(Spacer(1, 3 * cm))

    # Footer notice
    elements.append(HRFlowable(
        width="60%",
        thickness=1,
        color=BORDER_GRAY,
        hAlign="CENTER",
        spaceAfter=10,
    ))
    elements.append(Paragraph(
        "Document confidentiel – Réservé à l'usage académique",
        ParagraphStyle(
            "Notice",
            fontName="Helvetica-Oblique",
            fontSize=9,
            textColor=BORDER_GRAY,
            alignment=TA_CENTER,
        ),
    ))

    elements.append(PageBreak())
    return elements


# ---------------------------------------------------------------------------
# Table of Contents
# ---------------------------------------------------------------------------
def build_toc(styles):
    elements = []
    elements.append(Paragraph("Table des Matières", styles["Heading1"]))
    elements.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=10))

    toc = TableOfContents()
    toc.levelStyles = [styles["TOCEntry0"], styles["TOCEntry1"]]
    elements.append(toc)
    elements.append(PageBreak())
    return elements, toc


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------

def build_etude_existence(styles):
    elements = []
    elements += section_heading("Étude d'existence", styles)
    elements.append(Paragraph(
        "Il existe plusieurs applications de navigation comme Google Maps, Moovit ou Citymapper. "
        "Cependant, ces solutions sont souvent inefficaces ou incomplètes en Tunisie, notamment pour :",
        styles["BodyText"],
    ))
    elements.append(bullet_list([
        "Les itinéraires des bus, métros, trains (SNCFT, Transtu)",
        "Les correspondances entre moyens de transport",
        "Les estimations de temps réelles",
    ], styles))
    elements.append(Paragraph(
        "Ainsi, il existe un manque d'outils fiables permettant aux Tunisiens de planifier leurs trajets "
        "en transport public.",
        styles["BodyText"],
    ))
    return elements


def build_problematique(styles):
    elements = []
    elements += section_heading("Problématique", styles)
    elements.append(Paragraph(
        "Comment concevoir une application capable de :",
        styles["BodyText"],
    ))
    elements.append(bullet_list([
        "Fournir des itinéraires optimisés en transport public en Tunisie",
        "Estimer le temps de trajet de manière réaliste",
        "Offrir une interface simple et accessible aux utilisateurs",
    ], styles))
    return elements


def build_objectifs(styles):
    elements = []
    elements += section_heading("Objectifs du projet", styles)
    elements.append(Paragraph(
        "L'objectif principal est de développer une application web (ou mobile) permettant aux "
        "utilisateurs de trouver facilement leurs itinéraires en transport public.",
        styles["BodyText"],
    ))
    elements += section_heading("Objectifs spécifiques", styles, level=2)
    elements.append(bullet_list([
        "Proposer des itinéraires optimisés (bus, métro, train)",
        "Fournir une estimation du temps de trajet",
        "Permettre la recherche par point de départ et destination",
        "Offrir une interface intuitive",
        "Gérer les données des lignes de transport",
        "Fournir des informations sur les arrêts et correspondances",
    ], styles))
    return elements


def build_besoins_fonctionnels(styles):
    elements = []
    elements += section_heading("Besoins fonctionnels", styles)

    # 1. Gestion des utilisateurs
    elements += section_heading("1. Gestion des utilisateurs", styles, level=2)
    elements.append(bullet_list([
        "Inscription et authentification",
        "Gestion des profils utilisateurs",
        "Historique des recherches",
    ], styles))

    # 2. Gestion des trajets
    elements += section_heading("2. Gestion des trajets", styles, level=2)
    elements.append(Paragraph("L'utilisateur saisit :", styles["BodyText"]))
    elements.append(bullet_list(["Point de départ", "Destination"], styles, sub=True))
    elements.append(Paragraph("Le système propose :", styles["BodyText"]))
    elements.append(bullet_list([
        "Plusieurs itinéraires possibles",
        "Les correspondances nécessaires",
        "Affichage des moyens de transport utilisés",
    ], styles, sub=True))

    # 3. Calcul des itinéraires
    elements += section_heading("3. Calcul des itinéraires", styles, level=2)
    elements.append(bullet_list([
        "Recherche du chemin optimal",
        ("Prise en compte :", ["Distance", "Temps estimé", "Correspondances"]),
        "Proposition de plusieurs options (rapide / économique)",
    ], styles))

    # 4. Gestion des données de transport
    elements += section_heading("4. Gestion des données de transport", styles, level=2)
    elements.append(Paragraph("L'administrateur peut :", styles["BodyText"]))
    elements.append(bullet_list([
        "Ajouter des lignes (bus, métro…)",
        "Ajouter des stations",
        "Modifier les horaires",
        "Supprimer des données",
    ], styles, sub=True))

    # 5. Estimation du temps
    elements += section_heading("5. Estimation du temps", styles, level=2)
    elements.append(Paragraph("Calcul du temps basé sur :", styles["BodyText"]))
    elements.append(bullet_list([
        "Distance",
        "Moyens de transport",
        "Temps d'attente estimé",
        "Affichage du temps total du trajet",
    ], styles, sub=True))

    # 6. Suivi et historique
    elements += section_heading("6. Suivi et historique", styles, level=2)
    elements.append(bullet_list([
        "Sauvegarde des recherches utilisateur",
        "Accès aux trajets récents",
    ], styles))

    return elements


def build_detail_itineraire(styles):
    elements = []
    elements += section_heading("Détail sur le calcul d'itinéraire", styles)
    elements.append(Paragraph(
        "Le système utilisera un algorithme de type :",
        styles["BodyText"],
    ))
    elements.append(bullet_list([
        "Dijkstra ou A* pour trouver le chemin optimal",
        ("Règles :", [
            "Minimiser le temps total",
            "Réduire les correspondances inutiles",
            "Prioriser les trajets directs si possible",
        ]),
    ], styles))
    return elements


def build_besoins_non_fonctionnels(styles):
    elements = []
    elements += section_heading("Besoins non fonctionnels", styles)

    categories = [
        ("1. Performance", [
            "Réponse rapide (< 2 secondes)",
            "Capable de gérer plusieurs utilisateurs simultanément",
        ]),
        ("2. Sécurité", [
            "Authentification sécurisée (JWT / Spring Security)",
            "Protection des données utilisateurs",
        ]),
        ("3. Fiabilité", [
            "Gestion des erreurs (coordonnées invalides, trajets inexistants)",
            "Validation des entrées utilisateur",
        ]),
        ("4. Accessibilité", [
            "Application web responsive",
            "Interface simple pour tous les utilisateurs",
        ]),
        ("5. Scalabilité", [
            "Architecture extensible",
            "Possibilité d'ajouter d'autres villes ou pays",
        ]),
    ]

    for title, items in categories:
        elements += section_heading(title, styles, level=2)
        elements.append(bullet_list(items, styles))

    return elements


def build_technologies(styles):
    elements = []
    elements += section_heading("Technologies utilisées", styles)

    tech_data = [
        ["Composant", "Technologie"],
        ["Back-end", "Java (Spring Boot)"],
        ["Base de données", "MySQL"],
        ["Sécurité", "Spring Security / JWT"],
        ["Frontend", "HTML / CSS / JS (ou React)"],
        ["Outils", "Postman, Maven"],
    ]

    col_widths = [(PAGE_WIDTH - 4 * cm) * 0.35, (PAGE_WIDTH - 4 * cm) * 0.65]
    tbl = Table(tech_data, colWidths=col_widths)
    tbl.setStyle(TableStyle([
        # Header row
        ("BACKGROUND", (0, 0), (-1, 0), DARK_BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        # Data rows
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 10),
        ("TEXTCOLOR", (0, 1), (-1, -1), GRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        # Grid
        ("BOX", (0, 0), (-1, -1), 1, BORDER_GRAY),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("ALIGN", (0, 1), (0, -1), "LEFT"),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0, 1), (0, -1), DARK_BLUE),
    ]))
    elements.append(tbl)
    return elements


def build_acteurs(styles):
    elements = []
    elements += section_heading("Acteurs cibles", styles)

    elements += section_heading("1. Utilisateurs", styles, level=2)
    elements.append(bullet_list([
        "Citoyens tunisiens",
        "Étudiants",
        "Touristes",
    ], styles))

    elements += section_heading("2. Administrateurs", styles, level=2)
    elements.append(bullet_list([
        "Gèrent les données des transports",
        "Maintiennent le système",
        "Ajoutent et modifient les lignes",
    ], styles))

    return elements


def build_planification(styles):
    elements = []
    elements += section_heading("Planification du projet", styles)

    phases = [
        ("Phase 1 – Analyse des besoins", [
            "Étude du transport en Tunisie",
            "Définition des fonctionnalités",
        ]),
        ("Phase 2 – Conception", [
            "Diagrammes UML",
            "Architecture du système",
        ]),
        ("Phase 3 – Développement", [
            "API + Base de données",
            "Implémentation des algorithmes",
        ]),
        ("Phase 4 – Tests et validation", [
            "Tests fonctionnels",
            "Tests de performance",
        ]),
    ]

    for title, items in phases:
        elements += section_heading(title, styles, level=2)
        elements.append(bullet_list(items, styles))

    return elements


def build_diagrams(styles):
    """Embed UML diagrams if image files are present; otherwise show placeholders."""
    elements = []
    elements += section_heading("Diagramme de cas d'utilisation", styles)

    use_case_path = "use_case_diagram.png"
    if os.path.exists(use_case_path):
        img = Image(use_case_path, width=14 * cm, height=10 * cm, kind="proportional")
        elements.append(img)
    else:
        _placeholder(elements, styles, "Diagramme de cas d'utilisation", "(use_case_diagram.png)")

    elements.append(Paragraph(
        "Figure 1 – Diagramme de cas d'utilisation (Use Case Diagram)",
        styles["DiagramCaption"],
    ))

    elements.append(PageBreak())
    elements += section_heading("Diagramme de classe", styles)

    class_diag_path = "class_diagram.png"
    if os.path.exists(class_diag_path):
        img = Image(class_diag_path, width=14 * cm, height=10 * cm, kind="proportional")
        elements.append(img)
    else:
        _placeholder(elements, styles, "Diagramme de classe", "(class_diagram.png)")

    elements.append(Paragraph(
        "Figure 2 – Diagramme de classe (Class Diagram)",
        styles["DiagramCaption"],
    ))

    return elements


def _placeholder(elements, styles, title, filename):
    """Render a grey box as a placeholder for a missing diagram image."""
    placeholder_style = ParagraphStyle(
        "PlaceholderText",
        fontName="Helvetica-Oblique",
        fontSize=11,
        textColor=GRAY,
        alignment=TA_CENTER,
        leading=16,
    )
    data = [[
        Paragraph(
            f"[ {title} ]<br/><br/>{filename}<br/><br/>"
            "Placez le fichier image dans le même répertoire que ce script.",
            placeholder_style,
        )
    ]]
    tbl = Table(data, colWidths=[14 * cm], rowHeights=[7 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
        ("BOX", (0, 0), (-1, -1), 1.5, BORDER_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    elements.append(tbl)


def build_conclusion(styles):
    elements = []
    elements += section_heading("Conclusion", styles)

    elements.append(Paragraph(
        "Le projet TuniRoute vise à résoudre un problème réel en Tunisie : l'absence d'un système "
        "fiable pour les itinéraires de transport public.",
        styles["ConclusionText"],
    ))
    elements.append(Paragraph("Grâce à :", styles["ConclusionText"]))
    elements.append(bullet_list([
        "Un calcul intelligent des trajets",
        "Une estimation du temps",
        "Une gestion centralisée des données",
    ], styles))
    elements.append(Paragraph(
        "L'application permettra d'améliorer considérablement l'expérience des utilisateurs.",
        styles["ConclusionText"],
    ))
    elements.append(Paragraph("Elle est conçue pour être :", styles["ConclusionText"]))
    elements.append(bullet_list([
        "Évolutive",
        "Performante",
        "Adaptée au contexte tunisien",
    ], styles))
    elements.append(Spacer(1, 0.5 * cm))
    elements.append(HRFlowable(width="60%", thickness=1, color=ACCENT, hAlign="CENTER", spaceAfter=10))
    elements.append(Paragraph(
        "TuniRoute – Année scolaire 2025-2026 – Encadré par Mr. Mansouri Oussema",
        ParagraphStyle(
            "FinalNote",
            fontName="Helvetica-Oblique",
            fontSize=9,
            textColor=GRAY,
            alignment=TA_CENTER,
        ),
    ))
    return elements


# ---------------------------------------------------------------------------
# Main build function
# ---------------------------------------------------------------------------
def generate_pdf(output_path="TuniRoute_Cahier_des_Charges.pdf"):
    styles = build_styles()

    doc = TuniRouteDoc(
        output_path,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2.5 * cm,
    )

    story = []

    # 1. Title page
    story += build_title_page(styles)

    # 2. Table of Contents
    toc_elements, toc = build_toc(styles)
    story += toc_elements

    # 3. Content sections
    story += build_etude_existence(styles)
    story += build_problematique(styles)
    story += build_objectifs(styles)
    story += build_besoins_fonctionnels(styles)
    story += build_detail_itineraire(styles)
    story += build_besoins_non_fonctionnels(styles)
    story += build_technologies(styles)
    story += build_acteurs(styles)
    story += build_planification(styles)
    story.append(PageBreak())

    # 4. Diagrams
    story += build_diagrams(styles)
    story.append(PageBreak())

    # 5. Conclusion
    story += build_conclusion(styles)

    # Build the PDF (two passes needed for TOC page numbers)
    doc.multiBuild(story, canvasmaker=NumberedCanvas)
    print(f"✅  PDF généré avec succès : {output_path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    generate_pdf()
