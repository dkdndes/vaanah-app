

class TestEmail(TestCustomerConcreteEmailsSending)

    def test_send_password_reset_email_for_user(self):
        extra_context = {
            'user': self.user,
            'reset_url': '/django-oscar/django-oscar',
        }
        self.dispatcher.send_password_reset_email_for_user(self.user, extra_context)

        self._test_common_part()
        expected_subject = 'Resetting your password at  Vaana.com {}.'.format(Site.objects.get_current())
        self.assertEqual(expected_subject, mail.outbox[0].subject)
        self.assertIn('Please go to the following page and choose a new password:', mail.outbox[0].body)
        self.assertIn({{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}, mail.outbox[0].body)