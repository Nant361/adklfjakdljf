import asyncio
from telethon import TelegramClient, events

# Ganti dengan API ID dan API Hash dari my.telegram.org
api_id = 21960406
api_hash = "846bca703fc77480a7a7c9b02fe59b7d"

# Inisialisasi client dengan sesi bernama "my_session"
client = TelegramClient("my_session", api_id, api_hash)

async def main():
    await client.start()  # Login ke Telegram
    bot_username = "@ePhoneNIK_Bot"  # Username bot

    while True:  # Loop agar bisa mengirim banyak pesan
        # Meminta input dari pengguna
        message = input("Ketik pesan: ")

        # Jika pengguna mengetik "exit", keluar dari loop
        if message.lower() == "exit":
            print("Keluar dari program...")
            break

        # Membuat Future untuk menunggu balasan
        future = asyncio.Future()

        # Event listener untuk menangkap balasan dari bot
        @client.on(events.NewMessage(from_users=bot_username))
        async def handler(event):
            if not future.done():  # Pastikan hanya menangkap satu balasan
                future.set_result(event.message.text)

        # Kirim pesan ke bot
        await client.send_message(bot_username, message)
        print(f"Pesan terkirim ke server: {message}")

        # Menunggu balasan dari bot
        try:
            response = await asyncio.wait_for(future, timeout=20)
            
            # Ganti bagian teks "Welcome To ePhoneNIK Bot" dengan "Welcome To nant osint"
            response = response.replace("Welcome To ePhoneNIK Bot", "Welcome To nant osint")
            
            # Filter untuk menghapus informasi sensitif
            filtered_response = "\n".join([
                line for line in response.splitlines() 
                if not any(line.strip().startswith(prefix) for prefix in [
                    "ID Pengguna", "Nama", "Username", "Status"
                ])
            ])
            
            print(f"Response: {filtered_response}")
        except asyncio.TimeoutError:
            print("Request Time Out/coba lagi nanti")

    # Tutup koneksi setelah keluar dari loop
    await client.disconnect()

# Jalankan bot dengan asyncio
asyncio.run(main())