import threading
import uvicorn
import bot

def run_uvicorn():
    uvicorn.run("pay:app", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # Thread ile bot ve uvicorn'u başlat
    bot_thread = threading.Thread(target=bot.run_bot, daemon=True)
    uvicorn_thread = threading.Thread(target=run_uvicorn,  daemon=True)

    uvicorn_thread.start()
    bot_thread.start()

    bot_thread.join()
    uvicorn_thread.join()
