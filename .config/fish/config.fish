
set -xU LC_ALL "C"

# User define alias

alias ..  "cd .."
alias ... "cd ../.."
alias l   "exa -la"
alias ls  "exa"
alias cat "bat"

alias dotconfig "/usr/bin/git --git-dir $HOME/.dotfiles/ --work-tree=$HOME"
