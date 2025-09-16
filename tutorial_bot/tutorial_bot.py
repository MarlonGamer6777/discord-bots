try:
    import os, sys, atexit, requests, logging, tkinter as tk
    from discord.ext import commands
    import discord
    import threading, asyncio

    # --- pip installieren ---
    os.system('pip install discord.py requests')

    # --- Funktion, damit Dateien auch in der EXE gefunden werden ---
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS  # bei EXE
        except AttributeError:
            base_path = os.path.abspath(".")  # normal
        return os.path.join(base_path, relative_path)
    
    os.system('cls')

    # --- GUI Setup ---
    root = tk.Tk()
    root.title("Bot läuft")
    root.geometry("500x300")

    text_log = tk.Text(root, wrap="word", state="disabled", bg="black", fg="white")
    text_log.pack(fill="both", expand=True, padx=5, pady=5)

    def log(msg: str):
        text_log.config(state="normal")
        text_log.insert("end", msg + "\n")
        text_log.see("end")
        text_log.config(state="disabled")

    # --- Logging ---
    log_path = resource_path("discord.log")
    handler = logging.FileHandler(filename=log_path, encoding='utf-8', mode='w')
    logging.basicConfig(handlers=[handler], level=logging.DEBUG)

    # --- Discord Setup ---
    BOTNAME = "Marlons erster Discord Bot"
    os.system(f'title Not ready - Bot: {BOTNAME}')

    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    token = "MTQxNjg0MjYwOTMwNDgwMTQxMA.GKNBvF.fC0uclrUobu3Rwcq1x5wqbPCghlIZS43s5gyUo"  # <-- fest im Code WAS AUTOMATICALLY CHANGED BY DISCORD AFTER 5 SECS

    bot = commands.Bot(command_prefix='\\', intents=intents)

    # --- Firebase ---
    firebase_url = "https://multi-projekt-default-rtdb.firebaseio.com/bots/discord/yt_tutorial/is_bot_online.json"
    is_from_exe = True

    def set_bot_status(status: bool):
        payload = {
            "status": status,
            "is_from_exe": is_from_exe
        }
        try:
            requests.put(firebase_url, json=payload)
            log(f"[Firebase] Status gesetzt: {'Online' if status else 'Offline'}")
        except Exception as e:
            log(f"[Firebase] Fehler beim Setzen des Status: {e}")

    def check_if_online():
        try:
            resp = requests.get(firebase_url)
            data = resp.json()
            if data and data.get("status") == True:
                log("Bot ist bereits online!")
                input("Drücke Enter zum Beenden...")
                sys.exit()
        except Exception as e:
            log(f"[Firebase] Fehler beim Prüfen des Status: {e}")

    # --- Bot Status ---
    check_if_online()
    set_bot_status(True)
    atexit.register(lambda: set_bot_status(False))

    # --- Discord Events ---
    @bot.event
    async def on_ready():
        os.system(f'title Ready! - Bot: {bot.user.name}')
        log(f"Bot is ready! Bot: {bot.user.name}")

    @bot.command()
    async def hello(ctx):
        await ctx.send(f"Hallo {ctx.author.mention}")

    # --- Fenster schließen ---
    def on_close():
        log("Fenster geschlossen -> Bot offline setzen...")
        set_bot_status(False)
        try:
            asyncio.get_event_loop().stop()
        except:
            pass
        root.destroy()
        os._exit(0)

    root.protocol("WM_DELETE_WINDOW", on_close)

    # --- Bot in eigenem Thread starten ---
    def start_bot():
        try:
            bot.run(token, log_handler=handler, log_level=logging.DEBUG)
        except Exception as e:
            log(f"Bot Fehler: {e}")

    t = threading.Thread(target=start_bot, daemon=True)
    t.start()

    root.mainloop()

except Exception as e:
    try:
        set_bot_status(False)
    except:
        pass
    print(f"Ein Fehler ist aufgetreten:\n{e}")
    input("Drücke Enter zum fortfahren...")
