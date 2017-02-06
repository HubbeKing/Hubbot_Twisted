from __future__ import unicode_literals
from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType
from hubbot.Utils.RNN.model import Model
import cPickle
import os
import tensorflow as tf
import unicodedata


class RNNChatter(ModuleInterface):
    help = ""
    save_dir = os.path.join("hubbot", "data", "RNN")

    def __init__(self, bot):
        self.bot = bot
        self.model = None
        self.chars = None
        self.vocab = None
        super(RNNChatter, self).__init__(bot)

    def on_load(self):
        saved_args = cPickle.load(os.path.join(self.save_dir, "config.pkl"))
        self.chars, self.vocab = cPickle.load(os.path.join(self.save_dir, "chars_vocab.pkl"))
        self.model = Model(saved_args, True)

    def should_trigger(self, message):
        if message.type in self.accepted_types:
            return True

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if self.bot.nickname.lower() in message.message_string.lower() and len(message.message_list) > 1:
            reply = ""
            prime_string = message.message_string.replace(self.bot.nickname, "")
            with tf.Session() as sess:
                tf.global_variables_initializer().run()
                saver = tf.train.Saver(tf.global_variables())
                ckpt = tf.train.get_checkpoint_state(self.save_dir)
                if ckpt and ckpt.model_checkpoint_path:
                    saver.restore(sess, ckpt.model_checkpoint_path)
                    reply = self.model.sample(sess, self.chars, self.vocab, 100, prime_string, 1)
            nick_list = [nick.lower() for nick in self.bot.channels[message.reply_to].users.keys()]
            for nick in nick_list:
                if nick in reply.lower():
                    reply_list = reply.lower().split()
                    nick_index = self._index_containing_substring(reply_list, nick)
                    new_list = [item for item in reply_list if nick not in item]
                    new_list.insert(nick_index, message.user.name)
                    reply = " ".join(new_list)
            reply = self._clean_up_string(reply)
            return IRCResponse(ResponseType.SAY, reply.capitalize(), message.reply_to)

    @staticmethod
    def _index_containing_substring(string_list, substring):
        """
        Given a list of strings, returns the index of the first element that contains a given substring
        If none exists, returns -1
        """
        for i, s in enumerate(string_list):
            if substring in s:
                return i
        return -1

    @staticmethod
    def _clean_up_string(string):
        new_string = "".join(c for c in string if ord(c) >= 0x20)
        while unicodedata.category(new_string[0]) not in ["Ll", "Lu"]:
            new_string = new_string[1:]
        return new_string.replace("(.+.+)", "")
