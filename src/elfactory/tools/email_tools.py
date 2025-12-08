"""Email sending tools for final gift responses."""

import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from pathlib import Path
from datapizza.tools import tool
from elfactory.services.gmail_service import GmailService
from elfactory.tools.state_tools import active_gifts, current_gift_id


@tool
def send_gift_email(
    recipient_email: str,
    subject: str,
    html_body: str,
    image_path: str = None
) -> str:
    """
    Send the final gift response email to the child.

    Args:
        recipient_email: Email address of the recipient
        subject: Email subject line
        html_body: HTML formatted email body
        image_path: Optional path to gift image to attach

    Returns:
        Confirmation message
    """
    gift_id = current_gift_id.get()

    try:
        gmail = GmailService()

        message = MIMEMultipart('related')
        message['To'] = recipient_email
        message['Subject'] = subject

        # Replace image placeholder if image exists
        if image_path and Path(image_path).exists():
            html_body = html_body.replace('[IMAGE_PLACEHOLDER]', '<img src="cid:gift_image" style="max-width: 600px; height: auto;" />')

            with open(image_path, 'rb') as f:
                img_data = f.read()
            image = MIMEImage(img_data)
            image.add_header('Content-ID', '<gift_image>')
            image.add_header('Content-Disposition', 'inline', filename='gift.png')
            message.attach(image)

        html_part = MIMEText(html_body, 'html')
        message.attach(html_part)

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

        gmail.service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()

        state = active_gifts.get(gift_id)
        if state:
            state.log_action(
                agent="email_sender",
                action="send_email",
                details=f"Email sent to {recipient_email} with subject: {subject}"
            )
            # Store the final response email content
            state.final_response = f"Subject: {subject}\n\n{html_body}"
            state.update_status("email_sent")

        return f"✓ Email sent successfully to {recipient_email}"

    except Exception as e:
        return f"✗ Error sending email: {str(e)}"
