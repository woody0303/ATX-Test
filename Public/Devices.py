#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Public.ReadConfig import ReadConfig
from Public.ATX_Server import ATX_Server
import uiautomator2 as u2
import subprocess
import re


def get_devices():
    '''get the devices from Pubilc/config.ini devices list
    return alive devices'''
    devices_ip = ReadConfig().get_devices_ip()
    print('Connect devices from config devices IP list %s' % devices_ip)
    devices_list = []
    for i in devices_ip:
        try:
            device = u2.connect(i)
            if device.healthcheck():
                dict_tmp = device.device_info
                dict_tmp['ip'] = i
                devices_list.append(dict_tmp)
            else:
                print('The IP %s device is not alive,please checkout!' % i)
        except Exception as e:
            print('Raise ERROR %s\nThe IP %s device is not alive,please checkout!' % (e, i))
    return devices_list


def get_online_devices():
    '''get the devices from Pubilc/config.ini devices list
    return alive devices'''
    devices = ATX_Server(ReadConfig().get_server_url()).online_devices()
    # print('Connect devices from config devices IP list %s' % devices_ip)
    devices_list = []
    for i in devices:
        try:
            device = u2.connect(i['ip'])
            if device.healthcheck():
                devices_list.append(i)
            else:
                print('The device %s  is not alive,please checkout!' % i['udid'])
        except Exception as e:
            print('Raise ERROR %s\nThe IP %s device is not alive,please checkout!' % (e, i['udid']))
    return devices_list


def connect_devices():
    '''get the devices usb connected on PC
    return alive devices'''
    output = subprocess.check_output(['adb', 'devices'])
    pattern = re.compile(
        r'(?P<serial>[^\s]+)\t(?P<status>device|offline)')
    matches = pattern.findall(output.decode())
    valid_serials = [m[0] for m in matches if m[1] == 'device']

    if valid_serials:
        print('Connecting devices linked on PC %s' % valid_serials)
        devices_list = []
        for i in valid_serials:
            try:
                device = u2.connect(i)
                if device.healthcheck():
                    dict_tmp = device.device_info
                    devices_list.append(dict_tmp)
                else:
                    print('The serial %s device is not alive,please checkout!' % i)
            except Exception as e:
                print('Raise ERROR %s\nThe serial %s device is not alive,please checkout!' % (e, i))
        return devices_list
    if len(valid_serials) == 0:
        print("No avaliable android devices detected.")