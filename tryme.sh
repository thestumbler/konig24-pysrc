#!/bin/bash

# Accept input path
INPUT="$1"

# Resolve mount point to BSD name (e.g., disk8s1 → disk8)
if [[ "$INPUT" == /dev/* ]]; then
    BSD_NAME=$(basename "$INPUT")
elif [[ "$INPUT" == /Volumes/* ]]; then
    BSD_NAME=$(diskutil info "$INPUT" | awk -F': ' '/Device Node/ {print $2}' | xargs basename)
else
    echo "Please provide a valid /dev/diskXsY or /Volumes/ path"
    exit 1
fi

# Get the whole disk (e.g., disk8s1 → disk8)
WHOLE_DISK=$(diskutil info "$BSD_NAME" | awk -F': ' '/Part of Whole:/ {print $2}' | xargs)

echo "📦 Disk: $BSD_NAME (Whole: $WHOLE_DISK)"

# Use ioreg to find the USB device associated with this disk
USB_INFO=$(ioreg -p IOUSB -w0 -l | \
    awk -v disk="$WHOLE_DISK" '
    /"BSD Name" =/ {
        if ($NF == "\""disk"\"") {
            show=1
        } else {
            show=0
        }
    }
    show {
        print
    }
    show && /USB Serial Number|idVendor|idProduct/ {
        print
    }')

if [[ -z "$USB_INFO" ]]; then
    echo "⚠️ Could not find USB info via ioreg"
else
    echo "🔍 USB Device Info:"
    echo "$USB_INFO"
fi

# Optional: get USB bus and address using ioreg + IOService
echo
echo "🧩 Bus/Address (best-effort):"
ioreg -r -c IOUSBHostDevice -l | \
grep -B10 "$WHOLE_DISK" | \
grep -E '"USB Address"|"locationID"|SerialNumber' || \
echo "Could not determine bus/address from ioreg"
