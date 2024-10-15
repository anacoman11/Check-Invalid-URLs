#!/bin/bash

repoPath=$(pwd)
pythonScript="$repoPath/checkInvalidURLs.py"

if [[ ! -f $pythonScript ]]; then
    echo "Error: Script checkInvalidURLs.py not found in $repoPath."
    exit 1
fi

if [ -n "$BASH_VERSION" ]; then
    profileFile="$HOME/.bashrc"
elif [ -n "$ZSH_VERSION" ]; then
    profileFile="$HOME/.zshrc"
else
    echo "Error: Unsupported shell. Please use bash or zsh."
    exit 1
fi

aliasCommand="alias checkInvalidURL='python3 \"$pythonScript\"'"

if grep -q "checkInvalidURL" "$profileFile"; then
    echo "The checkInvalidURL alias has already been added to $profileFile."
else
    echo "$aliasCommand" >> "$profileFile"
    echo "The checkInvalidURL alias has been added to $profileFile."
fi

source "$profileFile"

echo "The setup is complete! You can use the 'checkInvalidURL' command from any directory."

echo "Please restart your terminal to apply the changes globally."
