#!/usr/bin/env python3
"""Gün 16 figürleri: koşum sonuçlarından advisor-ready grafikler üretir.

Üç figür (hepsi salt-okuma; ajan çağrılmaz, --girdi ile yeni koşuma yönlendirilir):
  1) Ölçek eğrisi        -> pass@1, model boyutuna göre (genel vs coder ailesi)
  2) Türkçe vergisi+CI   -> acc_en-acc_tr, %95 bootstrap güven aralığıyla
  3) Hata taksonomisi    -> TR vs EN başarısızlık türü (yanlış-mantık vergisi)

Renk/mark disiplini dataviz metodundan: kategorik hue'lar SABİT sırada, tek
eksen, ince marklar, doğrudan etiket, recessive grid. bootstrap_ci ve sinifla
mevcut modüllerden yeniden kullanılır (tek doğruluk kaynağı).
"""
import re
import glob
import argparse
from collections import defaultdict, Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from metrik_ozet import bootstrap_ci, gorev_meta, hucreleri_yukle, ort
from hata_taksonomisi import sinifla

# --- Palet (dataviz reference, light) ---
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS, SURF = "#e1e0d9", "#c3c2b7", "#fcfcfb"

plt.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": SURF,
    "savefig.facecolor": SURF, "font.size": 10.5,
    "axes.edgecolor": AXIS, "axes.linewidth": 1.0,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.labelcolor": INK2, "text.color": INK,
})


def _iskele(ax):
    """Recessive kroni: üst/sağ spine gizli, yalnız yatay grid, muted eksen."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)


def _boyut(model: str):
    """Model adından milyar-parametre boyutunu çeker (qwen2.5:1.5b -> 1.5)."""
    m = re.search(r"(\d+\.?\d*)b\b", model.split(":")[-1])
    return float(m.group(1)) if m else None


def yukle(girdi):
    meta = gorev_meta()
    rows = hucreleri_yukle(girdi)
    for r in rows:
        r["variant_type"] = meta.get(r["gorev"], {}).get("variant_type", "canonical")
    return rows


# --- FIGÜR 1: ölçek eğrisi -----------------------------------------------
def figur_olcek(rows, cikti):
    modeller = sorted(set(r["model"] for r in rows))
    p1 = {md: ort([r["pass_at_1"] for r in rows if r["model"] == md])
          for md in modeller}

    def aile(pred):
        pts = sorted((_boyut(md), p1[md], md) for md in modeller if pred(md))
        return [(x, y) for x, y, _ in pts if x is not None]

    genel = aile(lambda m: m.startswith("qwen2.5:"))
    coder = aile(lambda m: m.startswith("qwen2.5-coder:"))
    digerleri = [(_boyut(md), p1[md], md) for md in modeller
                 if not md.startswith("qwen2.5")]

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    _iskele(ax)
    # Bağlam: qwen dışı modeller muted noktalar
    for x, y, md in digerleri:
        ax.scatter([x], [y], s=42, color=MUTED, zorder=3)
        ax.annotate(md.split(":")[0], (x, y), textcoords="offset points",
                    xytext=(6, -10), color=MUTED, fontsize=8.5)
    # İki aile çizgisi (sabit hue sırası: genel=blue, coder=orange)
    for pts, renk, ad in [(genel, BLUE, "qwen2.5 (genel)"),
                          (coder, ORANGE, "qwen2.5-coder")]:
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        ax.plot(xs, ys, "-o", color=renk, linewidth=2, markersize=8, zorder=5,
                label=ad)
        ax.annotate(ad, (xs[-1], ys[-1]), textcoords="offset points",
                    xytext=(8, 4), color=renk, fontsize=9.5, fontweight="bold")

    ax.set_xticks([0.5, 1.5, 2, 3])
    ax.set_xlabel("Model boyutu (milyar parametre)")
    ax.set_ylabel("pass@1 (tüm görev, tr+en)")
    ax.set_title("Ölçek eğrisi: kodlama başarısı model boyutuna göre",
                 color=INK, fontweight="bold", loc="left", pad=12)
    ax.legend(frameon=False, loc="lower right", fontsize=9)
    fig.tight_layout()
    fig.savefig(cikti, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return cikti


# --- FIGÜR 2: Türkçe vergisi + %95 CI ------------------------------------
def figur_vergi(rows, cikti):
    modeller = sorted(set(r["model"] for r in rows))
    veri = []
    for md in modeller:
        per = defaultdict(dict)
        for r in rows:
            if r["model"] == md and r["variant_type"] == "canonical":
                per[r["gorev"]][r["dil"]] = r["pass_at_1"]
        ciftler = [(v["en"], v["tr"]) for v in per.values()
                   if "en" in v and "tr" in v]
        if not ciftler:
            continue
        tax = ort([e for e, _ in ciftler]) - ort([t for _, t in ciftler])
        lo, hi = bootstrap_ci(
            ciftler, lambda s: ort([e for e, _ in s]) - ort([t for _, t in s]))
        veri.append((md, tax, lo, hi, lo > 0 or hi < 0))
    veri.sort(key=lambda x: x[1])

    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.axvline(0, color=AXIS, linewidth=1.2, zorder=1)  # sıfır referansı

    ys = range(len(veri))
    for y, (md, tax, lo, hi, anlamli) in zip(ys, veri):
        renk = BLUE if anlamli else MUTED
        ax.errorbar(tax, y, xerr=[[tax - lo], [hi - tax]], fmt="o",
                    color=renk, ecolor=renk, elinewidth=2, capsize=4,
                    markersize=9 if anlamli else 7,
                    markerfacecolor=renk if anlamli else SURF, zorder=5)
        ax.annotate(f"{tax:+.2f}", (tax, y), textcoords="offset points",
                    xytext=(0, 10), ha="center", color=INK2, fontsize=8.5)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([md for md, *_ in veri])
    ax.set_xlabel("Türkçe vergisi  (acc_en − acc_tr)")
    ax.set_title("Türkçe vergisi ve %95 güven aralığı (kanonik görevler)",
                 color=INK, fontweight="bold", loc="left", pad=12)
    # Doğrudan açıklama: dolu=anlamlı, boş=CI sıfırı içeriyor
    ax.annotate("dolu nokta = %95 GA sıfırı dışlıyor (anlamlı);  boş = değil",
                xy=(0.5, -0.16), xycoords="axes fraction", ha="center",
                color=MUTED, fontsize=8.5)
    fig.tight_layout()
    fig.savefig(cikti, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return cikti


# --- FIGÜR 3: hata taksonomisi TR vs EN ----------------------------------
def figur_taksonomi(rows, cikti):
    dil_sinif = {"en": Counter(), "tr": Counter()}
    for r in rows:
        for o in r.get("ornekler", []):
            s = sinifla(o)
            if s != "gecti":
                dil_sinif[r["dil"]][s] += 1
    siniflar = ["yanlis_mantik", "runtime_import", "eksik_fonksiyon",
                "syntax", "timeout", "harness_hatasi"]
    siniflar = [s for s in siniflar if dil_sinif["en"][s] or dil_sinif["tr"][s]]
    etiket = {"yanlis_mantik": "yanlış-mantık", "runtime_import": "import/runtime",
              "eksik_fonksiyon": "eksik fonksiyon", "syntax": "sözdizimi",
              "timeout": "zaman aşımı", "harness_hatasi": "harness"}

    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ys = range(len(siniflar))
    h = 0.38
    # Sabit hue sırası: EN=blue, TR=orange
    for off, dil, renk in [(+h / 2, "en", BLUE), (-h / 2, "tr", ORANGE)]:
        vals = [dil_sinif[dil][s] for s in siniflar]
        ax.barh([y + off for y in ys], vals, height=h, color=renk,
                zorder=3, label=dil.upper())
        for y, v in zip(ys, vals):
            if v:
                ax.annotate(str(v), (v, y + off), textcoords="offset points",
                            xytext=(4, 0), va="center", color=INK2, fontsize=8)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([etiket[s] for s in siniflar])
    ax.invert_yaxis()
    ax.set_xlabel("başarısız örnek sayısı")
    ax.set_title("Başarısızlık türü: TR vs EN — Türkçe vergisi bir mantık vergisidir",
                 color=INK, fontweight="bold", loc="left", pad=12)
    ax.legend(frameon=False, loc="lower right", fontsize=9)
    fig.tight_layout()
    fig.savefig(cikti, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return cikti


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--girdi", default="results/gun15_buyuk_kosum.ckpt.jsonl")
    ap.add_argument("--dizin", default="results/figures")
    args = ap.parse_args()
    rows = yukle(args.girdi)
    print("Yüklendi:", len(rows), "hücre |", args.girdi)
    print(figur_olcek(rows, f"{args.dizin}/fig1_olcek_egrisi.png"))
    print(figur_vergi(rows, f"{args.dizin}/fig2_turkce_vergisi_ci.png"))
    print(figur_taksonomi(rows, f"{args.dizin}/fig3_hata_taksonomisi.png"))


if __name__ == "__main__":
    main()
