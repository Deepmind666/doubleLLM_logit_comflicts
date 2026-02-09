from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle


OUT_DIR = Path("patent_cn/05_drawings")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def add_box(ax, x, y, w, h, text, fontsize=9):
    rect = Rectangle((x, y), w, h, fill=False, linewidth=1.4, edgecolor="black")
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize)


def add_arrow(ax, x1, y1, x2, y2):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle="->",
            mutation_scale=12,
            linewidth=1.2,
            color="black",
        )
    )


def finalize(fig, name):
    fig.savefig(OUT_DIR / name, dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig1_system_architecture():
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis("off")

    add_box(ax, 0.5, 7.5, 2.8, 1.2, "101 Input\nNormalization")
    add_box(ax, 4.2, 8.0, 2.8, 1.0, "102A Model A")
    add_box(ax, 4.2, 6.6, 2.8, 1.0, "102B Model B")
    add_box(ax, 8.0, 7.3, 2.8, 1.2, "103 Proposition\nParsing")
    add_box(ax, 11.5, 7.3, 2.8, 1.2, "104 Alignment\nMatching")
    add_box(ax, 11.5, 5.6, 2.8, 1.2, "105 Divergence\nDetection")
    add_box(ax, 8.0, 5.6, 2.8, 1.2, "106 Structured\nDecoupling")
    add_box(ax, 4.5, 5.0, 2.8, 1.2, "107 Evidence\nAdjudication")
    add_box(ax, 8.0, 3.8, 2.8, 1.2, "108 Fusion Output")
    add_box(ax, 11.5, 3.8, 2.8, 1.2, "109 Audit\nCompliance")
    add_box(ax, 4.2, 3.2, 2.8, 1.2, "110 Budget\nIteration")

    add_arrow(ax, 3.3, 8.1, 4.2, 8.5)
    add_arrow(ax, 3.3, 8.1, 4.2, 7.1)
    add_arrow(ax, 7.0, 8.5, 8.0, 7.9)
    add_arrow(ax, 7.0, 7.1, 8.0, 7.7)
    add_arrow(ax, 10.8, 7.9, 11.5, 7.9)
    add_arrow(ax, 12.9, 7.3, 12.9, 6.8)
    add_arrow(ax, 11.5, 6.2, 10.8, 6.2)
    add_arrow(ax, 8.0, 6.2, 7.3, 5.6)
    add_arrow(ax, 7.3, 5.6, 8.0, 4.4)
    add_arrow(ax, 10.8, 4.4, 11.5, 4.4)
    add_arrow(ax, 7.0, 3.8, 8.0, 4.2)
    add_arrow(ax, 10.8, 4.4, 7.0, 3.8)

    ax.text(0.5, 9.4, "Fig.1 System Architecture", fontsize=12, weight="bold")
    finalize(fig, "fig1_system_architecture.png")


def fig2_method_flow():
    fig, ax = plt.subplots(figsize=(8, 14))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 24)
    ax.axis("off")

    steps = [
        "S1 Dual-model generation",
        "S2 Proposition parsing",
        "S3 Alignment and matching",
        "S4 Divergence detection",
        "S5 Structured decoupling",
        "S6 Evidence adjudication (opt.)",
        "S7 Fusion synthesis",
        "S8 Iterative convergence (opt.)",
    ]
    y = 21.5
    for idx, s in enumerate(steps):
        add_box(ax, 1.2, y, 7.6, 1.4, s, fontsize=10)
        if idx < len(steps) - 1:
            add_arrow(ax, 5.0, y, 5.0, y - 1.4)
        y -= 2.6

    add_box(ax, 1.2, 1.2, 7.6, 1.4, "Stop: |D| <= threshold or max iter/time", fontsize=9)
    add_arrow(ax, 5.0, 3.2, 5.0, 2.6)
    add_arrow(ax, 1.2, 3.2, 1.2, 8.5)
    ax.text(1.5, 5.8, "Not converged -> back to S2", fontsize=9)
    ax.text(0.7, 23.3, "Fig.2 Method Flow", fontsize=12, weight="bold")
    finalize(fig, "fig2_method_flow.png")


def fig3_disagreement_graph():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis("off")

    nodes = {
        "P1": (1.5, 6.0),
        "P2": (4.0, 6.3),
        "P3": (6.7, 5.8),
        "P4": (9.2, 6.2),
        "P5": (2.8, 3.5),
        "P6": (5.5, 3.0),
        "P7": (8.5, 3.4),
    }

    for name, (x, y) in nodes.items():
        add_box(ax, x - 0.6, y - 0.35, 1.2, 0.7, name, fontsize=9)

    edges = [
        ("P1", "P2", "entails"),
        ("P2", "P3", "conflicts"),
        ("P3", "P4", "depends"),
        ("P2", "P5", "conflicts"),
        ("P5", "P6", "depends"),
        ("P6", "P7", "conflicts"),
    ]

    for a, b, label in edges:
        x1, y1 = nodes[a]
        x2, y2 = nodes[b]
        add_arrow(ax, x1, y1, x2, y2)
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.2, label, fontsize=8)

    ax.text(0.7, 7.3, "Fig.3 Divergence Graph", fontsize=12, weight="bold")
    finalize(fig, "fig3_disagreement_graph.png")


def fig4_decoupling_subquestions():
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis("off")

    add_box(ax, 4.5, 8.4, 3.0, 1.0, "Divergence D_01")
    add_box(ax, 1.1, 6.2, 3.0, 1.0, "q1: definition conflict?")
    add_box(ax, 4.5, 6.2, 3.0, 1.0, "q2: numeric boundary?")
    add_box(ax, 7.9, 6.2, 3.0, 1.0, "q3: missing premise?")
    add_box(ax, 1.1, 3.9, 3.0, 1.0, "J1: support A")
    add_box(ax, 4.5, 3.9, 3.0, 1.0, "J2: keep multi")
    add_box(ax, 7.9, 3.9, 3.0, 1.0, "J3: support B")
    add_box(ax, 4.1, 1.4, 3.8, 1.1, "Fusion F + Mapping")

    for x in [2.6, 6.0, 9.4]:
        add_arrow(ax, 6.0, 8.4, x, 7.2)
    add_arrow(ax, 2.6, 6.2, 2.6, 4.9)
    add_arrow(ax, 6.0, 6.2, 6.0, 4.9)
    add_arrow(ax, 9.4, 6.2, 9.4, 4.9)
    add_arrow(ax, 2.6, 3.9, 5.8, 2.5)
    add_arrow(ax, 6.0, 3.9, 6.0, 2.5)
    add_arrow(ax, 9.4, 3.9, 6.2, 2.5)

    ax.text(0.8, 9.4, "Fig.4 Decoupling Sub-questions", fontsize=12, weight="bold")
    finalize(fig, "fig4_decoupling_subquestions.png")


def fig5_iteration_feedback_loop():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis("off")

    add_box(ax, 1.0, 3.4, 2.6, 1.2, "Model A/B Output")
    add_box(ax, 4.0, 3.4, 2.6, 1.2, "Divergence Detect")
    add_box(ax, 7.0, 3.4, 2.6, 1.2, "Evidence Judge")
    add_box(ax, 10.0, 3.4, 1.6, 1.2, "Fusion")
    add_box(ax, 4.5, 6.0, 3.0, 1.0, "Convergence Check")
    add_box(ax, 1.2, 1.0, 3.2, 1.0, "Budget / Stop Rule")

    add_arrow(ax, 3.6, 4.0, 4.0, 4.0)
    add_arrow(ax, 6.6, 4.0, 7.0, 4.0)
    add_arrow(ax, 9.6, 4.0, 10.0, 4.0)
    add_arrow(ax, 10.8, 4.6, 6.0, 6.0)
    add_arrow(ax, 5.0, 6.0, 2.2, 4.6)
    add_arrow(ax, 6.0, 3.4, 2.8, 2.0)

    ax.text(0.8, 7.1, "Fig.5 Iterative Feedback Loop", fontsize=12, weight="bold")
    finalize(fig, "fig5_iteration_feedback_loop.png")


def fig6_data_structure():
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis("off")

    add_box(ax, 0.8, 6.8, 3.6, 1.4, "PropositionUnit\nunit_id/topic/type/text")
    add_box(ax, 5.2, 6.8, 3.6, 1.4, "MatchPair\npair_id/scores")
    add_box(ax, 9.6, 6.8, 3.6, 1.4, "DivergencePoint\ntype/confidence")

    add_box(ax, 0.8, 4.2, 3.6, 1.4, "SubQuestion\nverifiable/retrievable")
    add_box(ax, 5.2, 4.2, 3.6, 1.4, "JudgmentRecord\nJ_d/decision/evidence")
    add_box(ax, 9.6, 4.2, 3.6, 1.4, "FusionOutput\nconsensus/divergence")

    add_box(ax, 5.0, 1.2, 4.0, 1.6, "AuditLog\nprivacy/bias/illegal/timestamp")

    add_arrow(ax, 4.4, 7.5, 5.2, 7.5)
    add_arrow(ax, 8.8, 7.5, 9.6, 7.5)
    add_arrow(ax, 2.6, 6.8, 2.6, 5.6)
    add_arrow(ax, 7.0, 6.8, 7.0, 5.6)
    add_arrow(ax, 11.4, 6.8, 11.4, 5.6)
    add_arrow(ax, 7.0, 4.2, 7.0, 2.8)

    ax.text(0.8, 8.5, "Fig.6 Structured Output Schema", fontsize=12, weight="bold")
    finalize(fig, "fig6_data_structure.png")


def main():
    fig1_system_architecture()
    fig2_method_flow()
    fig3_disagreement_graph()
    fig4_decoupling_subquestions()
    fig5_iteration_feedback_loop()
    fig6_data_structure()
    print("Generated 6 figures in patent_cn/05_drawings/")


if __name__ == "__main__":
    main()
