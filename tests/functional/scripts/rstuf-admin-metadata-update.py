import json
import os
import sys
from tempfile import mkdtemp
from unittest import mock

from click.testing import CliRunner
from repository_service_tuf import Dynaconf, cli


def _run(input, selection):
    folder_name = mkdtemp()
    setting_file = os.path.join(folder_name, "rstuf.yml")
    context = {"settings": Dynaconf(), "config": setting_file}

    runner = CliRunner()

    # key selection
    cli.admin.helpers._select = mock.MagicMock()
    cli.admin.helpers._select.side_effect = selection

    output = runner.invoke(
        cli.admin.update.update,
        ["--in", "metadata/1.root.json", "--out"],
        input="\n".join(input),
        obj=context,
        catch_exceptions=False,
    )

    return output


def main():
    input_dict = json.loads(sys.argv[1])
    input = [v for k, v in input_dict.items() if not k.startswith("[select]")]
    selection = [v for k, v in input_dict.items() if k.startswith("[select]")]

    print("Using parameters:")
    print(json.dumps(input_dict, indent=2))
    output = _run(input, selection)

    print(f"\nExit code: {output.exit_code}")
    print("\nOutput: ")
    print(output.stdout)
    if output.stderr_bytes is not None:
        print(f"\nError\n: {output.stderr}")

    if output.exception:
        print(f"Exception: {output.exception}")
        print(f"Exception Info: {output.exc_info}")
        output.exc_info

    sys.exit(output.exit_code)


if __name__ == "__main__":
    main()
