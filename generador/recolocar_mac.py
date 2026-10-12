#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RECOLOCAR en el Mac los ficheros de un número YA COLOCADO que se ha REGENERADO.

POR QUÉ EXISTE (12-oct-2026, N18). `sync.py` coloca «para CADA número publicado que
FALTE en local»: es idempotente *por existencia*, no por contenido. Si un número ya
se colocó y DESPUÉS se corrige y se republica (cambio de Destacado, de titulares, una
deduplicación, un linkfix…), sync.py lo ve «ya colocado» y NO lo refresca: la subcarpeta,
UICAR y el Escritorio se quedan con la versión vieja indefinidamente, mientras la web en
vivo ya está bien. Eso fue exactamente lo que pasó con N18: el Destacado se cambió por
decisión del usuario después de que el Mac hubiera colocado los ficheros.

Este script fuerza la recolocación de UN número, comparando contenido y sobrescribiendo
solo lo que de verdad ha cambiado.

Uso:   python3 generador/recolocar_mac.py <n> [--pull] [--escritorio] [--dry-run]
       --pull        hace `git pull` del repo antes de copiar
       --escritorio  fuerza la copia al Escritorio aunque no hubiera ninguna
       --dry-run     dice lo que haría, sin tocar nada

Destinos (reglas del usuario, PASO 8 de la SKILL):
  · subcarpeta  Briefing Cardiovascular_N<n>/  ->  SOLO el Briefing y la Auditoría
  · UICAR       ~/Documents/UICAR/Cardio al dIA/  ->  destino PERMANENTE del Cardio al día
  · Escritorio  copia temporal de comprobación (solo se REFRESCA si ya había una;
                si el usuario la borró, NO se resucita salvo --escritorio)
NUNCA usa rm/rmdir: solo copia (shutil.copy2), que sobrescribe en sitio.
"""
import sys, os, hashlib, shutil, subprocess

REPO_MAC = "/Users/dmarzal/Documents/Claude/Briefing Cardiovascular/briefing-cardiovascular-repo"
WORK_MAC = "/Users/dmarzal/Documents/Claude/Briefing Cardiovascular"

def sha(p):
    if not os.path.exists(p): return None
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def main():
    args = sys.argv[1:]
    nums = [a for a in args if a.isdigit()]
    pull  = "--pull" in args
    force_desk = "--escritorio" in args
    dry   = "--dry-run" in args

    repo = REPO_MAC if os.path.isdir(REPO_MAC) else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    work = WORK_MAC if os.path.isdir(WORK_MAC) else None
    uicar = os.path.expanduser("~/Documents/UICAR/Cardio al dIA")
    desk  = os.path.expanduser("~/Desktop")

    if work is None:
        raise SystemExit("Este script SOLO corre en el Mac: no existe %s.\n"
                         "(En la nube no hay acceso al disco del usuario: ahi no hay nada que recolocar.)" % WORK_MAC)
    if pull and not dry:
        print(subprocess.run(["git", "-C", repo, "pull", "--ff-only"], capture_output=True, text=True).stdout.strip())

    # Sin numeros explicitos: los ULTIMOS que haya publicados en el repo (por defecto 2).
    if not nums:
        k = 2
        if "--ultimos" in args:
            i = args.index("--ultimos")
            if i + 1 < len(args) and args[i + 1].isdigit(): k = int(args[i + 1])
        pub = sorted((int(d[1:]) for d in os.listdir(repo)
                      if d.startswith("n") and d[1:].isdigit()
                      and os.path.exists(os.path.join(repo, d, "index.html"))), reverse=True)
        nums = [str(x) for x in pub[:k]]
        print(f"Sin numero explicito: recoloco los {len(nums)} ultimos publicados -> N{', N'.join(nums)}\n")
    if not nums:
        raise SystemExit("No hay ningun numero publicado en " + repo)

    for n in nums:
        recoloca(n, repo, work, uicar, desk, force_desk, dry)

def recoloca(n, repo, work, uicar, desk, force_desk, dry):

    print(f"--- N{n} ---")
    sub = os.path.join(work, f"Briefing Cardiovascular_N{n}")
    plan = [
        (os.path.join(repo, f"n{n}", "index.html"),
         os.path.join(sub, f"Briefing Cardiovascular_N{n}.html"), True),
        (os.path.join(repo, f"n{n}", "articulos-revisados.html"),
         os.path.join(sub, f"Briefing Cardiovascular_N{n}_artículos revisados.html"), True),
        (os.path.join(repo, f"n{n}", "cardio-al-dia.html"),
         os.path.join(uicar, f"Cardio al día_N{n}.html"), True),
        (os.path.join(repo, f"n{n}", "cardio-al-dia.html"),
         os.path.join(desk, f"Cardio al día_N{n}.html"), False),   # solo si ya existe, o --escritorio
    ]
    cambios = iguales = saltados = 0
    for src, dst, obligatorio in plan:
        if not os.path.exists(src):
            print(f"  ! FALTA EN EL REPO: {src}"); continue
        if not obligatorio and not os.path.exists(dst) and not force_desk:
            print(f"  - Escritorio: no habia copia y no se resucita (usa --escritorio si la quieres) -> {dst}")
            saltados += 1; continue
        a, b = sha(src), sha(dst)
        if a == b:
            print(f"  = YA AL DIA  {dst}"); iguales += 1; continue
        estado = "ACTUALIZA" if b else "COLOCA   "
        print(f"  {'[dry] ' if dry else ''}{estado} {dst}")
        if not dry:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            assert sha(dst) == a, "la copia no coincide con el origen: " + dst
        cambios += 1
    # La subcarpeta NO debe conservar ningun Cardio al dia (regla del usuario)
    sobra = os.path.join(sub, f"Cardio al día_N{n}.html")
    if os.path.exists(sobra):
        print(f"  ! OJO: la subcarpeta tiene un Cardio al dia que no deberia estar: {sobra}")
        print("    muevelo a UICAR con mv (nunca rm).")
    print(f"\nN{n}: {cambios} fichero(s) {'a actualizar' if dry else 'actualizados'} · {iguales} ya al dia · {saltados} omitido(s)")
    if cambios and not dry:
        print("Abre uno y comprueba el Destacado: debe coincidir con "
              f"https://domingomarzal.github.io/briefing-cardiovascular/n{n}/")

if __name__ == "__main__":
    main()
