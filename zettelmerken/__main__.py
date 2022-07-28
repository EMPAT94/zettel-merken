import sys
from zettelmerken.core import main
from zettelmerken.helpers import add_systemd_units, remove_systemd_units

if "add_systemd_units" in sys.argv:
    add_systemd_units()
elif "remove_systemd_units" in sys.argv:
    remove_systemd_units()
else:
    main()
