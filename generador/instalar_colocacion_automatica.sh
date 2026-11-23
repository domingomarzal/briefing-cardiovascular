#!/bin/bash
# Instala el trabajo de launchd que coloca los ficheros del Briefing en sus destinos.
# Se ejecuta UNA SOLA VEZ. No pide contraseña (es un LaunchAgent de usuario, sin sudo).
#
#   bash "<repo>/generador/instalar_colocacion_automatica.sh"
#
# Para quitarlo:
#   launchctl bootout gui/$(id -u)/com.dmarzal.briefing-colocar
#   mv ~/Library/LaunchAgents/com.dmarzal.briefing-colocar.plist /tmp/
set -eu
REPO="$HOME/Documents/Claude/Briefing Cardiovascular/briefing-cardiovascular-repo"
GEN="$REPO/generador"
AGENTS="$HOME/Library/LaunchAgents"
LABEL="com.dmarzal.briefing-colocar"
[ -f "$GEN/colocar_automatico.sh" ] || { echo "No encuentro $GEN/colocar_automatico.sh"; exit 1; }
chmod +x "$GEN/colocar_automatico.sh"
mkdir -p "$AGENTS"
cp -f "$GEN/$LABEL.plist" "$AGENTS/$LABEL.plist"
launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$AGENTS/$LABEL.plist"
launchctl kickstart -k "gui/$(id -u)/$LABEL"
echo "Instalado y lanzado. Log: ~/Library/Logs/briefing-colocar.log"
echo "Comprobar estado:  launchctl print gui/$(id -u)/$LABEL | head -20"
