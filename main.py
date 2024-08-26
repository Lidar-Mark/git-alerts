import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
GITHUB_TOKEN = ''
REPO_OWNER = 'Lidar-Mark'
REPO_NAME = 'git-alerts'
BRANCH = 'main'
CHECK_INTERVAL = 5  # seconds

# Email configuration (for notifications)
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
EMAIL_USERNAME = 'your_email@example.com'
EMAIL_PASSWORD = 'your_email_password'
EMAIL_TO = 'recipient@example.com'


def get_latest_commit_sha():
    """
    Get the latest commit SHA for the specified branch.
    """
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/branches/{BRANCH}'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        branch_info = response.json()
        return branch_info['commit']['sha']
    else:
        raise Exception(f'Failed to get branch info: {response.status_code}, {response.text}')


def send_notification():
    """
    Send an email notification.
    """
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USERNAME
    msg['To'] = EMAIL_TO
    msg['Subject'] = 'Repository Update Alert'

    body = 'The main branch of the git-alert repository has been updated.'
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(EMAIL_USERNAME, EMAIL_TO, text)
            print('Notification sent!')
    except Exception as e:
        print(f'Failed to send email: {e}')


def main():
    last_commit_sha = get_latest_commit_sha()
    print(f'Initial commit SHA: {last_commit_sha}')

    try:
        while True:
            time.sleep(CHECK_INTERVAL)
            try:
                current_commit_sha = get_latest_commit_sha()
                if current_commit_sha != last_commit_sha:
                    print('Change detected!')
                    send_notification()
                    last_commit_sha = current_commit_sha
                else:
                    print('No changes.')
            except Exception as e:
                print(f'Error checking for changes: {e}')
    except KeyboardInterrupt:
        print('Monitoring stopped by user.')


if __name__ == '__main__':
    main()
