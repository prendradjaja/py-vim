import unittest
import vim

class BufferTests(unittest.TestCase):
    def setUp(self):
        self.buffer = vim.Buffer(["lorem", "ipsum", "dolor", "sit"])

    def testReplace(self):
        self.buffer.replace_lines(2, 3, ("foo", "bar"))
        self.assertEqual(self.buffer.dump(),
                "lorem\nfoo\nbar\nsit\n")

    def testReplaceHead(self):
        self.buffer.replace_lines(1, 1, ("foo", "bar"))
        self.assertEqual(self.buffer.dump(),
                "foo\nbar\nipsum\ndolor\nsit\n")

    def testReplaceTail(self):
        self.buffer.replace_lines(4, 4, ("foo", "bar"))
        self.assertEqual(self.buffer.dump(),
                "lorem\nipsum\ndolor\nfoo\nbar\n")

    def testReplaceWithNothing(self):
        self.buffer.replace_lines(2, 3, ())
        self.assertEqual(self.buffer.dump(),
                "lorem\nsit\n")

if __name__ == '__main__':
    unittest.main()
