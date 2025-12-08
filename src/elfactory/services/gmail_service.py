"""Gmail API service for email monitoring."""

import os
import pickle
from pathlib import Path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
CREDENTIALS_FILE = PROJECT_ROOT / "credentials.json"
TOKEN_FILE = PROJECT_ROOT / "token.json"


class GmailService:
    """Gmail API service for reading emails."""

    def __init__(self):
        """Initialize Gmail service with OAuth2 authentication."""
        self.service = None
        self.creds = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Gmail API using OAuth2."""
        # Check if token.json exists (previously authenticated)
        if TOKEN_FILE.exists():
            self.creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

        # If no valid credentials, authenticate
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                # Refresh expired token
                print("Refreshing expired token...")
                self.creds.refresh(Request())
            else:
                # First time authentication - opens browser
                if not CREDENTIALS_FILE.exists():
                    raise FileNotFoundError(
                        f"credentials.json not found at {CREDENTIALS_FILE}\n"
                        "Please download it from Google Cloud Console."
                    )

                print("First time authentication - opening browser...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CREDENTIALS_FILE), SCOPES
                )
                self.creds = flow.run_local_server(port=0)

            # Save credentials for next time
            with open(TOKEN_FILE, "w") as token:
                token.write(self.creds.to_json())
            print(f"✓ Authentication successful! Token saved to {TOKEN_FILE}")

        # Build Gmail service
        self.service = build("gmail", "v1", credentials=self.creds)

    def get_unread_messages(self, max_results: int = 10) -> list[dict[str, Any]]:
        """
        Get unread messages from inbox.

        Args:
            max_results: Maximum number of messages to retrieve

        Returns:
            List of message dictionaries with id, subject, from, body
        """
        try:
            # Get list of unread messages
            results = (
                self.service.users()
                .messages()
                .list(userId="me", q="is:unread", maxResults=max_results)
                .execute()
            )

            messages = results.get("messages", [])

            if not messages:
                return []

            # Get full message details
            full_messages = []
            for msg in messages:
                full_msg = (
                    self.service.users()
                    .messages()
                    .get(userId="me", id=msg["id"], format="full")
                    .execute()
                )

                # Parse message
                parsed_msg = self._parse_message(full_msg)
                full_messages.append(parsed_msg)

            return full_messages

        except Exception as e:
            print(f"Error getting unread messages: {e}")
            return []

    def _parse_message(self, message: dict[str, Any]) -> dict[str, Any]:
        """
        Parse Gmail API message into simplified format.

        Args:
            message: Raw Gmail API message

        Returns:
            Simplified message dictionary
        """
        headers = message["payload"]["headers"]

        # Extract headers
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
        from_email = next((h["value"] for h in headers if h["name"] == "From"), "")
        date = next((h["value"] for h in headers if h["name"] == "Date"), "")

        # Extract body
        body = self._get_message_body(message["payload"])

        return {
            "id": message["id"],
            "thread_id": message["threadId"],
            "subject": subject,
            "from": from_email,
            "date": date,
            "body": body,
            "snippet": message.get("snippet", ""),
        }

    def _get_message_body(self, payload: dict[str, Any]) -> str:
        """
        Extract email body from message payload.

        Args:
            payload: Message payload from Gmail API

        Returns:
            Email body text
        """
        import base64

        # Check if payload has body data
        if "body" in payload and "data" in payload["body"]:
            return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")

        # Check parts (multipart messages)
        if "parts" in payload:
            for part in payload["parts"]:
                if part["mimeType"] == "text/plain":
                    if "data" in part["body"]:
                        return base64.urlsafe_b64decode(part["body"]["data"]).decode(
                            "utf-8"
                        )
                # Recursive for nested parts
                if "parts" in part:
                    body = self._get_message_body(part)
                    if body:
                        return body

        return ""

    def mark_as_read(self, message_id: str):
        """
        Mark a message as read.

        Args:
            message_id: Gmail message ID
        """
        try:
            self.service.users().messages().modify(
                userId="me", id=message_id, body={"removeLabelIds": ["UNREAD"]}
            ).execute()
        except Exception as e:
            print(f"Error marking message as read: {e}")

    def watch_mailbox(self) -> dict[str, Any]:
        """
        Set up Gmail push notifications (requires webhook endpoint).

        This is for future enhancement - currently we use polling.

        Returns:
            Watch response from Gmail API
        """

        pass
