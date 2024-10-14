#!/bin/bash

# Obține calea absolută a scriptului Python
repoPath=$(pwd)
pythonScript="$repoPath/checkInvalidURLs.py"

# Verificăm dacă scriptul Python există
if [[ ! -f $pythonScript ]]; then
    echo "Eroare: Scriptul checkInvalidURLs.py nu a fost găsit în $repoPath."
    exit 1
fi

# Verificăm sistemul de operare
case "$OSTYPE" in
  linux-gnu* | darwin*)
    # Pentru Linux și macOS
    profileFile="$HOME/.bashrc"
    aliasCommand="alias checkInvalidURL='python3 \"$pythonScript\"'"
    ;;
  msys* | mingw*)
    # Pentru Windows
    profileFile="$HOME/Documents/WindowsPowerShell/Microsoft.PowerShell_profile.ps1"
    aliasCommand="function checkInvalidURL { python3 \"$pythonScript\" }"
    ;;
  *)
    echo "Eroare: Sistemul de operare nu este suportat."
    exit 1
    ;;
esac

# Adăugăm aliasul în fișierul de profil corespunzător
if grep -q "checkInvalidURL" "$profileFile"; then
    echo "Aliasul checkInvalidURL este deja adăugat în $profileFile."
else
    echo "$aliasCommand" >> "$profileFile"
    echo "Aliasul checkInvalidURL a fost adăugat în $profileFile."
fi

# Aplicăm modificările
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    source "$profileFile"
else
    # Pentru Windows, utilizatorul trebuie să-și repornească PowerShell-ul
    echo "Pentru a aplica modificările, închide și redeschide PowerShell."
fi

echo "Setup-ul este complet! Poți folosi comanda 'checkInvalidURL' din orice director."
