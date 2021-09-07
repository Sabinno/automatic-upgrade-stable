#!/bin/bash
# This script aims to improve system stability by only upgrading packages that have not seen further upgrades after 1 week.
# For best results, only run as superuser, ideally once-weekly via cron.

[ ! -f /var/upgrade_stable/last-upgrades.txt ] && { mkdir -p /var/upgrade_stable; touch /var/upgrade_stable/last-upgrades.txt; first_run=true; }

# Gets current upgrade candidates and formats output
get_upgrade_candidates() {
        python3 /usr/local/sbin/upgrade_stable/get_dnf_upgrades.py | column -t -s ' '
}

# Outputs upgrade candidates to file.
save-upgrade-candidates() {
        dnf -q clean metadata && dnf -q makecache
        get_upgrade_candidates > /var/upgrade_stable/last-upgrades.txt
}

# Upgrade "stable packages" based on comparing the currently available upgrades to what was available 1 week ago.
[ $first_run ] && save-upgrade-candidates || dnf -y upgrade "$(get_upgrade_candidates | comm -12 /var/upgrade_stable/last-upgrades.txt - | awk '{printf "%s ",$1}')" && save-upgrade-candidates