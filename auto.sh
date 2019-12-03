#!/usr/bin/expect  -f
spawn sh /openvpn/openvpn-install.sh
expect {
		"Add" {send "1\r" ;exp_continue}
		"Tell" {send $argv\r ;exp_continue}
}

