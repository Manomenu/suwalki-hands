#!/usr/bin/env bash
# Sourced by scripts — do not call directly.

function menu {
	sttyb=$(stty -g)
	stty -icanon
	stty -echo
	tput civis >&2

	function pretty {
		tput setaf 2
		echo "$1"
		tput sgr0
	}

	function _menu {
		trap 'return' INT

		argc=${#@}
		i=1
		while true; do
			for item in "$@"; do
				if [ "${!i}" == "$item" ]
					then pretty " > $item"
					else echo   "   $item"
				fi
			done >&2

			read -t0.01
			read -n1 key
			if [ "$key" == $'\e' ]; then
				read -n2 key
			fi

			tput cuu $argc >&2
			tput ed        >&2

			if [ "$key" == "[A" ] || [ "$key" == "k" ]; then
				((i=(i-2+argc+argc)%argc+1))
			elif [ "$key" == "[B" ] || [ "$key" == "j" ]; then
				((i=i%argc+1))
			elif [ "$key" == "" ]; then
				pretty "${!i}" >&2
				echo "${!i}"
				break
			fi
		done
	}

	_menu "$@"

	tput cnorm >&2
	stty "$sttyb"
}
