# Speech Synthesis on Spotify Podcast data

Speech synthesis using Spotify's podcast dataset
https://podcastsdataset.byspotify.com/

See the synthesized results here:
https://www.notion.so/malyvsen/4967e4e8627b48f998b9524933764a21?v=645207dbb991489da6e881f06a7af622 

## Setup

After cloning the repo, create a virtual environment with [Poetry](https://python-poetry.org/):

- If you don't have Poetry, follow [these instructions](https://python-poetry.org/docs/#installation) to get it
- Run `poetry install` to set up a virtual environment

Run `poetry shell` to spawn a new shell within the virtual environment. Python will now see all the packages which are installed in the virtual environment, instead of those installed globally on your system.

To exit the shell, just do as you would with any shelld - `exit` or `ctrl+d`.

## Running the code

Within the virtual environment, run `guild run <operation>` to run a piece of the pipeline. You'll find a list of available operations by running `guild help`.

That operation will then run in an isloated directory made specifically for it. To take a look at the operations output, use `guild runs` to list all operations you have run and then `guild open <operation-number>` to open your file browser.

You can re-run an operation any number of times, its output will always be saved to a new directory (runs do not interfere with each other).

## Dev instructions

Whenever you want to use a new package in the project:

- Decide if it's a dev dependency or not. Dev dependencies are packages which aren't actually needed for running the code, only for development (eg. a linter).
- `poetry add <package>` or `poetry add --dev <package>`
- commit changes to `pyproject.toml` and `poetry.lock`

Whenever someone else changed dependencies and you pull the changes: `poetry install`.

When you want to add a `guild` operation:

- Write a Python script which does the actual thing
  - If there is something you might want to supply as a command-line argument, make it a global variable
  - If your script needs to use the output of another operation (eg. spectrogram generation will need the output of `download-audio`), just pretend that what you need is in the current working directory
  - Save the script's output to the current working directory as well
- Add the operation to `guild.yml`
  - If your script uses the output of another operation, specify the name of that resource in the `requires` attribute - for example, you could create a `spectrogram` operation which requires `audio`
    - The names of resources are to be found in the `resources` section of `guild.yml`
  - If your script produces output that you might want to use in another operation, register that fact in `resources` - for example, see how `download-audio` produces the `audio` resource
  - Use `flags-import: all` for `guild` to detect what your script wants as command-line arguments
- Commit the script and changes to `guild.yml`

You can always refer to the `guild` documentation [here](https://my.guild.ai/t/guild-ai-documentation/).

To make your code pretty on save, ask your editor to format it with `black` (installed as a dev dependency already). In VS Code, you can do this in the settings ("Editor: format on save").
