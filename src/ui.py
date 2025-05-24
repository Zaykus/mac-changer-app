class UserInterface:
    def __init__(self, mac_changer):
        self.mac_changer = mac_changer
        self.create_interface()

    def create_interface(self):
        # Simple CLI interface
        print("Welcome to the MAC Changer CLI (UI not implemented yet).")

    def display_options(self):
        # Display options for MAC address configuration
        print("Options:")
        print("1. Generate random MAC address")
        print("2. Change MAC address")
        print("3. Restore original MAC address")
        print("4. Exit")

    def handle_user_input(self):
        # Handle user input for changing MAC address
        while True:
            self.display_options()
            choice = input("Enter your choice: ")
            if choice == "1":
                print("Random MAC:", self.mac_changer.generate_random_mac())
            elif choice == "2":
                adapters = self.mac_changer.get_adapters()
                for idx, (_, desc, _) in enumerate(adapters):
                    print(f"{idx+1}. {desc}")
                idx = int(input("Select adapter: ")) - 1
                new_mac = input("Enter new MAC address (format: XX:XX:XX:XX:XX:XX): ")
                net_cfg_id, _, reg_path = adapters[idx]
                self.mac_changer.change_mac(net_cfg_id, reg_path, new_mac)
                print("MAC address changed.")
            elif choice == "3":
                adapters = self.mac_changer.get_adapters()
                for idx, (_, desc, _) in enumerate(adapters):
                    print(f"{idx+1}. {desc}")
                idx = int(input("Select adapter: ")) - 1
                net_cfg_id, _, reg_path = adapters[idx]
                self.mac_changer.restore_mac(net_cfg_id, reg_path)
                print("Original MAC address restored.")
            elif choice == "4":
                print("Exiting.")
                break
            else:
                print("Invalid choice.")

    def run(self):
        # Run the CLI interface
        self.handle_user_input()