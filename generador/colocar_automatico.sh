#!/bin/bash
# Coloca los ficheros del número publicado en sus tres destinos, SIN depender de que
# la app de Claude se abra. Lo lanza launchd (com.dmarzal.briefing-colocar).
#
# Hace exactamente los PASOS 0.1 y 0.1.b de la SKILL, en ese orden y sin lógica nueva:
#   1. sync.py          -> coloca lo que FALTE en local (y la copia del Escritorio del
#                          número más reciente, una sola vez).
#   2. recolocar_mac.py -> compara contenido (SHA-256) y refresca SOLO lo que cambió,
#                          para que una corrección republicada no deje copias viejas.
# Nunca usa rm. Es idempotente: si todo está al día, no hace nada.
set -u
REPO="$HOME/Documents/Claude/Briefing Cardiovascular/briefing-cardiovascular-repo"
LOG="$HOME/Library/Logs/briefing-colocar.log"
mkdir -p "$(dirname "$LOG")"
echo "=== $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG"
SYNC="$HOME/Library/Application Support/briefing-sync/sync.py"
if [ -f "$SYNC" ]; then
  /usr/bin/python3 "$SYNC" >> "$LOG" 2>&1 || echo "sync.py devolvio error" >> "$LOG"
else
  echo "sync.py no esta instalado; sigo con recolocar_mac.py" >> "$LOG"
fi
if [ -f "$REPO/generador/recolocar_mac.py" ]; then
  /usr/bin/python3 "$REPO/generador/recolocar_mac.py" --pull >> "$LOG" 2>&1 \
    || echo "recolocar_mac.py devolvio error" >> "$LOG"
else
  echo "NO ENCUENTRO EL REPO EN $REPO" >> "$LOG"
fi
