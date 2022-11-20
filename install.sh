#!/bin/bash

flatpak install --user flathub org.gnome.Platform//43 org.gnome.Sdk//43 -y
flatpak-builder --force-clean --install --user -y builddir com.charlieqle.RetroGameLauncher.json