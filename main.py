import command_updater

if __name__ == "__main__":
    CU = command_updater.CommandUpdater()
    CU.import_repo("https://github.com/LOLBAS-Project/LOLBAS", "LOLBAS-project") #import and update LOLBAS repo
    CU.parse_repo("LOLBAS-project")
