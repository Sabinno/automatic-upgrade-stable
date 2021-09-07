import dnf

# Initialize dnf
base = dnf.Base()
base.read_all_repos()
base.fill_sack()

# Gets current upgrade candidates
for pkg in list(base.sack.query().upgrades()):
    print(pkg.name, pkg.version)

base.close()