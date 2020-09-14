"""Aztech adapter for Mozilla WebThings Gateway."""

from gateway_addon import Adapter, Database
from pyKyla import Discover, SmartBulb, SmartPlug, SmartStrip

from .aztech_device import AztechBulb, AztechPlug


_TIMEOUT = 3


class AztechAdapter(Adapter):
    """Adapter for Aztech smart home devices."""

    def __init__(self, verbose=False):
        """
        Initialize the object.

        verbose -- whether or not to enable verbose logging
        """
        self.name = self.__class__.__name__
        Adapter.__init__(self,
                         'aztech-adapter',
                         'aztech-adapter',
                         verbose=verbose)

        self.pairing = False
        self.start_pairing(_TIMEOUT)

    def _add_from_config(self):
        """Attempt to add all configured devices."""
        database = Database('aztech-adapter')
        if not database.open():
            return

        config = database.load_config()
        database.close()

        if not config or 'addresses' not in config:
            return

        for address in config['addresses']:
            try:
                dev = Discover.discover_single(address)
            except (OSError, UnboundLocalError) as e:
                print('Failed to connect to {}: {}'.format(address, e))
                continue

            if dev:
                self._add_device(dev)

    def start_pairing(self, timeout):
        """
        Start the pairing process.

        timeout -- Timeout in seconds at which to quit pairing
        """
        if self.pairing:
            return

        self.pairing = True

        self._add_from_config()

        for dev in Discover.discover(timeout=min(timeout, _TIMEOUT)).values():
            if not self.pairing:
                break

            self._add_device(dev)

        self.pairing = False

    def _add_device(self, dev):
        """
        Add the given device, if necessary.

        dev -- the device object from pyKyla
        """
        if isinstance(dev, SmartStrip):
            for idx, plug in dev.plugs.items():
                _id = 'aztech-' + dev.sys_info['children'][idx]['id']
                if _id not in self.devices:
                    device = AztechPlug(self, _id, plug, index=idx)
                    self.handle_device_added(device)

            return

        _id = 'aztech-' + dev.sys_info['deviceId']
        if _id not in self.devices:
            if isinstance(dev, SmartPlug):
                device = AztechPlug(self, _id, dev)
            elif isinstance(dev, SmartBulb):
                device = AztechBulb(self, _id, dev)
            else:
                return

            self.handle_device_added(device)

    def cancel_pairing(self):
        """Cancel the pairing process."""
        self.pairing = False
