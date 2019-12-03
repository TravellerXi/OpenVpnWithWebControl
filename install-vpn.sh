#!/usr/bin/expect  -f
spawn sh /openvpn/openvpn-install.sh
expect {
		"IP" {send "\r" ;exp_continue}
		"Protocol" {send "\r" ;exp_continue}
		"port" {send "\r" ;exp_continue}
		"DNS" {send "\r" ;exp_continue}
		"Client" {send "\r" ;exp_continue}
		"continue" {send "\r";exp_continue}
}

