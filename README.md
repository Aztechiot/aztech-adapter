# Aztech-adapter

Aztech Kyla smart plug/bulb adapter for Mozilla WebThings Gateway.

# Supported Devices

## Tested and Working

* Smart plugs
    * Smart Plug
## Untested but _Should Work_


# Unsupported Devices

## Kyla

# Requirements

If you're running this add-on outside of the official gateway image for the Raspberry Pi, i.e. you're running on a development machine, you'll need to do the following (adapt as necessary for non-Ubuntu/Debian):

```
sudo apt install python3-dev libnanomsg-dev
sudo pip3 install nnpy
sudo pip3 install git+https://github.com/mozilla-iot/gateway-addon-python.git
```
