import argparse
import random
import string

def generate_password(length, use_lowercase, use_uppercase, use_digits, use_special):
    available_chars = ''
    if use_lowercase:
        available_chars += string.ascii_lowercase
    if use_uppercase:
        available_chars += string.ascii_uppercase
    if use_digits:
        available_chars += string.digits
    if use_special:
        available_chars += string.punctuation

    return ''.join(random.choice(available_chars) for _ in range(length))

def save_passwords_to_file(passwords):
    with open("pass.txt", "w") as pass_file:
        for password in passwords:
            pass_file.write(password + "\n")

def main():
    parser = argparse.ArgumentParser(description="Random password generator")
    parser.add_argument("length", type=int, nargs="?", default=0, help="Length of the password")
    parser.add_argument("--lowercase", action="store_true", help="Include lowercase letters")
    parser.add_argument("--uppercase", action="store_true", help="Include uppercase letters")
    parser.add_argument("--digits", action="store_true", help="Include digits")
    parser.add_argument("--special", action="store_true", help="Include special characters")
    args = parser.parse_args()

    if args.length == 0:
        passwords = []

        # 2 паролі довжиною 10 символів
        for _ in range(2):
            passwords.append(generate_password(10, True, True, True, True))

        # 3 цифрові паролі довжиною 8 цифр
        for _ in range(3):
            passwords.append(generate_password(8, False, False, True, False))

        # Пароль з 7 символів нижнього регістру, 3 великих, 5 цифр і 2 спеціальних символів
        passwords.append(generate_password(7, True, False, False, False) +
                        generate_password(3, False, True, False, False) +
                        generate_password(5, False, False, True, False) +
                        generate_password(2, False, False, False, True))

        # Перемішаємо символи у згенерованому паролі
        passwords[-1] = ''.join(random.sample(passwords[-1], len(passwords[-1])))

        # Запишемо згенеровані паролі у файл pass.txt
        save_passwords_to_file(passwords)

        print("Згенеровані паролі збережено у файлі pass.txt.")
    else:
        password = generate_password(args.length, args.lowercase, args.uppercase, args.digits, args.special)
        print(password)

if __name__ == "__main__":
    main()
