# DSC565_A4.2
# LangChain – The Triage Step and the Main Agent

This is the code from the Part 8 slides as a Python script. It builds the two components of an email assistant with LangChain, LangGraph and OpenAI models: a triage step that sorts an email into ignore, notify or respond, and a main agent that answers questions and writes emails with three placeholder tools. Part 9 joins the two into one email agent. No real email is sent and no calendar is touched.

## What's in the folder

| File | What it is |
| --- | --- |
| `code.py` | The code from the slides. This is the file you run. |
| `prompts.py` | The prompts that `code.py` imports. |
| `requirements.txt` | The Python packages to install. |
| `.env` | Holds your OpenAI API key. |
| `.gitignore` | Keeps `.env` and `.venv` out of Git, so your key isn't committed by accident. |
| `.vscode/settings.json` | Makes VS Code use this folder's `.venv`, uses the Python extension's own handling of the Run Python File button, stops automatic environment activation from interrupting commands, and stops a Python prompt opened in this folder from importing `code.py` (details in the file). |

## What you need

- VS Code with the Python extension
- Python 3.10 to 3.14 (check with `python3 --version`; on Windows, `py --version`). Python 3.15 worked in testing only with a C compiler installed, because two packages have no ready-made Mac builds for it yet.
- An OpenAI API key from <https://platform.openai.com/account/api-keys>. Each run makes about 3 calls to the OpenAI API, which are charged to your account: one for the triage step and, in testing, two for the main agent.

## How to run it

1. **Unzip** `LangChain_Part_8_code.zip`. VS Code cannot run code from inside a ZIP.

2. **Open the folder.** In VS Code, choose **File > Open Folder** and pick the unzipped `LangChain_Part_8_code` folder, the one that directly contains `code.py`. If VS Code asks whether you trust the authors of the files in this folder, click **Yes, I trust the authors**. The Python extension does not run otherwise. VS Code may also warn that the default interpreter path could not be resolved. That is expected until step 3 creates `.venv`, so close the message and leave the setting as it is.

3. **Install the packages.** Choose **Terminal > New Terminal** and run these two commands.

   macOS or Linux:

   ```bash
   python3 -m venv .venv
   .venv/bin/python -m pip install -r requirements.txt
   ```

   Windows:

   ```powershell
   py -m venv .venv
   .venv\Scripts\python -m pip install -r requirements.txt
   ```

4. **Select the environment (Windows only).** On macOS and Linux, VS Code uses `.venv` by itself. On Windows, press `Ctrl+Shift+P`, run **Python: Select Interpreter** and choose the one that shows `.venv`.

5. **Add your key.** Open `.env`, paste your key straight after `OPENAI_API_KEY=` and save the file. If VS Code offers to enable `python.terminal.useEnvFile`, choose **Don't Show Again**. The script reads `.env` by itself.

6. **Run it.** Open `code.py` and click the **Run Python File** button (the triangle at the top right of the editor).

   You can also run it from the terminal with `.venv/bin/python code.py` (Windows: `.venv\Scripts\python code.py`).

## What you should see

The output appears in the terminal, in this order. The wording of the model's answers changes from run to run.

1. **Triage result for the example email:** the model's reasoning and its classification, which should be `respond` (slide 17).
2. **`agent_system_prompt`:** the prompt template, unfilled (slide 22).
3. **Main agent:** its answer to the availability question (slide 24). The times 9:00 AM, 2:00 PM and 4:00 PM are hard-coded in the calendar tool.

## How it differs from the slides

The script holds the code of slides 5 to 24, in the order of the slides. Where a slide shortens a line with `...`, the script has the full line. These are the only other differences:

- **`prompts.py` was recreated.** The slides import it, but the file was not part of the original material. Its text comes from the video for Part 8 and from the later notebooks of the same series. Its three prompts are word for word the same as in [a third-party copy of the file on GitHub](https://github.com/ankitmalik84/Agentic_Longterm_Memory/blob/e60135ebd7f01630f7c68bdc804a5fb05dc42a6f/langgraph/online-course/prompts.py), which also has a fourth prompt that this script does not use.
- **Two prints are commented out.** Slides 13 and 16 print the two triage prompt templates. In the script those two lines are present with a `#` in front, as in the original notebook. Remove the `#` to print them.
- **There is a check for the API key,** so a missing key gives a clear message instead of a long error.
- **The `.env` file is found from the script's location** rather than the current folder.
- **One library notice is hidden.** LangGraph 1.x marks `create_react_agent` as deprecated in favor of `langchain.agents.create_agent`. The function still works at the version in `requirements.txt`, so the script keeps the slides' call and hides only that notice.
- **Short labels are printed** above each result, because a script has no cells to separate them.
- **Imports are gathered at the top,** and only the ones this part uses. `TypedDict` and `Annotated` from slide 10 are first used in Part 9, and `Literal` is imported from `typing` rather than `typing_extensions`; the two are the same class.
- **Slide 24 writes the question as "whats my availability for tuesday?".** The script keeps the notebook's "what is my availability for tuesday?".

## If something goes wrong

| What you see | What to do |
| --- | --- |
| `ModuleNotFoundError: No module named ...` | If you typed `python3 code.py` yourself, use `.venv/bin/python code.py` as in step 6. Otherwise VS Code is not using `.venv`, or step 3 did not finish. Check that you opened the folder that directly contains `code.py` and that step 3 ended without errors. If it still fails, press `Cmd+Shift+P` (`Ctrl+Shift+P` on Windows), run **Python: Select Interpreter** and choose the one that shows `.venv`. |
| VS Code asks you to select a Python interpreter, or nothing happens when you click Run | Step 3 has not been done yet. Close the prompt, finish step 3 and click Run again. |
| `KeyboardInterrupt` or `^C` in the terminal | VS Code's automatic environment activation interrupted the command. Check that you opened the folder that directly contains `code.py`, then run the command again. |
| `KeyboardInterrupt` or `SyntaxError` right after you click Run, and the terminal shows `>>>` | A Python prompt is open in the terminal named Python, and the button typed its command into that prompt. Close that terminal with its trash icon and click Run again. |
| `OPENAI_API_KEY is not set` | Repeat step 5, and make sure the file is saved. |
| `401` and `Incorrect API key` | The key is wrong. If `OPENAI_API_KEY` is already set on your system, that value is used instead of the one in `.env`. |
| `429` | Your OpenAI account is out of credit or has hit a rate limit. |
| `Connection error` | Your computer cannot reach OpenAI. Check your internet connection or proxy. |
| The script runs twice or crashes after you add `breakpoint()` or use `pdb` | Python's debugger imports a standard module also named `code` and finds `code.py` instead. Use VS Code's debugger (F5), which is not affected. |
| `Could not open requirements file` during step 3 | The wrong folder is open. Repeat step 2 with the folder that directly contains `code.py`, then repeat step 3. You can delete the `.venv` folder created in the wrong place. |
| `Failed to build` during step 3 | Your Python is probably newer than 3.14, where two packages need a C compiler. Install Python 3.14 from <https://www.python.org/downloads/>, delete the `.venv` folder and repeat step 3 with `python3.14` in place of `python3`. |
| `No matching distribution found` during step 3 | Check `python3 --version` (on Windows, `py --version`). If it is below 3.10, install a Python from 3.10 to 3.14, delete the `.venv` folder and repeat step 3. If the version is fine, pip could not reach the internet, so check your connection or proxy and repeat step 3. |

## OpenAI model retirement

The script uses the slides' models, `gpt-4o-mini` and `gpt-4o`. [OpenAI has announced](https://developers.openai.com/api/docs/deprecations) that both will be removed from the API on January 14, 2027, and recommends `gpt-6-luna` as the replacement. After that date, change the model names in the `init_chat_model(...)` and `create_react_agent(...)` calls in `code.py`. The replacement has not been tested with this script.

## What has been tested

All testing was done on macOS. The Windows and Linux steps above have not been run.

- **VS Code:** steps 3, 5 and 6 in VS Code 1.142 with Python extension 2026.10, in two windows whose user settings had the Python Environments extension's setting on and off, using a local stand-in for the OpenAI API. The tests triggered the Run Python File command rather than clicking it, and the trust prompt in step 2 was not tested. A Python prompt typed into VS Code's terminal in this folder, on Python 3.14, did not run the script; with the last setting in `.vscode/settings.json` left at its default, it did (checked on the Part 9 folder, which ships the same settings file).
- **Python versions:** a fresh install and full run on each of Python 3.10 to 3.14 with the stand-in.
- **A real OpenAI run:** the code in this file ran once against the real OpenAI API on November 1, 2026, as part of the combined script of Parts 8 and 9 (Python 3.13), without errors. On its own, this part has been run only against the stand-in.
