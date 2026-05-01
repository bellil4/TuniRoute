#!/usr/bin/env python3
"""
Generate UML diagrams for TuniRoute project.
Produces:
  - use_case_diagram.png
  - class_diagram.png
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def draw_actor(ax, x, y, label, fontsize=9):
    """Draw a UML stick-figure actor."""
    head_r = 0.18
    # head
    head = plt.Circle((x, y + 0.55 + head_r), head_r, color="black", fill=False, lw=1.5, zorder=5)
    ax.add_patch(head)
    # body
    ax.plot([x, x], [y + 0.55, y + 0.18], color="black", lw=1.5, zorder=5)
    # arms
    ax.plot([x - 0.28, x + 0.28], [y + 0.40, y + 0.40], color="black", lw=1.5, zorder=5)
    # legs
    ax.plot([x, x - 0.22], [y + 0.18, y], color="black", lw=1.5, zorder=5)
    ax.plot([x, x + 0.22], [y + 0.18, y], color="black", lw=1.5, zorder=5)
    # label
    ax.text(x, y - 0.22, label, ha="center", va="top", fontsize=fontsize,
            fontweight="bold", zorder=5)


def draw_ellipse(ax, cx, cy, w, h, label, fontsize=8.5, bg="#FFFDE7", border="#F9A825"):
    """Draw a UML use-case ellipse."""
    ell = mpatches.Ellipse((cx, cy), w, h,
                           edgecolor=border, facecolor=bg, lw=1.5, zorder=4)
    ax.add_patch(ell)
    # wrap label
    words = label.split()
    if len(words) > 3:
        mid = len(words) // 2
        line1 = " ".join(words[:mid])
        line2 = " ".join(words[mid:])
        ax.text(cx, cy + 0.07, line1, ha="center", va="center", fontsize=fontsize,
                zorder=5)
        ax.text(cx, cy - 0.18, line2, ha="center", va="center", fontsize=fontsize,
                zorder=5)
    else:
        ax.text(cx, cy, label, ha="center", va="center", fontsize=fontsize,
                zorder=5)


def draw_include_arrow(ax, x1, y1, x2, y2, label="<<include>>", fontsize=7.5):
    """Draw a dashed arrow with <<include>> label."""
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color="#555555",
                                lw=1.2, linestyle="dashed"))
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    ax.text(mx, my, label, ha="center", va="bottom", fontsize=fontsize,
            color="#555555", style="italic", zorder=6)


def draw_solid_arrow(ax, x1, y1, x2, y2):
    """Draw a solid association line."""
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-", color="#333333", lw=1.5))


# ---------------------------------------------------------------------------
# 1. Use Case Diagram
# ---------------------------------------------------------------------------

def generate_use_case_diagram():
    fig, ax = plt.subplots(figsize=(22, 16))
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 16)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    # Title
    ax.text(11, 15.4, "Diagramme de cas d'utilisation – TuniRoute",
            ha="center", va="center", fontsize=15, fontweight="bold", color="#1A237E")
    ax.axhline(15.1, color="#1A237E", lw=1.5, xmin=0.03, xmax=0.97)

    # ---- System boundary box ----
    sys_box = FancyBboxPatch((3.5, 1.2), 15, 13.4,
                             boxstyle="round,pad=0.05",
                             edgecolor="#1A237E", facecolor="#F3F4FF",
                             lw=2, zorder=1)
    ax.add_patch(sys_box)
    ax.text(11, 14.35, "Système TuniRoute", ha="center", va="center",
            fontsize=11, color="#1A237E", fontweight="bold")

    # ---- Actors ----
    draw_actor(ax, 1.5, 10.5, "Utilisateur", fontsize=10)
    draw_actor(ax, 20.5, 10.5, "Administrateur", fontsize=10)

    # ---- S'authentifier (central) ----
    auth_x, auth_y = 11, 12.5
    draw_ellipse(ax, auth_x, auth_y, 3.2, 0.9, "S'authentifier",
                 fontsize=10, bg="#E8F5E9", border="#2E7D32")

    # Actor -> S'authentifier
    draw_solid_arrow(ax, 2.2, 11.25, auth_x - 1.6, auth_y)
    draw_solid_arrow(ax, 19.8, 11.25, auth_x + 1.6, auth_y)

    # ---- USER USE CASES ----
    # Main user use cases branching from S'authentifier
    user_cases = [
        (5.5,  10.3, "Rechercher\nitinéraire"),
        (5.5,  7.8,  "Consulter\nhistorique"),
        (5.5,  5.5,  "Gérer\nfavoris"),
        (5.5,  3.2,  "Voir détails\ntrajet"),
        (11.0, 3.2,  "Voir\nalternatives"),
    ]
    ell_w, ell_h = 2.8, 0.85
    for (cx, cy, lbl) in user_cases:
        draw_ellipse(ax, cx, cy, ell_w, ell_h, lbl, fontsize=8.5)
        draw_include_arrow(ax, auth_x - 1.6, auth_y - 0.2, cx + ell_w / 2, cy)

    # Sub-includes for Rechercher itinéraire
    rechercher_x, rechercher_y = 5.5, 10.3
    sub_rechercher = [
        (4.5,  13.5, "Calculer\nitinéraire"),
        (4.5, 11.8,  "Estimer\ntemps"),
        (9.0, 13.5,  "Saisir départ/\ndestination"),
        (9.0, 11.8,  "Afficher\nrésultats"),
    ]
    sub_w, sub_h = 2.5, 0.78
    for (sx, sy, sl) in sub_rechercher:
        draw_ellipse(ax, sx, sy, sub_w, sub_h, sl, fontsize=7.5,
                     bg="#FFF8E1", border="#FBC02D")
        draw_include_arrow(ax, rechercher_x, rechercher_y + ell_h / 2, sx, sy - sub_h / 2)

    # Sub-includes for Gérer favoris
    gerer_fav_x, gerer_fav_y = 5.5, 5.5
    sub_fav = [
        (4.5,  7.0,  "Ajouter aux\nfavoris"),
        (4.5,  5.5,  "Consulter\nfavoris"),
        (4.5,  4.0,  "Supprimer\nfavori"),
    ]
    for (sx, sy, sl) in sub_fav:
        draw_ellipse(ax, sx, sy, sub_w, sub_h, sl, fontsize=7.5,
                     bg="#FFF8E1", border="#FBC02D")
        draw_include_arrow(ax, gerer_fav_x + ell_w / 2, gerer_fav_y, sx + sub_w / 2, sy)

    # ---- ADMIN USE CASES ----
    admin_cases = [
        (16.5, 10.3, "Gérer lignes\nde transport"),
        (16.5, 7.8,  "Gérer\nstations"),
        (16.5, 5.5,  "Gérer\nhoraires"),
    ]
    for (cx, cy, lbl) in admin_cases:
        draw_ellipse(ax, cx, cy, ell_w, ell_h, lbl, fontsize=8.5)
        draw_include_arrow(ax, auth_x + 1.6, auth_y - 0.2, cx - ell_w / 2, cy)

    # Sub-includes for Gérer lignes de transport
    lignes_x, lignes_y = 16.5, 10.3
    sub_lignes = [
        (17.5, 13.5, "Ajouter\nligne"),
        (17.5, 11.8, "Modifier\nligne"),
        (17.5, 10.3, "Supprimer\nligne"),
    ]
    for (sx, sy, sl) in sub_lignes:
        draw_ellipse(ax, sx, sy, sub_w, sub_h, sl, fontsize=7.5,
                     bg="#FFF8E1", border="#FBC02D")
        draw_include_arrow(ax, lignes_x + ell_w / 2, lignes_y + (sy - lignes_y) * 0.1,
                           sx - sub_w / 2, sy)

    # Sub-includes for Gérer stations
    stations_x, stations_y = 16.5, 7.8
    sub_stations = [
        (17.5, 9.0,  "Ajouter\nstation"),
        (17.5, 7.8,  "Modifier\nstation"),
        (17.5, 6.6,  "Supprimer\nstation"),
    ]
    for (sx, sy, sl) in sub_stations:
        draw_ellipse(ax, sx, sy, sub_w, sub_h, sl, fontsize=7.5,
                     bg="#FFF8E1", border="#FBC02D")
        draw_include_arrow(ax, stations_x + ell_w / 2, stations_y + (sy - stations_y) * 0.1,
                           sx - sub_w / 2, sy)

    # Sub-includes for Gérer horaires
    horaires_x, horaires_y = 16.5, 5.5
    sub_horaires = [
        (17.5, 6.6,  "Ajouter\nhoraire"),
        (17.5, 5.5,  "Modifier\nhoraire"),
        (17.5, 4.3,  "Supprimer\nhoraire"),
    ]
    for (sx, sy, sl) in sub_horaires:
        draw_ellipse(ax, sx, sy, sub_w, sub_h, sl, fontsize=7.5,
                     bg="#FFF8E1", border="#FBC02D")
        draw_include_arrow(ax, horaires_x + ell_w / 2, horaires_y + (sy - horaires_y) * 0.1,
                           sx - sub_w / 2, sy)

    # Legend
    ax.plot([4.5, 5.5], [1.6, 1.6], color="#555555", lw=1.2, linestyle="dashed")
    ax.annotate("", xy=(5.5, 1.6), xytext=(5.4, 1.6),
                arrowprops=dict(arrowstyle="-|>", color="#555555", lw=1.2))
    ax.text(5.7, 1.6, "<<include>>", va="center", fontsize=8, color="#555555", style="italic")
    ax.plot([8.0, 9.0], [1.6, 1.6], color="#333333", lw=1.5)
    ax.text(9.2, 1.6, "Association", va="center", fontsize=8, color="#333333")

    out_path = os.path.join(OUT_DIR, "use_case_diagram.png")
    plt.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"✅  Use case diagram saved → {out_path}")
    return out_path


# ---------------------------------------------------------------------------
# 2. Class Diagram  (without Segment)
# ---------------------------------------------------------------------------

CLASS_W = 3.2   # class box width
CLASS_H_HDR = 0.45  # header height
ATTR_H = 0.28   # per-attribute height


def draw_class_box(ax, x, y, name, attributes, methods=None, color="#1A237E", bg="#E8EAF6"):
    """Draw a UML class box. Returns total height."""
    if methods is None:
        methods = []
    n_attrs = len(attributes)
    n_meths = len(methods)
    total_h = CLASS_H_HDR + n_attrs * ATTR_H + (0.1 if n_meths == 0 else n_meths * ATTR_H + 0.1)

    # outer box
    box = FancyBboxPatch((x - CLASS_W / 2, y - total_h), CLASS_W, total_h,
                         boxstyle="square,pad=0", edgecolor=color,
                         facecolor=bg, lw=1.5, zorder=3)
    ax.add_patch(box)

    # header background
    hdr = FancyBboxPatch((x - CLASS_W / 2, y - CLASS_H_HDR), CLASS_W, CLASS_H_HDR,
                         boxstyle="square,pad=0", edgecolor=color,
                         facecolor=color, lw=0, zorder=4)
    ax.add_patch(hdr)

    # class name
    ax.text(x, y - CLASS_H_HDR / 2, name, ha="center", va="center",
            fontsize=9, fontweight="bold", color="white", zorder=5)

    # divider line after header
    sep_y = y - CLASS_H_HDR
    ax.plot([x - CLASS_W / 2, x + CLASS_W / 2], [sep_y, sep_y],
            color=color, lw=1, zorder=4)

    # attributes
    for i, attr in enumerate(attributes):
        ay = sep_y - (i + 0.6) * ATTR_H
        ax.text(x - CLASS_W / 2 + 0.12, ay, attr, ha="left", va="center",
                fontsize=7.5, color="#1A237E", zorder=5)

    # divider before methods
    if methods:
        meth_sep_y = sep_y - n_attrs * ATTR_H - 0.05
        ax.plot([x - CLASS_W / 2, x + CLASS_W / 2], [meth_sep_y, meth_sep_y],
                color=color, lw=1, zorder=4)
        for i, meth in enumerate(methods):
            my = meth_sep_y - (i + 0.6) * ATTR_H
            ax.text(x - CLASS_W / 2 + 0.12, my, meth, ha="left", va="center",
                    fontsize=7.5, color="#4A148C", zorder=5)

    return total_h


def draw_relationship(ax, x1, y1, x2, y2, label="", end_style="->",
                      color="#333333", label_offset=(0, 0.15)):
    """Draw a relationship arrow between two classes."""
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=end_style, color=color, lw=1.3))
    if label:
        mx = (x1 + x2) / 2 + label_offset[0]
        my = (y1 + y2) / 2 + label_offset[1]
        ax.text(mx, my, label, ha="center", va="center", fontsize=7,
                color="#555555", style="italic",
                bbox=dict(facecolor="white", edgecolor="none", pad=1))


def generate_class_diagram():
    fig, ax = plt.subplots(figsize=(26, 20))
    ax.set_xlim(0, 26)
    ax.set_ylim(0, 20)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    # Title
    ax.text(13, 19.5, "Diagramme de classe – TuniRoute",
            ha="center", va="center", fontsize=15, fontweight="bold", color="#1A237E")
    ax.axhline(19.2, color="#1A237E", lw=1.5, xmin=0.02, xmax=0.98)

    # ------------------------------------------------------------------
    # Place classes
    # Layout (cx, cy-top):
    #   Row 1 (y=18): Role(enum), Utilisateur, TypeTransport(enum)
    #   Row 2 (y=13): Favori,  Itinéraire,  Historique
    #   Row 3 (y=8.5): Trajet
    #   Row 4 (y=5.5): Station (left), LigneTransport (center-right), Horaire (right)
    # ------------------------------------------------------------------

    ENUM_COLOR = "#4A148C"
    ENUM_BG    = "#F3E5F5"

    # -- Role (enum) --
    role_x, role_y = 3.0, 18.5
    draw_class_box(ax, role_x, role_y, "<<enumeration>>\nRole",
                   ["USER", "ADMIN"], color=ENUM_COLOR, bg=ENUM_BG)

    # -- TypeTransport (enum) --
    tt_x, tt_y = 23.0, 18.5
    draw_class_box(ax, tt_x, tt_y, "<<enumeration>>\nTypeTransport",
                   ["METRO", "BUS", "TGM", "LOUAGE"], color=ENUM_COLOR, bg=ENUM_BG)

    # -- Utilisateur --
    util_x, util_y = 13.0, 18.5
    util_attrs = [
        "- id : Long",
        "- nom : String",
        "- prenom : String",
        "- email : String",
        "- motDePasse : String",
        "- role : Role",
    ]
    util_h = draw_class_box(ax, util_x, util_y, "Utilisateur", util_attrs)

    # -- Itinéraire --
    itin_x, itin_y = 13.0, 13.5
    itin_attrs = [
        "- id : Long",
        "- dateCreation : Date",
    ]
    itin_h = draw_class_box(ax, itin_x, itin_y, "Itinéraire", itin_attrs)

    # -- Favori --
    fav_x, fav_y = 6.5, 13.5
    fav_attrs = [
        "- id : Long",
    ]
    draw_class_box(ax, fav_x, fav_y, "Favori", fav_attrs)

    # -- Historique --
    hist_x, hist_y = 19.5, 13.5
    hist_attrs = [
        "- id : Long",
        "- date : Date",
    ]
    draw_class_box(ax, hist_x, hist_y, "Historique", hist_attrs)

    # -- Trajet --
    trajet_x, trajet_y = 13.0, 9.0
    trajet_attrs = [
        "- id : Long",
        "- dureeEstimee : Integer",
        "- distanceTotale : Double",
    ]
    trajet_h = draw_class_box(ax, trajet_x, trajet_y, "Trajet", trajet_attrs)

    # -- Station --
    station_x, station_y = 6.5, 5.5
    station_attrs = [
        "- id : Long",
        "- nom : String",
        "- latitude : Double",
        "- longitude : Double",
    ]
    station_h = draw_class_box(ax, station_x, station_y, "Station", station_attrs)

    # -- LigneTransport --
    ligne_x, ligne_y = 13.0, 5.0
    ligne_attrs = [
        "- id : Long",
        "- nom : String",
        "- typeTransport : TypeTransport",
    ]
    draw_class_box(ax, ligne_x, ligne_y, "LigneTransport", ligne_attrs)

    # -- Horaire --
    horaire_x, horaire_y = 19.5, 5.5
    horaire_attrs = [
        "- id : Long",
        "- heureDepart : Time",
        "- heureArrivee : Time",
    ]
    draw_class_box(ax, horaire_x, horaire_y, "Horaire", horaire_attrs)

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    # Utilisateur --has--> Role
    draw_relationship(ax, util_x - CLASS_W / 2, util_y - 0.22,
                      role_x + CLASS_W / 2, role_y - 0.22,
                      label="", end_style="-|>", color="#4A148C",
                      label_offset=(0, 0.18))
    ax.text((util_x - CLASS_W / 2 + role_x + CLASS_W / 2) / 2,
            util_y - 0.1, "role", ha="center", va="bottom", fontsize=7.5,
            color="#555555", style="italic")

    # LigneTransport --has--> TypeTransport
    draw_relationship(ax, ligne_x + CLASS_W / 2, ligne_y - 0.22,
                      tt_x - CLASS_W / 2, tt_y - (tt_y - ligne_y) * 0.85,
                      label="", end_style="-|>", color="#4A148C",
                      label_offset=(0, 0.18))

    # Utilisateur --1:N--> Itinéraire  (vertical)
    draw_relationship(ax, util_x, util_y - util_h,
                      itin_x, itin_y,
                      label="1  *", end_style="->", color="#333333",
                      label_offset=(0.35, 0.1))

    # Itinéraire --contains--> Trajet  (vertical)
    draw_relationship(ax, itin_x, itin_y - itin_h,
                      trajet_x, trajet_y,
                      label="1  1", end_style="->", color="#333333",
                      label_offset=(0.35, 0.1))

    # Trajet --depart--> Station
    draw_relationship(ax, trajet_x - CLASS_W / 2, trajet_y - 0.9,
                      station_x + CLASS_W / 2, station_y - 0.4,
                      label="départ", end_style="->", color="#1565C0",
                      label_offset=(0, 0.22))

    # Trajet --arrivee--> Station
    draw_relationship(ax, trajet_x - CLASS_W / 2, trajet_y - 1.3,
                      station_x + CLASS_W / 2, station_y - 0.8,
                      label="arrivée", end_style="->", color="#1565C0",
                      label_offset=(0, -0.22))

    # Favori --> Utilisateur
    draw_relationship(ax, fav_x + CLASS_W / 2, fav_y - 0.22,
                      util_x - CLASS_W / 2, util_y - (util_y - fav_y) * 0.55,
                      label="", end_style="->", color="#333333",
                      label_offset=(0, 0.18))
    ax.text((fav_x + CLASS_W / 2 + util_x - CLASS_W / 2) / 2, fav_y + 0.08,
            "utilisateur", ha="center", va="bottom", fontsize=7, color="#555555", style="italic")

    # Favori --> Itinéraire
    draw_relationship(ax, fav_x + CLASS_W / 2, fav_y - 0.5,
                      itin_x - CLASS_W / 2, itin_y - 0.5,
                      label="", end_style="->", color="#333333",
                      label_offset=(0, 0.18))
    ax.text((fav_x + CLASS_W / 2 + itin_x - CLASS_W / 2) / 2, fav_y - 0.38,
            "itinéraire", ha="center", va="bottom", fontsize=7, color="#555555", style="italic")

    # Historique --> Utilisateur
    draw_relationship(ax, hist_x - CLASS_W / 2, hist_y - 0.22,
                      util_x + CLASS_W / 2, util_y - (util_y - hist_y) * 0.55,
                      label="", end_style="->", color="#333333",
                      label_offset=(0, 0.18))
    ax.text((hist_x - CLASS_W / 2 + util_x + CLASS_W / 2) / 2, hist_y + 0.08,
            "utilisateur", ha="center", va="bottom", fontsize=7, color="#555555", style="italic")

    # Historique --> Itinéraire
    draw_relationship(ax, hist_x - CLASS_W / 2, hist_y - 0.5,
                      itin_x + CLASS_W / 2, itin_y - 0.5,
                      label="", end_style="->", color="#333333",
                      label_offset=(0, 0.18))
    ax.text((hist_x - CLASS_W / 2 + itin_x + CLASS_W / 2) / 2, hist_y - 0.38,
            "itinéraire", ha="center", va="bottom", fontsize=7, color="#555555", style="italic")

    # Horaire --> LigneTransport
    draw_relationship(ax, horaire_x, horaire_y - CLASS_H_HDR - len(horaire_attrs) * ATTR_H,
                      ligne_x + CLASS_W / 2, ligne_y - 0.22,
                      label="ligne", end_style="->", color="#333333",
                      label_offset=(0, 0.18))

    # Horaire --> Station (stationDepart, stationArrivee)
    draw_relationship(ax, horaire_x - CLASS_W / 2, horaire_y - 0.6,
                      station_x + CLASS_W / 2, station_y - 0.6,
                      label="stations", end_style="->", color="#333333",
                      label_offset=(0, 0.22))

    # Station --> LigneTransport  (many-to-many via Horaire)
    # (No direct line needed; Horaire mediates)

    # Legend
    legend_x, legend_y = 1.0, 2.5
    ax.text(legend_x, legend_y + 0.5, "Légende", fontsize=9,
            fontweight="bold", color="#1A237E")
    ax.annotate("", xy=(legend_x + 1.2, legend_y + 0.1),
                xytext=(legend_x, legend_y + 0.1),
                arrowprops=dict(arrowstyle="-|>", color="#4A148C", lw=1.3))
    ax.text(legend_x + 1.4, legend_y + 0.1, "réalise / hérite", va="center",
            fontsize=8, color="#4A148C")
    ax.annotate("", xy=(legend_x + 1.2, legend_y - 0.25),
                xytext=(legend_x, legend_y - 0.25),
                arrowprops=dict(arrowstyle="->", color="#333333", lw=1.3))
    ax.text(legend_x + 1.4, legend_y - 0.25, "association", va="center",
            fontsize=8, color="#333333")
    ax.annotate("", xy=(legend_x + 1.2, legend_y - 0.6),
                xytext=(legend_x, legend_y - 0.6),
                arrowprops=dict(arrowstyle="->", color="#1565C0", lw=1.3))
    ax.text(legend_x + 1.4, legend_y - 0.6, "navigabilité (départ/arrivée)",
            va="center", fontsize=8, color="#1565C0")

    out_path = os.path.join(OUT_DIR, "class_diagram.png")
    plt.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"✅  Class diagram saved → {out_path}")
    return out_path


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    generate_use_case_diagram()
    generate_class_diagram()
    print("\nBoth diagrams generated successfully.")
