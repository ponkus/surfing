#!/bin/bash
# Revierte la limpieza de la tablet TJD (27/09/2026). Uso: bash revertir.sh
adb shell pm enable com.google.android.youtube
adb shell pm enable com.google.android.apps.youtube.music
adb shell pm enable com.google.android.videos
adb shell pm enable com.google.android.gm
adb shell pm enable com.google.android.calendar
adb shell pm enable com.google.android.contacts
adb shell pm enable com.google.android.apps.tachyon
adb shell pm enable com.google.android.apps.maps
adb shell pm enable com.google.android.apps.docs
adb shell pm enable com.google.android.apps.photosgo
adb shell pm enable com.google.android.apps.searchlite
adb shell pm enable com.google.android.apps.assistant
adb shell pm enable com.google.android.apps.wellbeing
adb shell pm enable com.google.android.feedback
adb shell cmd package install-existing com.opera.mini.native
# Ajustes (valores previos)
adb shell settings put global window_animation_scale 1.0
adb shell settings put global transition_animation_scale 1.0
adb shell settings delete global animator_duration_scale
adb shell settings put global stay_on_while_plugged_in 7
adb shell settings put system screen_off_timeout 60000
adb shell settings put system screen_brightness 255
