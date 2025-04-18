# DualBoot Installer for Xiaomi Pad 5 (nabu)
This repository generates ZIP installers (for Magisk/Recovery) to enable dual booting on the Xiaomi Pad 5.

There are two options for dual booting:

### 1. Using a magnetic cover:
- If the tablet is (re)booted with the `magnetic cover closed`, the Android kernel will start.
- If the tablet is (re)booted with the `magnetic cover open`, UEFI from [Project-Aloha](https://github.com/Project-Aloha/mu_aloha_platforms) will start.

### 2. Using a software boot manager (like [rEFInd](https://sourceforge.net/projects/refind/)):
- The tablet will always boot to the software boot menu with an option to `Reboot to Android`.
- When the `Reboot to Android` option is selected, the tablet will reboot, and the Android kernel will start.
### `SB` (Secure Boot enabled) and `NOSB` (Secure Boot disabled) installers are generated for both options. If you just plan to dualboot between Windows and Android you can easily choose the SECURE BOOT enabled `case` version. If you want to use the `boot manager` version check [custom-sb-keys](https://github.com/rodriguezst/nabu-dualboot-img/tree/custom-sb-keys?tab=readme-ov-file#how-to-add-your-own-secure-boot-keys-as-trusted-in-uefi) branch for the extra steps needed to build UEFI with your own keys and sign EFI binaries with those keys.

## Installation

1. Download the ZIP file in the variant you need (**`installer_{case/bootmanager}_{SB/NOSB}.zip`**) and flash it using Magisk Manager or TWRP recovery.
2. (For the software boot manager option only) Install the boot manager and the [`Reboot to Android`](https://github.com/rodriguezst/Reboot2AndroidPkg/releases) app in your EFI System Partition (ESP). For rEFInd, the partition should contain the following structure:
```
[ESP Partition]
└── EFI
    ├── BOOT
    │   ├── BOOTAA64.EFI (renamed from refindaa64.efi)
    │   ├── icons (rEFInd icons directory)
    │   └── refind.conf (rEFInd configuration file)
    └── android
        └── Reboot2Android.efi
```
## How it works

The Android kernel in `boot.img` is patched to include both the Android kernel and UEFI, along with a small selection logic to jump to a specific section of the binary (Android kernel or UEFI).

In the magnetic cover option, this selection logic checks the status of the magnetic sensor on the tablet to decide which section to boot.

In the boot manager option, the selection logic reads a specific memory address and checks if a certain pattern is present at that address. If the pattern is not found (as happens on every cold boot), UEFI is launched. When the `Reboot to Android` app is launched, that pattern is written to the memory address, and a warm reboot is triggered. On the next boot, the selection logic will find the matching pattern and boot the Android kernel.

## How to add your own Secure Boot keys as trusted in UEFI

1. Generate Secure Boot certificates:
```bash
openssl req -new -x509 -newkey rsa:2048 -keyout Db.key \
  -out Db.crt -nodes -days 3650 \
  -subj "/O=EFI Binaries/CN=yourname/"

openssl x509 -in Db.crt -out Db.der -outform DER
```
2. Fork this repo and replace `user.der` with your `Db.der`.
3. Sign EFI binaries (rEFInd, grub, Linux kernels...) with your key:
```bash
sbsign --key Db.key --cert Db.crt --output file.signed.efi file.efi
```

## Credits

[DualBootKernelPatcher](https://github.com/Project-Aloha/DualBootKernelPatcher)

[UEFI](https://github.com/Project-Aloha/mu_aloha_platforms)

[SurfaceDuo-Guides](https://github.com/WOA-Project/SurfaceDuo-Guides/blob/main/Install/DualBoot.md)
