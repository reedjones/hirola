from faker import Faker

fake = Faker()


class DummyMessage:
    def __init__(self):
        self.user1 = fake.name()
        self.user2 = fake.name()
        self.current = 0
        self.users = [self.user1, self.user2]

    def get_user(self):
        u = self.users[self.current]
        if self.current == 1:
            self.current = 0
        elif self.current == 0:
            self.current = 1
        return u

    def get_message(self, num_sentences=3):
        data = {
            'user': self.get_user(),
            'message': fake.paragraph(nb_sentences=num_sentences, variable_nb_sentences=True, ext_word_list=None),
            'sent_at': None
        }
