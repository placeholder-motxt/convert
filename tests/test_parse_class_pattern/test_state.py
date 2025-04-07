import unittest

from app.parse_class_pattern.parse_relationship_state import (
    DotState,
    MaximumNumberState,
    MinimumNumberState,
    MultiplicityValidator,
    StartState,
)


class TestMultiplicityValidator(unittest.TestCase):
    def setUp(self):
        self.context = MultiplicityValidator("1..2")

    def test_start_state(self):
        state = StartState()
        state.handle(self.context, "1", 0)
        self.assertIsInstance(self.context.state, MinimumNumberState)

        with self.assertRaises(ValueError):
            state.handle(self.context, "a", 0)
        with self.assertRaises(ValueError):
            state.handle(self.context, "-", 0)

    def test_minimum_number_state(self):
        state = MinimumNumberState()
        self.context.state = state
        state.handle(self.context, "2", 1)
        self.assertIsInstance(self.context.state, MinimumNumberState)

        state.handle(self.context, ".", 2)
        self.assertIsInstance(self.context.state, DotState)

        with self.assertRaises(ValueError):
            state.handle(self.context, "*", 1)
        with self.assertRaises(ValueError):
            state.handle(self.context, "-", 1)

    def test_dot_state(self):
        state = DotState()
        self.context.state = state
        state.handle(self.context, ".", 3)
        self.assertEqual(self.context.titik_count, 1)

        state.handle(self.context, "2", 4)
        self.assertIsInstance(self.context.state, MaximumNumberState)

        with self.assertRaises(ValueError):
            state.handle(self.context, "a", 2)
        with self.assertRaises(ValueError):
            state.handle(self.context, "-", 2)

    def test_maximum_number_state(self):
        state = MaximumNumberState()
        self.context.state = state
        state.handle(self.context, "5", 5)
        self.assertIsInstance(self.context.state, MaximumNumberState)

        with self.assertRaises(ValueError):
            state.handle(self.context, "b", 3)
        with self.assertRaises(ValueError):
            state.handle(self.context, "-", 3)


if __name__ == "__main__":
    unittest.main()
