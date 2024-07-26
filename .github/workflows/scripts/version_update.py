import toml
import sys
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Automatically update version in pytoml"
    )
    parser.add_argument("pytoml")

    parser.add_argument("--major", action="store_true")
    parser.add_argument("--minor", action="store_true")
    parser.add_argument("--patch", action="store_true")

    args = parser.parse_args()

    if args.patch or (not args.major and not args.minor):
        do_patch = True
    else:
        do_patch = False

    pytoml = toml.load(args.pytoml)

    major, minor, patch = pytoml["project"]["version"].split(".")

    print(f"Current version {major}.{minor}.{patch}")

    if args.major:
        print("Updating major")
        major = int(major) + 1
        patch = 0
        minor = 0

    if args.minor:
        print("Updating minor")
        minor = int(minor) + 1
        patch = 0

    if do_patch:
        print("Updating patch")
        patch = int(patch) + 1

    new_version = f"{major}.{minor}.{patch}"
    pytoml["project"]["version"] = new_version

    print(f"New version: {new_version}")

    with open(args.pytoml, "w") as new_toml:
        toml.dump(pytoml, new_toml)
