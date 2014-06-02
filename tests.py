import unittest
import vim
import util
import operators
import motions

class BufferTests(unittest.TestCase):
    def setUp(self):
        self.buffer = vim.Buffer(["lorem", "ipsum", "dolor", "sit"])

    def testReplace(self):
        self.buffer.replace_lines(2, 3, ("foo", "bar"))
        self.assertEqual(self.buffer.dump(),
                util.unlines(["lorem", "foo", "bar", "sit"]))

    def testReplaceHead(self):
        self.buffer.replace_lines(1, 1, ("foo", "bar"))
        self.assertEqual(self.buffer.dump(),
                util.unlines(["foo", "bar", "ipsum", "dolor", "sit"]))

    def testReplaceTail(self):
        self.buffer.replace_lines(4, 4, ("foo", "bar"))
        self.assertEqual(self.buffer.dump(),
                util.unlines(["lorem", "ipsum", "dolor", "foo", "bar"]))

    def testReplaceWithNothing(self):
        self.buffer.replace_lines(2, 3, ())
        self.assertEqual(self.buffer.dump(),
                util.unlines(["lorem", "sit"]))

class EditorTests(unittest.TestCase):
    def setUp(self):
        self.editor = vim.Editor()
        self.editor.buffer = vim.Buffer(["foo", " bar", "  dolor", " sit"])

    def testDeleteRight(self):
        self.editor.execute_command(operators.delete, motions.right)
        self.assertEqual(self.editor.buffer.dump(),
                util.unlines(["oo", " bar", "  dolor", " sit"]))

    def testFirstNonblank(self):
        self.assertEqual(motions.first_nonblank.execute(3, 5, self.editor.buffer), (3, 3))

if __name__ == '__main__':
    unittest.main()
