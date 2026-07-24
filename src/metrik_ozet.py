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
import random
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


def bootstrap_ci(birimler, istatistik, B=2000, seed=12345, alpha=0.05):
    """Birim (görev/aile) düzeyinde yeniden örneklemeli %95 güven aralığı.

    `birimler`: bağımsız örnekleme birimlerinin listesi (görev başına eşleştirilmiş
    değerler). Yeniden örnekleme GÖREV düzeyinde yapılır çünkü asıl belirsizlik
    modelin görev dağılımı üzerindeki değişkenliğinden gelir (hücre-içi 3-tekrar
    gürültüsünden değil). Deterministik: sabit seed => tekrarlanabilir aralık.

    Döner: (alt, üst) yüzdelik. CI sıfırı dışlıyorsa fark anlamlı sayılır.
    """
    rng = random.Random(seed)
    n = len(birimler)
    if n < 2:
        return (float("nan"), float("nan"))
    vals = []
    for _ in range(B):
        ornek = [birimler[rng.randrange(n)] for _ in range(n)]
        v = istatistik(ornek)
        if v == v:  # NaN değilse
            vals.append(v)
    if not vals:
        return (float("nan"), float("nan"))
    vals.sort()
    lo = vals[int((alpha / 2) * len(vals))]
    hi = vals[min(len(vals) - 1, int((1 - alpha / 2) * len(vals)))]
    return (lo, hi)


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
    # CI'ler görev düzeyinde eşleştirilmiş (en, tr) çiftlerinden bootstrap edilir.
    print("=" * 92)
    print("MANŞET 1+2: Kodlama yeteneği ve Türkçe vergisi (kanonik görevlerde)")
    print("  TR vergi = acc_en - acc_tr;  [.,.] = %95 GA;  * = GA sıfırı dışlıyor (anlamlı)")
    print("=" * 92)
    print(f"{'model':<20} {'pass@1':>7} {'acc_en':>7} {'acc_tr':>7} {'TR vergi':>9}  {'%95 GA':>16}")
    print("-" * 92)
    tax_tab = {}
    for md in modeller:
        genel = ort([r["pass_at_1"] for r in rows if r["model"] == md])
        # kanonik görev başına eşleştirilmiş (en, tr) pass@1
        per_gorev = defaultdict(dict)
        for r in rows:
            if r["model"] == md and r["variant_type"] == "canonical":
                per_gorev[r["gorev"]][r["dil"]] = r["pass_at_1"]
        ciftler = [(v["en"], v["tr"]) for v in per_gorev.values()
                   if "en" in v and "tr" in v]
        en = ort([e for e, _ in ciftler])
        tr = ort([t for _, t in ciftler])
        tax = en - tr
        lo, hi = bootstrap_ci(
            ciftler, lambda s: ort([e for e, _ in s]) - ort([t for _, t in s]))
        anlamli = "*" if (lo > 0 or hi < 0) else " "
        tax_tab[md] = tax
        print(f"{md:<20} {genel:>7.3f} {en:>7.3f} {tr:>7.3f} {tax:>+8.3f}{anlamli} "
              f"[{lo:+.3f},{hi:+.3f}]")

    # --- 3) İki-seviyeli ezber farkı ---
    # Adil karşılaştırma için yalnız her üç türe de sahip AİLELER kullanılır.
    aileler = defaultdict(set)
    for r in rows:
        aileler[r["canonical_id"]].add(r["variant_type"])
    tam_aile = {c for c, ts in aileler.items()
                if {"canonical", "parametric_story", "story_mutation"} <= ts}

    print()
    aile_list = sorted(tam_aile)
    print("=" * 92)
    print(f"MANŞET 3: İki-seviyeli ezber farkı (n={len(aile_list)} tam aile, tr+en)")
    print("  sığ  = canonical - parametric_story  (yalnız hikâye)")
    print("  derin= canonical - story_mutation    (ad/imza/değişken de);  * = %95 GA sıfırı dışlıyor")
    print("=" * 92)
    print(f"{'model':<18} {'canon':>6} {'param':>6} {'mut':>6} "
          f"{'sığ Δ (%95 GA)':>22} {'derin Δ (%95 GA)':>22}")
    print("-" * 92)
    for md in modeller:
        # aile başına varyant doğruluğu (tr+en ortalaması); birim = aile
        def acc_aile(c, vt):
            return ort([r["pass_at_1"] for r in rows
                        if r["model"] == md and r["variant_type"] == vt
                        and r["canonical_id"] == c])
        birimler = [(acc_aile(c, "canonical"), acc_aile(c, "parametric_story"),
                     acc_aile(c, "story_mutation")) for c in aile_list]
        c = ort([b[0] for b in birimler])
        p = ort([b[1] for b in birimler])
        s = ort([b[2] for b in birimler])
        sg_lo, sg_hi = bootstrap_ci(
            birimler, lambda B: ort([b[0] for b in B]) - ort([b[1] for b in B]))
        dr_lo, dr_hi = bootstrap_ci(
            birimler, lambda B: ort([b[0] for b in B]) - ort([b[2] for b in B]))
        sg_m = "*" if (sg_lo > 0 or sg_hi < 0) else " "
        dr_m = "*" if (dr_lo > 0 or dr_hi < 0) else " "
        print(f"{md:<18} {c:>6.3f} {p:>6.3f} {s:>6.3f} "
              f"{c-p:>+6.3f}{sg_m}[{sg_lo:+.2f},{sg_hi:+.2f}] "
              f"{c-s:>+6.3f}{dr_m}[{dr_lo:+.2f},{dr_hi:+.2f}]")

    # --- 3c) Tasarım hipotezinin TAM testi: derin gizleme sığdan DAHA MI çok
    # düşürüyor? Fark-farkı = derinΔ - sığΔ = (c-s)-(c-p) = p - s (aile başına).
    # CI sıfırı dışlar ve pozitifse hipotez o modelde doğrulanmış olur. ---
    print()
    print("  Fark-farkı (derinΔ - sığΔ = param - mutasyon), birim = aile:")
    print(f"  {'model':<18} {'derin-sığ':>10}  {'%95 GA':>16}  hipotez")
    for md in modeller:
        def acc_aile(c, vt):
            return ort([r["pass_at_1"] for r in rows
                        if r["model"] == md and r["variant_type"] == vt
                        and r["canonical_id"] == c])
        birimler = [(acc_aile(c, "parametric_story"), acc_aile(c, "story_mutation"))
                    for c in aile_list]
        fark = ort([b[0] for b in birimler]) - ort([b[1] for b in birimler])
        lo, hi = bootstrap_ci(
            birimler, lambda B: ort([b[0] for b in B]) - ort([b[1] for b in B]))
        karar = "doğrulandı" if lo > 0 else ("ters" if hi < 0 else "belirsiz")
        print(f"  {md:<18} {fark:>+10.3f}  [{lo:+.3f},{hi:+.3f}]  {karar}")

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
    tk = rows[0].get("tekrar", "?") if rows else "?"
    print(f"Not: pass_at_1 = tekrar={tk} örnek üzerinden ortalama (sıcaklık=0.4).")
    print("     Token vergisi > 1.0 ise Türkçe çözüm daha uzun/pahalı üretiliyor.")


if __name__ == "__main__":
    main()
