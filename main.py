import os

class DiskEmulator:
    def __init__(self):
        self.selected_disk = None
        self.disk_format = "custom"  # Default disk format changed to custom
        self.cursor_position = (0, 0)  # Line number, Sector number

    def error_handler(self, errcode):
        print(f"diskemulator<ERR>> {errcode}. Refer to \"help err\" for more info.")

    def help(self, topic=None):
        help_messages = {
            "cmd": ("Available commands:\n"
                    "- list: Lists all disks\n"
                    "- nd <name> [format] [sectors]: Creates a new disk with a custom number of sectors\n"
                    "- dd <name>: Deletes a disk\n"
                    "- fd [name] [format] [sectors]: Formats a disk with a custom number of sectors\n"
                    "- sd <name>: Selects a disk\n"
                    "- vd: Visualizes the selected disk\n"
                    "- dm: Displays memory stats of the selected disk\n"
                    "- mv <position>: Moves the cursor\n"
                    "- inc [amount]: Increments the sector value by the specified amount, defaults to 1 if no amount given\n"
                    "- dec [amount]: Decrements the sector value by the specified amount, defaults to 1 if no amount given\n"
                    "- ri [increase value]: Recursively increases sector value, defaults to 1 if no value given\n"
                    "- sum: Sums all sector values\n"
                    "- wc: Writes changes to disk (Deprecated)\n"
                    "- cs: Clears the screen\n"
                    "- help cmd: Shows this command list\n"
                    "- help err: Shows error codes and their meanings\n"
                    "- cp <source> <destination>: Copies a disk to a new disk\n"
                    "- rn <old_name> <new_name>: Renames a selected disk\n"
                    "- fn <value>: Finds the first occurrence of a value in sectors and moves the cursor to it\n"
                    "- rp <old_value> <new_value>: Replaces all occurrences of a value in sectors with a new value\n"
                    "- Inline commands can be chained using '>>'"),
            "err": ("Error codes:\n"
                    "- ERR001: Disk not found\n"
                    "- ERR002: No disk selected\n"
                    "- ERR003: Cursor position out of bounds\n"
                    "- ERR004: Modification position out of bounds\n"
                    "- ERR005: Unknown command\n"
                    "- ERR006: Empty command\n"
                    "- ERR007: Python error occurred\n"
                    "- ERR008: Copy failed\n"
                    "- ERR009: Rename failed\n"
                    "- ERR010: Value not found\n"
                    "- ERR011: Replace failed")
        }
        print(help_messages.get(topic, "Invalid help topic. Use 'help cmd' for command help or 'help err' for error help."))

    def safe_execute(self, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            self.error_handler("ERR007")
            print(f"Python error: {e}")

    def list_disks(self):
        print("\n".join(file for file in os.listdir('.') if file.endswith('.mx')))

    def create_disk(self, name, format="custom", sectors=40):
        self.disk_format = format
        sectors = int(sectors)  # Convert sectors to integer
        sector_data = '0 ' * 10
        lines = sectors // 10
        with open(f"{name}.mx", 'w') as disk:
            disk.write((sector_data.rstrip() + '\n') * lines)

    def delete_disk(self, name):
        try:
            os.remove(f"{name}.mx")
        except FileNotFoundError:
            self.error_handler("ERR001")

    def format_disk(self, name=None, format="custom", sectors=40):
        if name is None and self.selected_disk is None:
            self.error_handler("ERR002")
            return
        self.disk_format = format
        disk_name = self.selected_disk if name is None else name
        sector_data = '0 ' * 10
        lines = sectors // 10
        with open(f"{disk_name}.mx", 'w') as disk:
            disk.write((sector_data.rstrip() + '\n') * lines)

    def select_disk(self, name):
        if os.path.exists(f"{name}.mx"):
            self.selected_disk = name
        else:
            self.error_handler("ERR001")

    def visualize_disk(self):
        if self.selected_disk is None:
            self.error_handler("ERR002")
            return
        line_num, sector_num = self.cursor_position
        with open(f"{self.selected_disk}.mx", 'r') as disk:
            for i, line in enumerate(disk):
                sectors = line.strip().split()
                if i == line_num and sector_num < len(sectors):
                    sectors[sector_num] = f"\033[1m\033[92m{sectors[sector_num]}\033[0m"  # Highlight selected sector
                print(' '.join(sectors))

    def display_memory_stats(self):
        if self.selected_disk is None:
            self.error_handler("ERR002")
            return
        with open(f"{self.selected_disk}.mx", 'r') as disk:
            content = disk.read()
            used_space = content.count(' ') + content.count('\n')
            max_capacity = 80  # Assuming custom format has a max capacity of 80
            print(f"Format: {self.disk_format}, Max. Capacity: {max_capacity}, Space Used: {used_space}/{max_capacity}")

    def move_cursor(self, position):
        if self.selected_disk is None:
            self.error_handler("ERR002")
            return

        line, sector = map(int, position.split('x'))
        disk_path = f"{self.selected_disk}.mx"
        with open(disk_path, 'r') as disk:
            lines = disk.readlines()
            max_lines = len(lines)
            sectors_per_line = len(lines[0].split()) if lines else 0

        if line < max_lines and sector < sectors_per_line:
            self.cursor_position = (line, sector)
            print(f"Cursor moved to line {line}, sector {sector}.")
        else:
            self.error_handler("ERR003")

    def find_value(self, value):
        if self.selected_disk is None:
            self.error_handler("ERR002")
            return
        found = False
        with open(f"{self.selected_disk}.mx", 'r') as disk:
            for i, line in enumerate(disk):
                sectors = line.strip().split()
                if value in sectors:
                    sector_index = sectors.index(value)
                    self.cursor_position = (i, sector_index)
                    print(f"Value {value} found at line {i}, sector {sector_index}.")
                    found = True
                    break
        if not found:
            self.error_handler("ERR010")

    def replace_value(self, old_value, new_value):
        if self.selected_disk is None:
            self.error_handler("ERR002")
            return
        try:
            with open(f"{self.selected_disk}.mx", 'r+') as disk:
                lines = disk.readlines()
                disk.seek(0)
                modified_lines = []
                for line in lines:
                    new_line = []
                    for value in line.strip().split():
                        if value == old_value:
                            overflow = int(new_value) - 9  # Assuming 9 is the max value
                            underflow = 0 - int(new_value)  # Assuming 0 is the min value
                            if overflow > 0:
                                new_line.append(str(overflow))
                            elif underflow > 0:
                                new_line.append(str(9 - underflow))
                            else:
                                new_line.append(new_value)
                        else:
                            new_line.append(value)
                    modified_lines.append(' '.join(new_line) + '\n')
                disk.writelines(modified_lines)
                print(f"All occurrences of {old_value} replaced with {new_value}.")
        except Exception as e:
            self.error_handler("ERR011")
            print(f"Replace error: {e}")

    def recursive_increase(self, amount=1):
        if self.selected_disk is None:
            self.error_handler("ERR002")
            return
        with open(f"{self.selected_disk}.mx", 'r+') as disk:
            lines = disk.readlines()
            disk.seek(0)
            disk.writelines([' '.join(str((int(value) + amount) % 10) for value in line.strip().split()) + '\n' for line in lines])
            print("All sector values increased.")

    def sum_sectors(self):
        if self.selected_disk is None:
            self.error_handler("ERR002")
            return
        with open(f"{self.selected_disk}.mx", 'r') as disk:
            total_sum = sum(int(value) for value in disk.read().replace('\n', ' ').split())
            print(f"Sum of all sectors: {total_sum}")

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Screen cleared.")

    def copy_disk(self, source, destination):
        try:
            with open(f"{source}.mx", 'r') as src:
                content = src.read()
            with open(f"{destination}.mx", 'w') as dest:
                dest.write(content)
            print(f"Disk {source} copied to {destination}.")
        except Exception as e:
            self.error_handler("ERR008")
            print(f"Copy error: {e}")

    def rename_disk(self, old_name, new_name):
        try:
            os.rename(f"{old_name}.mx", f"{new_name}.mx")
            print(f"Disk {old_name} renamed to {new_name}.")
        except Exception as e:
            self.error_handler("ERR009")
            print(f"Rename error: {e}")

    def increment_sector(self, amount=1):
        if self.selected_disk is None:
            self.error_handler("ERR002")
            return
        line_num, sector_num = self.cursor_position
        with open(f"{self.selected_disk}.mx", 'r+') as disk:
            lines = disk.readlines()
            disk.seek(0)
            for i, line in enumerate(lines):
                if i == line_num:
                    sectors = line.strip().split()
                    sectors[sector_num] = str((int(sectors[sector_num]) + amount) % 10)
                    lines[i] = ' '.join(sectors) + '\n'
            disk.writelines(lines)
            print(f"Sector value incremented by {amount}.")

    def decrement_sector(self, amount=1):
        if self.selected_disk is None:
            self.error_handler("ERR002")
            return
        line_num, sector_num = self.cursor_position
        with open(f"{self.selected_disk}.mx", 'r+') as disk:
            lines = disk.readlines()
            disk.seek(0)
            for i, line in enumerate(lines):
                if i == line_num:
                    sectors = line.strip().split()
                    sectors[sector_num] = str((int(sectors[sector_num]) - amount) % 10)
                    lines[i] = ' '.join(sectors) + '\n'
            disk.writelines(lines)
            print(f"Sector value decremented by {amount}.")

    def process_command(self, command):
        if not command:
            self.error_handler("ERR006")
            return
        # Split the command string into individual commands if inline commands are used
        inline_commands = command.split(" >> ")
        for cmd in inline_commands:
            cmd_parts = cmd.split()
            cmd_name, *args = cmd_parts
            command_mapping = {
                "list": self.list_disks,
                "nd": lambda: self.create_disk(*args),
                "dd": lambda: self.delete_disk(*args),
                "fd": lambda: self.format_disk(*args) if args else self.format_disk(),
                "sd": lambda: self.select_disk(*args),
                "vd": self.visualize_disk,
                "dm": self.display_memory_stats,
                "mv": lambda: self.move_cursor(*args),
                "ri": lambda: self.recursive_increase(int(args[0]) if args else 1),
                "sum": self.sum_sectors,
                "wc": lambda: print("The 'wc' command is deprecated. All changes are now written immediately."),
                "cs": self.clear_screen,
                "cp": lambda: self.copy_disk(*args),
                "rn": lambda: self.rename_disk(*args),
                "help": lambda: self.help(*args),
                "inc": lambda: self.increment_sector(int(args[0]) if args else 1),
                "dec": lambda: self.decrement_sector(int(args[0]) if args else 1),
                "fn": lambda: self.find_value(*args),
                "rp": lambda: self.replace_value(*args)
            }
            command_func = command_mapping.get(cmd_name, lambda: self.error_handler("ERR005"))
            self.safe_execute(command_func)

def main():
    emulator = DiskEmulator()
    while True:
        command = input("diskemulator> ").strip()
        if command:
            emulator.process_command(command)

if __name__ == "__main__":
    main()
