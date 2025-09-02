import configparser

cfg_path = "setup.cfg"

config = configparser.ConfigParser()
config.read(cfg_path)

current_version = config["metadata"]["version"]
major, minor, patch = map(int, current_version.split("."))
patch += 1
new_version = f"{major}.{minor}.{patch}"

config["metadata"]["version"] = new_version
with open(cfg_path, "w") as f:
    config.write(f)

print(f"Version updated: {current_version} -> {new_version}")
