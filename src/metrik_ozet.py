#!/usr/bin/env python3
"""Gün 15 metrik motoru: büyük koşum sonuçlarından manşet metrikleri hesaplar.

Üç manşet:
  1) Saf kodlama yeteneği  -> model başına pass@1 (tr+en ortalaması)
  2) Türkçe vergisi        -> acc(en) - acc(tr)   (kanonik görevlerde)
  3) İki-seviyeli ezber farkı:
        sığ  = acc(canonical) - acc(parametric_story)   (yalnız hikâye değişir)
        derin= acc(canonical) - acc(story_mutation)     (ad/imza/değişken de değişir)

Girdi: results/*.ckpt.jsonl (hücre = görev×model×dil) + data/tasks/*.json (variant_type).
Ölçüm anında ajan çağrılmaz; sadece kayıtlı hücreler okunur.
"""
import json
import glob
import argparse
from collections import defaultdict


def gorev_meta():
    meta = {}
    for f in glob.glob("data/tasks/*.json"):
        d = json.load(open(f, encoding="utf-8"))
        meta[d["id"]] = {
            "variant_type": d.get("variant_type", "canonical"),
            "canonical_id": d.get("canonical_id", d["id"]),
        }
    return meta


def hucreleri_yukle(yol):
    rows = []
    for l in open(yol, encoding="utf-8"):
        l = l.strip()
        if not l or '"_tip"' in l:
            continue
        rows.append(json.loads(l))
    return rows


def ort(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--girdi", default="results/gun15_buyuk_kosum.ckpt.jsonl")
    args = ap.parse_args()

    meta = gorev_meta()
    rows = hucreleri_yukle(args.girdi)
    for r in rows:
        m = meta.get(r["gorev"], {"variant_type": "canonical", "canonical_id": r["gorev"]})
        r["variant_type"] = m["variant_type"]
        r["canonical_id"] = m["canonical_id"]

    modeller = sorted(set(r["model"] for r in rows))

    # --- 1) pass@1 (tüm görev, tr+en) ve 2) Türkçe vergisi (yalnız kanonik) ---
    print("=" * 78)
    print("MANŞET 1+2: Kodlama yeteneği ve Türkçe vergisi (kanonik görevlerde)")
    print("=" * 78)
    print(f"{'model':<20} {'pass@1(hepsi)':>13} {'acc_en':>8} {'acc_tr':>8} {'TR vergi':>9}")
    print("-" * 78)
    tax_tab = {}
    for md in modeller:
        genel = ort([r["pass_at_1"] for r in rows if r["model"] == md])
        kanon = [r for r in rows if r["model"] == md and r["variant_type"] == "canonical"]
        en = ort([r["pass_at_1"] for r in kanon if r["dil"] == "en"])
        tr = ort([r["pass_at_1"] for r in kanon if r["dil"] == "tr"])
        tax = en - tr
        tax_tab[md] = tax
        print(f"{md:<20} {genel:>13.3f} {en:>8.3f} {tr:>8.3f} {tax:>+9.3f}")

    # --- 3) İki-seviyeli ezber farkı ---
    # Adil karşılaştırma için yalnız her üç türe de sahip AİLELER kullanılır.
    aileler = defaultdict(set)
    for r in rows:
        aileler[r["canonical_id"]].add(r["variant_type"])
    tam_aile = {c for c, ts in aileler.items()
                if {"canonical", "parametric_story", "story_mutation"} <= ts}

    print()
    print("=" * 78)
    print(f"MANŞET 3: İki-seviyeli ezber farkı (n={len(tam_aile)} tam aile, tr+en)")
    print("  sığ  = canonical - parametric_story  (yalnız hikâye)")
    print("  derin= canonical - story_mutation    (ad/imza/değişken de)")
    print("=" * 78)
    print(f"{'model':<20} {'canon':>7} {'param':>7} {'mutasyon':>9} {'sığ Δ':>7} {'derin Δ':>8}")
    print("-" * 78)
    for md in modeller:
        def acc(vt):
            return ort([r["pass_at_1"] for r in rows
                        if r["model"] == md and r["variant_type"] == vt
                        and r["canonical_id"] in tam_aile])
        c, p, s = acc("canonical"), acc("parametric_story"), acc("story_mutation")
        print(f"{md:<20} {c:>7.3f} {p:>7.3f} {s:>9.3f} {c-p:>+7.3f} {c-s:>+8.3f}")

    # --- 3b) pass@1 vs pass@k: örnekleme kazancı. sıcaklık>0'da k örnekten
    # en az biri geçerse pass@k=1. pass@k - pass@1 farkı, modelin "arada bir
    # doğruyu bulabildiği ama kararlı üretemediği" görevlerin payını gösterir. ---
    print()
    print("=" * 78)
    print(f"MANŞET 3b: pass@1 vs pass@k (k={rows[0]['tekrar']}, tüm görev, tr+en)")
    print("=" * 78)
    print(f"{'model':<20} {'pass@1':>8} {'pass@k':>8} {'kazanç':>8}")
    print("-" * 78)
    for md in modeller:
        p1 = ort([r["pass_at_1"] for r in rows if r["model"] == md])
        pk = ort([r["pass_at_k"] for r in rows if r["model"] == md
                  and r.get("pass_at_k_gecerli", True)])
        print(f"{md:<20} {p1:>8.3f} {pk:>8.3f} {pk-p1:>+8.3f}")

    # --- 4) Token vergisi: Türkçe çözüm İngilizce'ye göre kaç kat/token daha
    # pahalı? Aynı görevin iki dilinde ortalama completion token'ı karşılaştırılır
    # (yalnız kanonik görevler, çünkü tr/en parite orada tam garanti). ---
    print()
    print("=" * 78)
    print("MANŞET 4: Token vergisi (kanonik görevlerde ort. completion token)")
    print("=" * 78)
    print(f"{'model':<20} {'tok_en':>8} {'tok_tr':>8} {'fark':>8} {'oran(tr/en)':>12}")
    print("-" * 78)
    for md in modeller:
        kanon = [r for r in rows if r["model"] == md and r["variant_type"] == "canonical"]
        te = ort([r.get("ort_completion_tok") for r in kanon if r["dil"] == "en"])
        tt = ort([r.get("ort_completion_tok") for r in kanon if r["dil"] == "tr"])
        oran = tt / te if te else float("nan")
        print(f"{md:<20} {te:>8.1f} {tt:>8.1f} {tt-te:>+8.1f} {oran:>12.2f}")

    print()
    print("Not: pass_at_1 = tekrar=3 örnek üzerinden ortalama (sıcaklık=0.4).")
    print("     Token vergisi > 1.0 ise Türkçe çözüm daha uzun/pahalı üretiliyor.")


if __name__ == "__main__":
    main()
