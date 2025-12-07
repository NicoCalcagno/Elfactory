"""Email monitoring daemon for Elfactory.

This script continuously monitors Gmail for new gift requests
and triggers the workshop workflow when emails arrive.
"""

import time
from datetime import datetime

from elfactory.services.gmail_service import GmailService
from elfactory.core.orchestrator import process_gift_request


# Configuration
CHECK_INTERVAL = 60  # seconds between checks
VERBOSE = True  # Print detailed logs


def is_gift_request(message: dict) -> bool:
    """
    Determine if an email is a gift request.

    Checks if the subject contains the keyword "letterina".

    Args:
        message: Email message dictionary

    Returns:
        True if this is a gift request, False otherwise
    """
    subject = message.get("subject", "").lower()
    return "letterina" in subject


def process_email(gmail: GmailService, message: dict):
    """
    Process a single gift request email.

    Args:
        gmail: GmailService instance
        message: Email message to process
    """
    print()
    print("=" * 60)
    print(f"📧 New gift request received!")
    print(f"From: {message['from']}")
    print(f"Subject: {message['subject']}")
    print(f"Date: {message['date']}")
    print("=" * 60)
    print()

    # Extract email body
    email_content = message["body"]

    if VERBOSE:
        print("Email content preview:")
        print("-" * 60)
        print(email_content[:500])  # First 500 chars
        if len(email_content) > 500:
            print("...")
        print("-" * 60)
        print()

    try:
        # Process the gift request through the workshop
        print("🎄 Starting workshop workflow...")
        print()

        state = process_gift_request(email_content)

        print()
        print("=" * 60)
        print(f"✓ Gift request processed!")
        print(f"Gift ID: {state.gift_id}")
        print(f"Status: {state.status}")
        print(f"Child: {state.child_info.name if state.child_info else 'Unknown'}")
        print("=" * 60)
        print()

        # Mark email as read
        gmail.mark_as_read(message["id"])
        if VERBOSE:
            print(f"✓ Email marked as read")

    except Exception as e:
        print()
        print(f"✗ Error processing gift request: {e}")
        print()
        # Don't mark as read if processing failed
        # Will retry on next check


def monitor_loop(gmail: GmailService):
    """
    Main monitoring loop.

    Continuously checks for new unread emails and processes them.

    Args:
        gmail: GmailService instance
    """
    print()
    print("🎅 Elfactory Email Monitor Started")
    print("=" * 60)
    print(f"Checking for new emails every {CHECK_INTERVAL} seconds")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()

    processed_ids = set()  # Track processed messages to avoid duplicates

    while True:
        try:
            # Check for unread messages
            messages = gmail.get_unread_messages(max_results=10)

            # Filter for gift requests and unprocessed messages
            for message in messages:
                if message["id"] in processed_ids:
                    continue

                if is_gift_request(message):
                    process_email(gmail, message)
                    processed_ids.add(message["id"])
                else:
                    # Not a gift request, skip it (leave unread)
                    if VERBOSE:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Skipped email without 'letterina' keyword: {message['subject']}")
                    processed_ids.add(message["id"])

            # Clean up old processed IDs (keep last 1000)
            if len(processed_ids) > 1000:
                processed_ids = set(list(processed_ids)[-1000:])

            # Wait before next check
            if VERBOSE:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Waiting {CHECK_INTERVAL}s...")

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print()
            print("=" * 60)
            print("🛑 Monitor stopped by user")
            print("=" * 60)
            break

        except Exception as e:
            print(f"✗ Error in monitor loop: {e}")
            print(f"Retrying in {CHECK_INTERVAL} seconds...")
            time.sleep(CHECK_INTERVAL)


def main():
    """Main entry point."""
    try:
        # Initialize Gmail service
        print("Initializing Gmail service...")
        gmail = GmailService()
        print("✓ Gmail service initialized")

        # Start monitoring
        monitor_loop(gmail)

    except FileNotFoundError as e:
        print()
        print("=" * 60)
        print("✗ Setup Required")
        print("=" * 60)
        print()
        print(f"Error: {e}")
        print()
        print("Please run the setup script first:")
        print("  uv run python scripts/setup_gmail.py")
        print()
        return 1

    except Exception as e:
        print()
        print(f"✗ Error starting monitor: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
