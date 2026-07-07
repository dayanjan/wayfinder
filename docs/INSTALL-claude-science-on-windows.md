# Installing Claude Science on Windows — a no-Linux-knowledge guide

**Who this is for:** a scientist on a **Windows 10/11** machine who wants to run Anthropic's
**Claude Science** and has never used Ubuntu/Linux. Claude Science has no native Windows app yet —
it runs inside a lightweight Linux environment called **WSL** — but you do **not** need to learn
Linux, open a Linux terminal, or ever type a Linux password. **Every command below is pasted into
Windows Terminal (or PowerShell).** The only click-with-a-mouse step is signing in.

**Time:** ~15 minutes, most of it downloads. **You need:** a Claude plan that includes Claude
Science (Pro, Max, Team, or Enterprise). **The one trick** that makes this painless is in Step 3.

> Tip: open **Windows Terminal** (press `Start`, type "Terminal", Enter). Paste each block, press
> Enter, wait for it to finish, then do the next one.

---

## Step 1 — Turn on WSL and install Ubuntu (one time)

In Windows Terminal, run:

```powershell
wsl --install -d Ubuntu-24.04
```

- If Windows asks you to **reboot**, do it, then re-open Terminal.
- The first time Ubuntu launches it asks you to **create a username and password**. Pick anything
  simple and **write it down** — but with this guide you will **not need the password again**.
- Why Ubuntu **24.04**: Claude Science's security sandbox needs a recent version; 24.04 has it.

Check it worked:

```powershell
wsl -l -v
```

You should see `Ubuntu-24.04` with `VERSION 2`. (If you already had a distro just called `Ubuntu`
that is 24.04+, you can use that instead — substitute its name for `Ubuntu-24.04` everywhere below.)

## Step 2 — (Optional) give it more memory for big analyses

By default WSL is capped at a slice of your RAM. For heavy datasets, raise it. Create a small
config file (this example allows 32 GB — adjust to about half your RAM):

```powershell
@"
[wsl2]
memory=32GB
autoMemoryReclaim=gradual
"@ | Set-Content -NoNewline "$env:USERPROFILE\.wslconfig"
wsl --shutdown
```

`autoMemoryReclaim=gradual` hands unused memory back to Windows, so this isn't "lost." Skip this
step entirely if you're just trying it out.

## Step 3 — Install the prerequisites **without any password** (the trick)

Claude Science needs three small helper programs. Installing system software on Linux normally
means the `sudo` command, which stops and asks for your Linux password — and when you paste a
command from Windows, there's no place for that prompt to appear, so it just hangs.

**The fix:** run the install as Linux's built-in administrator account (`root`), which needs **no
password**. That's what `-u root` does. Paste this exactly:

```powershell
wsl -d Ubuntu-24.04 -u root -- bash -lc "apt-get update && apt-get install -y curl bubblewrap socat"
```

Plain English: *"run this setup as the Linux admin, quietly, no password."* You never type a
password and never open a Linux terminal. (Installing system packages as root is normal and safe —
`sudo` just does the same thing with an extra password step.)

## Step 4 — Install Claude Science itself

This one runs as **your** normal user (not root), because it installs into your own home folder —
so, again, no password:

```powershell
wsl -d Ubuntu-24.04 -- bash -lc "curl -fsSL https://claude.ai/install-claude-science.sh | bash && grep -q '.local/bin' ~/.bashrc || echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
```

It downloads Claude Science (~150 MB) and makes it runnable. Confirm:

```powershell
wsl -d Ubuntu-24.04 -- bash -lc "export PATH=\"\$HOME/.local/bin:\$PATH\"; claude-science --version"
```

You should see a version number (e.g. `claude-science 0.1.16`).

> Cautious? You can look at the installer before running it instead of piping it straight to
> `bash`: `wsl -d Ubuntu-24.04 -- bash -lc "curl -fsSL https://claude.ai/install-claude-science.sh -o ~/cs.sh; less ~/cs.sh"` (press `q` to quit), then run `bash ~/cs.sh`.

## Step 5 — Start it and sign in

Start the Claude Science program in the background:

```powershell
wsl -d Ubuntu-24.04 -- bash -lc "export PATH=\"\$HOME/.local/bin:\$PATH\"; claude-science serve --port 8765 --no-browser --detached"
```

Now get your personal sign-in link:

```powershell
wsl -d Ubuntu-24.04 -- bash -lc "export PATH=\"\$HOME/.local/bin:\$PATH\"; claude-science url"
```

- **Copy the whole `http://localhost:8765/?nonce=...` link** it prints and paste it into **Edge or
  Chrome** on Windows. (Windows and WSL share `localhost`, so it just works.)
- Click **Sign in**, then sign in with your Claude account. **Signing in is also the check that
  your plan includes Claude Science** — if it lets you in, you're set.
- The link is single-use and expires in ~3 minutes; if it stops working, run the `...url` command
  again for a fresh one.

## Step 6 — Give it your data

Claude Science reads fastest from inside its own Linux home folder. Copy a Windows folder of data
into it like this (change the two paths to your data folder and a name you like):

```powershell
wsl -d Ubuntu-24.04 -- bash -lc "mkdir -p ~/my-data && cp -r '/mnt/c/Users/<YourWindowsUser>/Documents/<YourDataFolder>/'* ~/my-data/ && ls -la ~/my-data"
```

Then in Claude Science just tell it: *"my data is in `~/my-data/`"*. (Your Windows `C:` drive is
visible to Linux as `/mnt/c`, which is why the path starts that way.)

---

## Coming back later

After a restart, bring Claude Science back up with one line, then get a fresh link:

```powershell
wsl -d Ubuntu-24.04 -- bash -lc "export PATH=\"\$HOME/.local/bin:\$PATH\"; claude-science serve --port 8765 --no-browser --detached; claude-science url"
```

## If something goes wrong

| Symptom | Fix |
|---|---|
| A command seems to **hang forever** | It's probably waiting for a Linux password. You used a command *without* `-u root` for something that needs admin. Press `Ctrl+C`, and for setup steps use the `-u root` form (Step 3). |
| `bwrap: ... user namespaces` or sandbox error | Your Ubuntu is too old. Confirm `wsl -l -v` shows 24.04+; if not, install `Ubuntu-24.04` (Step 1). |
| Sign-in is **rejected** | Your Claude plan may not include Claude Science, or you signed in with the wrong account. Use the account that has Pro/Max/Team/Enterprise. |
| The link says **expired** | Re-run the `...claude-science url` command for a new one and open it right away. |
| Out of memory on big data | Do Step 2 (raise the memory cap), then `wsl --shutdown` and start again. |

---

*Verified end-to-end on a Windows 11 machine on 2026-07-07 (Ubuntu 24.04.1, Claude Science 0.1.16),
including on a corporate-managed laptop with endpoint security — the sandbox ran fine. The
no-password `-u root` method is the key to a paste-only install with zero Linux knowledge.*
