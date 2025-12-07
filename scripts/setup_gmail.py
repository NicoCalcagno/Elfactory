"""Setup script for Gmail API OAuth2 authentication.

Run this script ONCE to authenticate with Gmail API.
It will open a browser window for you to login and authorize the app.
After successful authentication, a token.json file will be created.
"""

from elfactory.services.gmail_service import GmailService


def main():
    """Setup Gmail API authentication."""
    print("=" * 60)
    print("Gmail API Authentication Setup")
    print("=" * 60)
    print()
    print("This script will:")
    print("1. Open your browser")
    print("2. Ask you to login with your Gmail account")
    print("3. Request permission to read your emails")
    print("4. Save an authentication token for future use")
    print()
    print("=" * 60)
    print()

    try:
        # Initialize GmailService - will trigger OAuth flow
        gmail = GmailService()

        # Test by getting unread count
        print()
        print("Testing connection...")
        messages = gmail.get_unread_messages(max_results=1)

        print(f"✓ Connection successful!")
        print(f"✓ Found {len(messages)} unread message(s) in your inbox")
        print()
        print("=" * 60)
        print("Setup completed successfully!")
        print("You can now run scripts/monitor_emails.py")
        print("=" * 60)

    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        print()
        print("Make sure credentials.json is in the project root directory.")
        return 1

    except Exception as e:
        print(f"✗ Error during setup: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
