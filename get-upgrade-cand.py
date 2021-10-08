# This script aims to improve system stability by only upgrading packages that have not seen further upgrades since the last time this script was run.
# For best results, run as superuser (required to install system packages via DNF), ideally once-weekly or thereabout.

import dnf
from pathlib import Path
import os.path
import numpy
import csv

# Needs to be received by a cli arg
last_upgrade_candidates_dir = Path("/var/upgrade_stable/")

# Initialize dnf
base = dnf.Base()
base.read_all_repos()
base.fill_sack()

# Gets current upgrade candidates
def current_upgrade_candidates():
    return [(pkg.name, pkg.version) for pkg in base.sack.query().upgrades()]

# Save upgrade candidates to file
def save_upgrade_candidates():
    if not os.path.exists(last_upgrade_candidates_dir):
        os.makedirs(last_upgrade_candidates_dir)
    with open(os.path.join(last_upgrade_candidates_dir, "last-upgrade-candidates.csv"), 'w', newline='') as file:
        csvwriter = csv.writer(file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerows(current_upgrade_candidates())

# Open results of last save_upgrade_candidates
def last_upgrade_candidates():
    try:
        with open(os.path.join(last_upgrade_candidates_dir, "last-upgrade-candidates.csv"), 'r', newline='') as file:
            csvreader = csv.reader(file, delimiter=' ', quotechar='|')
            return [tuple(row) for row in csvreader]
    except:
        return []

# Upgrade "stable packages" based on comparing the currently available upgrades to what was available 1 week ago. 
if os.path.isfile(last_upgrade_candidates_dir) and os.path.getsize(last_upgrade_candidates_dir) > 0:
    base.install([elem[0] for elem in set(current_upgrade_candidates()).intersection(last_upgrade_candidates())])
    base.resolve()
    base.download_packages(base.transaction.install_set)
    base.do_transaction()

save_upgrade_candidates()

base.close()