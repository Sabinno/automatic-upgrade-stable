import dnf
 
base = dnf.Base()
base.read_all_repos()
base.fill_sack()
 

for pkg in list(base.sack.query().upgrades()):
    print(pkg.name, pkg.version)
 
base.close()