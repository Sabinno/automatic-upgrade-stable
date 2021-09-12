# This script aims to improve system stability by only upgrading packages that have not seen further upgrades after 1 week.
# For best results, only run as superuser, ideally once-weekly via cron.

import dnf
import os.path
import numpy

# Needs to be received by a cli arg
last_upgrade_candidates_path = Path("/var/upgrade_stable/last-upgrade-candidates.txt")

# Initialize dnf
base = dnf.Base()
base.read_all_repos()
base.fill_sack()

# Gets current upgrade candidates
def get_upgrade_candidates():
    return [(pkg.name, pkg.version) for pkg in base.sack.query().upgrades()]

# Save upgrade candidates to file
def save_upgrade_candidates():
    with open(last_upgrade_candidates_path, 'w') as file
        file.writelines(get_upgrade_candidates())

# Upgrade "stable packages" based on comparing the currently available upgrades to what was available 1 week ago. 
if os.path.isfile(last_upgrade_candidates_path) and os.path.getsize(last_upgrade_candidates_path) > 0:
    current_upgrade_candidates = # Result of packages that are equal between get_upgrade_candidates() and upgrade candidates from file 
    base.install(current_upgrade_candidates)
    base.resolve()
    base.download_packages(base.transaction.install_set)
    base.do_transaction()


save_upgrade_candidates()

base.close()