# DiskEmulator Documentation

Welcome to the DiskEmulator documentation! DiskEmulator is a Python-based tool designed to emulate disk operations and management in a simplified environment. This tool allows users to create, delete, format, and manage virtual disks with custom sector values, providing a unique way to understand and manipulate disk data.

## Features

- **Disk Creation and Deletion**: Easily create new disks with custom formats and sectors, and delete them when no longer needed.
- **Disk Selection and Visualization**: Select any created disk for operations and visualize its current state.
- **Disk Formatting**: Format disks with custom sector values.
- **Memory and Sector Management**: Display memory stats, move the cursor across sectors, increment or decrement sector values, and perform recursive increases.
- **Data Manipulation**: Find, replace, and sum sector values.
- **Utility Commands**: Clear the screen, copy disks, rename disks, and more.

## Commands

- `list`: Lists all disks.
- `nd <name> [format] [sectors]`: Creates a new disk with a custom number of sectors.
- `dd <name>`: Deletes a disk.
- `fd [name] [format] [sectors]`: Formats a disk with a custom number of sectors.
- `sd <name>`: Selects a disk.
- `vd`: Visualizes the selected disk.
- `dm`: Displays memory stats of the selected disk.
- `mv <position>`: Moves the cursor.
- `inc [amount]`: Increments the sector value by the specified amount, defaults to 1 if no amount given.
- `dec [amount]`: Decrements the sector value by the specified amount, defaults to 1 if no amount given.
- `ri [increase value]`: Recursively increases sector value, defaults to 1 if no value given.
- `sum`: Sums all sector values.
- `wc`: Writes changes to disk (Deprecated).
- `cs`: Clears the screen.
- `cp <source> <destination>`: Copies a disk to a new disk.
- `rn <old_name> <new_name>`: Renames a selected disk.
- `fn <value>`: Finds the first occurrence of a value in sectors and moves the cursor to it.
- `rp <old_value> <new_value>`: Replaces all occurrences of a value in sectors with a new value.

## Error Handling

DiskEmulator includes a comprehensive error handling system that provides feedback on various errors, such as disk not found, no disk selected, cursor position out of bounds, and more. Use the `help err` command for a detailed list of error codes and their meanings.

## Getting Started

To start using DiskEmulator, simply run the `main.py` file in your Python environment. You will be greeted with a `diskemulator>` prompt where you can start entering commands to manage your virtual disks.

Thank you for using DiskEmulator!
