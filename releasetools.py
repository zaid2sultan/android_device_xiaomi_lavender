# Copyright (C) 2009 The Android Open Source Project
# Copyright (c) 2011, The Linux Foundation. All rights reserved.
# Copyright (C) 2019 The LineageOS Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import common
import re

def FullOTA_InstallBegin(info):
  AddImage(info, "super_dummy.img", "/tmp/super_dummy.img");
  flash_script = open("device/xiaomi/lavender/partitions/flash_super_dummy.sh", 'r').read()
  common.ZipWriteStr(info.output_zip, "install/bin/flash_super_dummy.sh", flash_script);
  info.script.AppendExtra('package_extract_file("install/bin/flash_super_dummy.sh", "/tmp/flash_super_dummy.sh");')
  info.script.AppendExtra('run_program("/sbin/sh", "/tmp/flash_super_dummy.sh");')
  return

def FullOTA_InstallEnd(info):
  OTA_InstallEnd(info)
  return

def IncrementalOTA_InstallEnd(info):
  OTA_InstallEnd(info)
  return

def AddImage(info, basename, dest):
  path = "IMAGES/" + basename
  if path not in info.input_zip.namelist():
    return

  data = info.input_zip.read(path)
  common.ZipWriteStr(info.output_zip, basename, data)
  info.script.AppendExtra('package_extract_file("%s", "%s");' % (basename, dest))


def OTA_InstallEnd(info):
  info.script.Print("Patching device-tree and verity images...")
  AddImage(info, "vbmeta.img", "/dev/block/bootdevice/by-name/vbmeta")
  return