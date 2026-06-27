import resend
from core.config import setting


async def send_email(email_address: str, reset_token: str, username: str):
    resend.api_key = setting.RESEND_API_KEY

    reset_link = f"https://yourapp.com/reset-password?token={reset_token}"

    html_content = f"""
        <h2>Reset Your Password</h2>

        <p>Hello, {username}</p>

        <p>We received a request to reset your password. Click the link below to set a new password:</p>

        <p><a href="{reset_link}">Reset Password</a></p>

        <p>Or copy and paste this link into your browser:</p>
        <p>{reset_link}</p>

        <p>This link will expire in 1 hour.</p>

        <p>If you didn't request this, please ignore this email.</p>

        <br>
        <p>Thanks</p>
        <p>Blog Post Team</p>
        """

    params: resend.Emails.SendParams = {
        'from': 'onboarding@resend.dev',
        'to': email_address,
        'subject': 'Reset Password',
        'html': html_content
    }

    sent_email = resend.Emails.send(params=params)
    return sent_email
