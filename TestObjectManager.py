import unittest
from objectManager import ObjectManager

class ObjectManagerTests(unittest.TestCase):
    def setUp(self):
        self.o1 = object()
        self.o2 = object()
        self.o3 = object()

        ObjectManager().clearObjects()

    def testSingletonDesign(self):
         self.assertEqual(ObjectManager(), ObjectManager())

    def testAddObj(self):
        self.addThreeObjects()

        self.assertIn(self.o1, ObjectManager())
        self.assertIn(self.o2, ObjectManager())
        self.assertIn(self.o3, ObjectManager())
        self.assertEqual(3, ObjectManager().getNumObjects())

    def testRemoveObj(self):
        self.addThreeObjects()
        ObjectManager().removeObj(self.o2)

        self.assertIn(self.o1, ObjectManager())
        self.assertNotIn(self.o2, ObjectManager())
        self.assertIn(self.o3, ObjectManager())
        self.assertEqual(2, ObjectManager().getNumObjects())

    def testGetObjects(self):
        self.addThreeObjects()
        todos = ObjectManager().getObjects()

        self.assertIn(self.o1, todos)
        self.assertIn(self.o2, todos)
        self.assertIn(self.o3, todos)
        self.assertEqual(3, len(todos))

    def testClearObjects(self):
        self.addThreeObjects()
        self.assertEqual(3, ObjectManager().getNumObjects())

        ObjectManager().clearObjects()
        self.assertEqual(0, ObjectManager().getNumObjects())

    def addThreeObjects(self):
        ObjectManager().addObj(self.o1)
        ObjectManager().addObj(self.o2)
        ObjectManager().addObj(self.o3)


if __name__ == '__main__':
    unittest.main()
