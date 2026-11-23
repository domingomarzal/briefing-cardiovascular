#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Briefing Cardiovascular - sincronizacion Mac <- GitHub.

La generacion del numero semanal la hace una routine EN LA NUBE cada lunes (funciona con el
Mac apagado) y publica en GitHub. Este script corre en el Mac al iniciar sesion y cada 30 min,
hace git pull y coloca los ficheros donde el usuario los espera:

  briefing-cardiovascular-repo/nN/index.html              -> Briefing Cardiovascular_NN/Briefing Cardiovascular_NN.html
  briefing-cardiovascular-repo/nN/articulos-revisados.html -> Briefing Cardiovascular_NN/Briefing Cardiovascular_NN_articulos revisados.html
  briefing-cardiovascular-repo/nN/cardio-al-dia.html      -> UICAR/Cardio al dIA/Cardio al dia_NN.html  (+ copia en el Escritorio)

Es idempotente: solo copia lo que falta o ha cambiado. No borra nada del Escritorio (el usuario
lo gestiona a mano) y nunca escribe en el repo.
"""
import os, re, shutil, subprocess, sys, datetime, filecmp

HOME = os.path.expanduser("~")
PROJ = os.path.join(HOME, "Documents/Claude/Briefing Cardiovascular")
REPO = os.path.join(PROJ, "briefing-cardiovascular-repo")
UICAR = os.path.join(HOME, "Documents/UICAR/Cardio al dIA")
DESK = os.path.join(HOME, "Desktop")
LOG = os.path.join(HOME, "Library/Logs/briefing-sync.log")

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(LOG, "a", encoding="utf-8") as fh: fh.write(line + "\n")
    except Exception: pass

def run(args, cwd=None):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=180)
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()

def copy_if_new(src, dst):
    """Copia solo si el destino no existe o difiere. Devuelve True si copio."""
    if not os.path.exists(src): return False
    if os.path.exists(dst) and filecmp.cmp(src, dst, shallow=False): return False
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    return True

def recupera_pull(rc, out, err):
    """Intenta desbloquear un `git pull` que choca con ficheros sin seguimiento.

    Ocurrio de verdad el 09/11/2026: la nube publico unos scripts que ya existian
    en el Mac sin versionar, git aborto el merge y el usuario se quedo sin su
    numero. Aqui se apartan esos ficheros a una carpeta de cuarentena (con `mv`,
    NUNCA `rm`: el pipeline tiene prohibido borrar) y se reintenta UNA vez.
    """
    texto = (err or "") + (out or "")
    if "untracked working tree files would be overwritten" not in texto:
        return rc, out, err
    estorban = []
    for linea in texto.splitlines():
        f = linea.strip()
        if f.startswith(("\t", " ")) or (f and not f.endswith(":") and "/" in f or f.endswith((".py", ".json", ".html"))):
            cand = os.path.join(REPO, f.lstrip("\t "))
            if os.path.isfile(cand):
                estorban.append(f.lstrip("\t "))
    if not estorban:
        return rc, out, err
    cuarentena = os.path.join(HOME, "Library/Application Support/briefing-sync/apartados",
                              datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    for f in estorban:
        dst = os.path.join(cuarentena, f)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.move(os.path.join(REPO, f), dst)
        log(f"  apartado (no borrado) para desbloquear el pull: {f}")
    log(f"  copia de lo apartado en: {cuarentena}")
    return run(["git", "pull", "--ff-only"], cwd=REPO)

def main():
    if not os.path.isdir(REPO):
        log(f"ERROR: no existe el repo {REPO}"); return 1

    rc, out, err = run(["git", "pull", "--ff-only"], cwd=REPO)
    if rc != 0:
        rc, out, err = recupera_pull(rc, out, err)
    if rc != 0:
        # NO abortar. Un pull fallido (sin red, ficheros sin seguimiento que
        # estorban al merge, conflicto) no debe impedir colocar lo que YA esta
        # descargado: el 09/11/2026 un pull bloqueado dejo al usuario sin sus
        # ficheros pese a tener el numero en local. Se avisa y se sigue.
        log(f"AVISO: git pull fallo (rc={rc}): {(err or out).splitlines()[-1] if (err or out) else '?'}")
        log("  -> se continua con lo que ya hay en el repo local")
    if "Already up to date" not in out and "Ya está actualizado" not in out:
        log(f"git pull: {out.splitlines()[-1] if out else 'ok'}")

    nums = sorted(int(m.group(1)) for d in os.listdir(REPO)
                  if (m := re.fullmatch(r"n(\d+)", d)) and os.path.isdir(os.path.join(REPO, d)))
    if not nums:
        log("ERROR: no hay carpetas nXX en el repo"); return 1

    copied_any = False
    nuevos = set()
    for n in nums:                                   # recorre todos: rellena huecos antiguos tambien
        src_dir = os.path.join(REPO, f"n{n}")
        sub = os.path.join(PROJ, f"Briefing Cardiovascular_N{n}")
        pairs = [
            (os.path.join(src_dir, "index.html"),
             os.path.join(sub, f"Briefing Cardiovascular_N{n}.html")),
            (os.path.join(src_dir, "articulos-revisados.html"),
             os.path.join(sub, f"Briefing Cardiovascular_N{n}_artículos revisados.html")),
            (os.path.join(src_dir, "cardio-al-dia.html"),
             os.path.join(UICAR, f"Cardio al día_N{n}.html")),
        ]
        for src, dst in pairs:
            if copy_if_new(src, dst):
                log(f"  N{n}: colocado {os.path.basename(dst)}")
                copied_any = True
                nuevos.add(n)

        # Copia de conveniencia en el Escritorio SOLO del numero mas reciente y solo si no la
        # ha visto ya el usuario (si la borro a mano, no se vuelve a poner).
        if n == nums[-1]:
            uic = os.path.join(UICAR, f"Cardio al día_N{n}.html")
            desk = os.path.join(DESK, f"Cardio al día_N{n}.html")
            marker = os.path.join(UICAR, f".desk_N{n}")
            if os.path.exists(uic) and not os.path.exists(desk) and not os.path.exists(marker):
                shutil.copy2(uic, desk)
                open(marker, "w").close()          # marca: ya se puso una vez
                log(f"  N{n}: copia de comprobacion en el Escritorio")
                copied_any = True
            elif (os.path.exists(uic) and os.path.exists(desk)
                  and not filecmp.cmp(uic, desk, shallow=False)):
                # El numero se CORRIGIO despues de dejar la copia. Paso el 23/11/2026:
                # el Escritorio recibio el N24 a las 08:56 y el Destacado se rehizo a
                # las 10:20, asi que la copia se quedo con la version vieja y el marcador
                # impedia reponerla. Si la copia sigue ahi, se refresca; si el usuario la
                # borro, NO se repone (eso lo decide el).
                shutil.copy2(uic, desk)
                log(f"  N{n}: copia del Escritorio actualizada (el numero se corrigio)")
                copied_any = True

    if nuevos:
        avisa(max(nuevos))
    if not copied_any:
        log("sin novedades")
    return 0

def avisa(n):
    """Notificacion de macOS al colocar un numero nuevo.

    Sin esto el usuario no se entera de que el lunes ha funcionado: el 23/11/2026
    descubrio el fallo del N24 porque ECHO EN FALTA los ficheros, no porque nadie
    le avisara. El aviso cierra el circuito.
    """
    try:
        subprocess.run(["osascript", "-e",
            f'display notification "N{n} ya esta en su carpeta, en UICAR y en el Escritorio." '
            f'with title "Briefing Cardiovascular" subtitle "Numero {n} colocado"'],
            capture_output=True, timeout=20)
    except Exception:
        pass

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        log(f"EXCEPCION: {e}"); sys.exit(1)
