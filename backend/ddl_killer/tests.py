from django.test import TestCase
from django.test.client import Client
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import base64
from .models import *
from .views import *
from unittest import mock


class ViewTestCase(TestCase):
    TEST_USER_ID = '10000000'
    TEST_USER_NAME = 'TeSt_userName_123!@#$%^'
    TEST_USER_PWD = 'test_PaSSword123456_'
    TEST_USER_EMAIL = 'test@email.com'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._key_pair = None
        self._user_data = None
        self._user_orm = None

    def setUp(self) -> None:
        class JsonClient(Client):
            def __init__(self, token_hook, **defaults):
                super().__init__(**defaults)
                self.token_hook = token_hook

            def post(self, *args, content_type='application/json', **kwargs):
                token = self.token_hook()
                return super().post(*args, content_type=content_type, HTTP_AUTHORIZATION=token, **kwargs)

            def get(self, *args, content_type='application/json', **kwargs):
                token = self.token_hook()
                return super().get(*args, content_type=content_type, HTTP_AUTHORIZATION=token, **kwargs)

        client = JsonClient(lambda: None if not self._user_data else self._user_data['token'])
        self.client = client

        def mock_mail_send(*args, **kwargs):
            print('sending mock mail.. args:', args, kwargs)

        with mock.patch('ddl_killer.utils.sendmail.YAG.send') as mail_obj:
            mail_obj.side_effect = mock_mail_send
            response = client.post('/api/register',
                                   data={'uid': self.TEST_USER_ID,
                                         'name': self.TEST_USER_NAME,
                                         'password': self.password_encrypt,
                                         'email': self.TEST_USER_EMAIL}).json()
        print('response:', response)
        user = User.objects.get(uid=self.TEST_USER_ID)
        user.is_active = True
        user.save()
        self._user_orm = user

    @property
    def key_pair(self):
        if self._key_pair is None:
            data = self.client.get('/api/security/pub-key').json()
            self._key_pair = SecurityKeyPair.objects.get(id=data['key_id'])
        return self._key_pair

    @property
    def password_encrypt(self):
        key_pair = self.key_pair
        cifer = PKCS1_v1_5.new(RSA.import_key(key_pair.pub_key))
        pwd_encrypt = cifer.encrypt(self.TEST_USER_PWD.encode())
        pwd_encrypt = base64.b64encode(pwd_encrypt).decode()
        pwd_encrypt = 'kid:{}|{}'.format(key_pair.id, pwd_encrypt)
        return pwd_encrypt

    def _login(self):
        if self._user_data is None:
            print('logging...')
            r = self.client.post('/api/login', {'uid': self.TEST_USER_ID,
                                                'password': self.password_encrypt})
            self._user_data = r.json()

    def test_user_login_success(self):
        self._login()
        data = self._user_data
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['name'], self.TEST_USER_NAME)

    def test_user_login_not_found(self):
        r = self.client.post('/api/login', {'uid': 'Not_exists',
                                            'password': self.password_encrypt})
        data = r.json()
        self.assertEqual(data['code'], 404)

    def test_user_login_wrong_password(self):
        r = self.client.post('/api/login', {'uid': self.TEST_USER_ID,
                                            'password': 'wrong password'})
        data = r.json()
        self.assertEqual(data['code'], 401)

    def test_user_login_not_activated(self):
        self._user_orm.is_active = False
        self._user_orm.save()
        r = self.client.post('/api/login', {'uid': self.TEST_USER_ID,
                                            'password': self.password_encrypt})
        data = r.json()
        self.assertEqual(data['code'], 400)
        self._user_orm.is_active = True
        self._user_orm.save()

    def test_edit_user(self):
        self._login()
        data = self.client.post('/api/modify', {
            'uid': self.TEST_USER_ID,
            'name': self.TEST_USER_NAME,
            'password': '',
            'email': 'tmp_email@mail.com'
        }).json()
        self.assertEqual(data['code'], 200)
        self.assertEqual(User.objects.get(uid=self.TEST_USER_ID).email,
                         'tmp_email@mail.com')

        self._user_orm.email = self.TEST_USER_EMAIL
        self._user_orm.save()

    def test_logout(self):
        self._login()
        r = self.client.post('/api/logout')
        data = r.json()
        self.assertEqual(data['code'], 200)

        # token keeps available

    def test_show_user(self):
        self._login()
        r = self.client.post('/api/user/{}/info'.format(self.TEST_USER_ID))
        data = r.json()
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['uid'], self.TEST_USER_ID)
        self.assertEqual(data['name'], self.TEST_USER_NAME)
        self.assertEqual(data['email'], self.TEST_USER_EMAIL)

    def test_show_user_course(self):
        self._login()
        r = self.client.post('/api/user/{}/courses'.format(self.TEST_USER_ID))
        data = r.json()
        self.assertEqual(data['code'], 200)

    def test_show_user_tasks(self):
        self._login()
        r = self.client.post('/api/user/{}/tasks'.format(self.TEST_USER_ID))
        data = r.json()
        self.assertEqual(data['code'], 200)

    def test_show_user_messages(self):
        self._login()
        read_messages = ['read_msg' + str(i) for i in range(10)]
        unread_messages = ['unread_msg' + str(i) for i in range(10)]

        UserMessage.objects.all().delete()
        read_message_orm = []
        unread_message_orm = []
        for i, msg in enumerate(read_messages):
            msg = Message.objects.create(title=msg,
                                         content=msg,
                                         category='test',
                                         publisher=self._user_orm,
                                         publish_time='now')
            orm = UserMessage.objects.create(user=self._user_orm,
                                             is_read=True,
                                             message=msg)
            read_message_orm.append(orm)
        for i, msg in enumerate(unread_messages):
            msg = Message.objects.create(title=msg,
                                         content=msg,
                                         category='test',
                                         publisher=self._user_orm,
                                         publish_time='now')
            orm = UserMessage.objects.create(user=self._user_orm,
                                             is_read=False,
                                             message=msg)
            unread_message_orm.append(orm)

        r = self.client.get('/api/user/{}/message?type=read'.format(self.TEST_USER_ID))
        data = r.json()
        self.assertEqual(data['code'], 200)

        r = self.client.get('/api/user/{}/message?type=unread'.format(self.TEST_USER_ID))
        data = r.json()
        self.assertEqual(data['code'], 200)

        r = self.client.get('/api/user/{}/message'.format(self.TEST_USER_ID))
        data = r.json()
        self.assertEqual(data['code'], 200)

    def test_forget_password(self):
        r = self.client.post('/api/user/forget/email',
                             {'uid': self.TEST_USER_ID})
        data = r.json()
        self.assertEqual(data['code'], 200)

        record = PasswordModificationRecord.objects.get(user=self._user_orm)
        record.key_pair = self.key_pair  # hack for test
        record.save()
        verify_code = record.verify_code
        r = self.client.post('/api/user/forget/verify',
                             {
                                 'uid': self.TEST_USER_ID,
                                 'verify_code': verify_code
                             })
        data = r.json()
        self.assertEqual(data['code'], 200)

        r = self.client.post('/api/user/forget/reset',
                             {
                                 'uid': self.TEST_USER_ID,
                                 'password': self.password_encrypt,
                             })
        data = r.json()
        self.assertEqual(data['code'], 200)

    def test_report_bug(self):
        self._login()
        r = self.client.post('/api/user/{}/report'.format(self.TEST_USER_ID),
                             {'uid': self.TEST_USER_ID,
                              'content': 'a bug'})
        data = r.json()
        self.assertEqual(data['code'], 200)

