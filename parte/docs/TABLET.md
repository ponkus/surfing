# Tablet: preparación por ADB (para Claude Code)

Objetivo: dejar la **TJD MT-1025** liviana, dedicada a la app `parte/`, **sin root y de forma reversible**.
Esto lo ejecuta **Claude Code en la Mac de Maiky** (con la tablet conectada por USB). Maiky no es programador:
explicale cada paso en simple, **de a uno**, y esperá su confirmación cuando tenga que tocar la tablet.

## Decisiones ya tomadas (no reabrir sin hablar con Maiky)
- **No root, no firmware alternativo.** No hay ROMs mantenidas para TJD; desbloquear bootloader en Unisoc suele requerir clave del fabricante → riesgo de brick sin beneficio seguro. (Ver `DECISIONES.md`.)
- **Todo reversible**: se usa `pm disable-user` (se revierte con `pm enable`) y, solo para bloatware obvio de terceros, `pm uninstall -k --user 0` (se revierte con `cmd package install-existing <paquete>`). Nunca `pm uninstall` sin `--user 0`.
- **Google Play y Chrome se quedan**: Play Store actualiza Chrome/WebView (donde corre la app) y es de donde se instala Fully Kiosk.
- La batería se degradó por la descarga profunda: la limpieza no la arregla. La tablet va a vivir enchufada (protección de carga: plan ESP32 + relé, `PROYECTO.md`).

## 0. Requisitos en la Mac
```bash
brew install --cask android-platform-tools   # trae adb
adb version
```

## 1. Tablet: activar depuración USB (lo hace Maiky, de a un paso)
1. Ajustes → Acerca de la tablet → tocar **7 veces** "Número de compilación" (aparece "Ya sos desarrollador").
2. Ajustes → Sistema → Opciones de desarrollador → activar **Depuración por USB**.
3. Conectar la tablet a la Mac con un cable **de datos** (no solo carga). En la tablet aceptar "¿Permitir depuración USB?" → marcar "Permitir siempre".
4. En la Mac: `adb devices` debe listar el equipo como `device` (si dice `unauthorized`, falta aceptar el aviso en la tablet).

**Si el USB se corta o queda `offline`** (pasó el 27/09 con 2 cables y 2 puertos): usar **depuración inalámbrica** (misma red Wi-Fi).
Opciones de desarrollador → Depuración inalámbrica → activar → "Vincular dispositivo con código de vinculación". En la Mac:
```bash
adb pair <IP:puerto del cartel> <código>
adb mdns services                  # muestra el puerto de conexión (_adb-tls-connect)
adb connect <IP:puerto de conexión>
```
El puerto cambia cada vez que se reactiva la depuración inalámbrica.

## 2. Diagnóstico ANTES de tocar nada (guardar todo)
```bash
mkdir -p ~/tablet-tjd && cd ~/tablet-tjd
adb shell getprop ro.product.model ro.build.version.release ro.board.platform ro.hardware ro.soc.model ro.build.display.id > info.txt
adb shell cat /proc/meminfo | head -3 >> info.txt
adb shell dumpsys battery > bateria.txt
adb shell pm list packages -s | sort > paquetes_sistema.txt
adb shell pm list packages -3 | sort > paquetes_terceros.txt
adb shell pm list packages -d | sort > paquetes_deshabilitados_antes.txt
adb shell dumpsys batterystats --charged | grep -A 40 "Estimated power use" > consumo.txt
adb shell top -b -n 1 -m 15 > top.txt
```
Reportarle a Maiky: modelo, Android, chip (`ro.board.platform`/`ro.soc.model`), RAM, estado de batería (level, health, temperature) y qué consume más.
**Anotar chip, RAM y Android en `PROYECTO.md`** (sección Hardware).

## 3. Limpieza (armar la lista con `paquetes_*.txt`, mostrársela a Maiky y pedir OK antes de ejecutar)
Candidatos típicos a **deshabilitar** (`adb shell pm disable-user --user 0 <paquete>`), solo si existen:
- Google que no se usa: `com.google.android.youtube`, `com.google.android.apps.youtube.music`, `com.google.android.gm` (Gmail),
  `com.google.android.apps.maps`, `com.google.android.apps.docs` (Drive), `com.google.android.apps.photos`,
  `com.google.android.apps.tachyon` (Meet/Duo), `com.google.android.googlequicksearchbox` (app Google/Asistente),
  `com.google.android.apps.magazines`, `com.google.android.videos`, `com.google.android.apps.subscriptions.red` (Google One),
  `com.google.android.calendar`, `com.google.android.keep`, `com.google.android.apps.wellbeing`, `com.google.android.feedback`,
  `com.google.android.apps.messaging`, `com.google.android.dialer`, `com.google.android.contacts` (si no se usan).
- Apps del fabricante/terceros preinstaladas (juegos, "tienda" propia, limpiadores, antivirus falsos, navegador propio, `com.mobiletjd.*` si hay): **desinstalar para el usuario 0** (`pm uninstall -k --user 0`).

**NUNCA tocar** (rompe la tablet o la app):
`com.android.systemui`, `com.android.settings`, `com.android.chrome`, `com.google.android.webview`, `com.android.webview`,
`com.google.android.gms` (Play Services), `com.google.android.gsf`, `com.android.vending` (Play Store),
`com.android.packageinstaller` / `com.google.android.packageinstaller`, `com.android.providers.*`, `com.android.phone`,
el launcher (`*launcher*`), el teclado (`*inputmethod*`, `com.google.android.inputmethod.latin`), `com.android.shell`,
`com.android.permissioncontroller` / `com.google.android.permissioncontroller`, `com.android.bluetooth`, `com.android.networkstack*`,
cualquier cosa con `sprd`/`unisoc`/`mediatek`/`mtk`/`allwinner`/`softwinner` en el nombre (drivers del chip; **esta tablet es Allwinner**), `android`.
Tampoco las del fabricante (`com.yhk.*` —incluye el actualizador del sistema—, `com.DeviceTest`).
Si hay duda sobre un paquete: **no se toca**.

Guardar lo que se hizo:
```bash
adb shell pm list packages -d | sort > paquetes_deshabilitados_despues.txt
```
Y dejar un script `revertir.sh` con un `adb shell pm enable <paquete>` / `cmd package install-existing <paquete>` por cada cambio.

## 3b. Actualizaciones (lo que sí se puede)
- Android no se actualiza (ver `DECISIONES.md`). Lo que importa para la web se actualiza por Play Store:
  - **Android System WebView** (lo usa Fully Kiosk): `adb shell am start -a android.intent.action.VIEW -d "market://details?id=com.google.android.webview"` y que Maiky toque Actualizar.
  - Play Store trabado en versión vieja: Play Store → Configuración → Acerca de → "Actualizar Play Store".
- Exceptuar del ahorro de batería el navegador de la app: `adb shell cmd deviceidle whitelist +com.android.chrome` (y Fully Kiosk cuando se instale).
- Después de reiniciar, la depuración inalámbrica cambia de puerto: `adb mdns services` lo muestra y `adb connect <IP:puerto>` reconecta (ya vinculada, sin código).

## 4. Ajustes de rendimiento (reversibles)
```bash
adb shell settings put global window_animation_scale 0.5
adb shell settings put global transition_animation_scale 0.5
adb shell settings put global animator_duration_scale 0.5
adb shell settings put global stay_on_while_plugged_in 7     # pantalla siempre prendida enchufada (AC/USB/inalámbrico)
adb shell settings put system screen_off_timeout 1800000    # 30 min si está a batería
```
- Desactivar actualizaciones automáticas de apps en Play Store (lo hace Maiky en la app, o dejarlas solo por Wi-Fi).
- **No** activar "límite de procesos en segundo plano" (puede matar el navegador de la app).
- Brillo: automático o ~50 % (menos calor, menos consumo).

## 5. Después (siguiente etapa, no en esta sesión salvo que Maiky lo pida)
- Instalar **Fully Kiosk Browser** (Play Store) → URL `https://ponkus.github.io/surfing/parte/`, pantalla completa, arrancar al prender.
  (Chrome en esta tablet **no ofrece "Agregar a pantalla principal"**: el launcher no soporta accesos directos. Probado 27/09/2026.)
- Protección de batería: ESP32 + relé + MacroDroid (corta 80 %, reconecta 40 %).

## 6. Al terminar
Actualizar `ESTADO.md` (qué se hizo, datos de la tablet), `CHANGELOG.md` (quién: "Claude Code") y guardar en el repo
`parte/docs/tablet/` los `.txt` de diagnóstico y `revertir.sh` (sin datos personales: revisar que no haya cuentas/emails).
