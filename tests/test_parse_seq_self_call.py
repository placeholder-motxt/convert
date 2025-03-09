import os
import unittest
from unittest.mock import call, patch

from app.models.diagram import ClassObject
from app.models.methods import (
    AbstractMethodCallObject,
    ClassMethodCallObject,
    ClassMethodObject,
)
from app.parse_json_to_object_seq import ParseJsonToObjectSeq

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DIR = os.path.join(CUR_DIR, "testdata")


class TestParseSeqSelfCall(unittest.TestCase):
    def setUp(self):
        self.parser = ParseJsonToObjectSeq()

        self.add_method_cobj = patch.object(
            ClassObject, "add_method", side_effect=ClassObject.add_method, autospec=True
        )
        self.set_name_cmobj = patch.object(
            ClassMethodObject,
            "set_name",
            side_effect=ClassMethodObject.set_name,
            autospec=True,
        )
        self.add_cls_method_call_cmobj = patch.object(
            ClassMethodObject, "add_class_method_call"
        )
        self.set_caller_cmcobj = patch.object(
            ClassMethodCallObject,
            "set_caller",
            side_effect=ClassMethodCallObject.set_caller,
            autospec=True,
        )
        self.set_method_cmcobj = patch.object(
            ClassMethodCallObject,
            "set_method",
            side_effect=ClassMethodCallObject.set_method,
            autospec=True,
        )

        self.doA = ClassMethodObject()
        self.doA.set_name("doA")

        self.doB = ClassMethodObject()
        self.doB.set_name("doB")
        self.doB_call = ClassMethodCallObject()
        self.doB_call.set_method(self.doB)
        self.doB_call.set_caller(self.doA)

        self.doC = ClassMethodObject()
        self.doC.set_name("doC")
        self.doC_call = ClassMethodCallObject()
        self.doC_call.set_method(self.doC)
        self.doC_call.set_caller(self.doB)

        self.doA.add_class_method_call(self.doB_call)
        self.doB.add_class_method_call(self.doC_call)

    def tearDown(self):
        self.add_method_cobj.stop()
        self.add_cls_method_call_cmobj.stop()
        self.set_caller_cmcobj.stop()
        self.set_method_cmcobj.stop()
        self.set_name_cmobj.stop()

    def test_parse_self_call_valid(self):
        # Valid test when there is a call from one method
        # to another method in the same class (not recursion)
        # there is also no conditions, params, nor return values, just calls
        with open(os.path.join(TEST_DIR, "self_call_valid.json")) as f:
            self.parser.set_json(f.read())

        # start patches before parsing
        add_method_cobj = self.add_method_cobj.start()
        set_name_cmobj = self.set_name_cmobj.start()
        add_cls_method_call_cmobj = self.add_cls_method_call_cmobj.start()
        set_caller_cmcobj = self.set_caller_cmcobj.start()
        set_method_cmcobj = self.set_method_cmcobj.start()

        self.parser.parse()

        self.assertEqual(
            [call_args.args[1] for call_args in add_method_cobj.call_args_list],
            [self.doA, self.doB, self.doC],
        )
        self.assertEqual(
            [call_args.args[1] for call_args in set_name_cmobj.call_args_list],
            ["doA", "doB", "doC"],
        )
        self.assertEqual(
            add_cls_method_call_cmobj.call_args_list,
            [call(self.doB_call), call(self.doC_call)],
        )
        self.assertEqual(
            [call_args.args[1] for call_args in set_caller_cmcobj.call_args_list],
            [self.doA, self.doB],
        )
        self.assertEqual(
            [call_args.args[1] for call_args in set_method_cmcobj.call_args_list],
            [self.doB, self.doC],
        )

    def test_parse_self_call_valid_recursion(self):
        # Valid test when the call made is recursive
        # (caller == method in ClassMethodCallObject)
        with open(os.path.join(TEST_DIR, "self_call_recursion.json")) as f:
            self.parser.set_json(f.read())

        doA_call = ClassMethodCallObject()
        doA_call.set_method(self.doA)
        doA_call.set_caller(self.doA)

        # self.add_method_cobj.side_effect = ClassObject.add_method
        # self.add_method_cobj.autospec = True
        add_method_cobj = self.add_method_cobj.start()
        add_cls_method_call_cmobj = self.add_cls_method_call_cmobj.start()
        set_caller_cmcobj = self.set_caller_cmcobj.start()
        set_method_cmcobj = self.set_method_cmcobj.start()

        self.parser.parse()

        add_method_cobj.assert_called_once()
        add_cls_method_call_cmobj.assert_called_once_with(doA_call)
        set_caller_cmcobj.assert_called_once()
        set_method_cmcobj.assert_called_once()

        last_args = add_method_cobj.call_args.args[1]
        self.assertEqual(last_args, self.doA)

        last_args = set_caller_cmcobj.call_args.args[1]
        self.assertEqual(last_args, self.doA)

        last_args = set_method_cmcobj.call_args.args[1]
        self.assertEqual(last_args, self.doA)

    def test_parse_self_call_too_deep(self):
        # If there is a very deep self call, more than n self call deep,
        # assume that it is invalid as if we try to make it valid,
        # it can lead to DoS. Currently n is 5.
        with open(os.path.join(TEST_DIR, "self_call_recursion_invalid.json")) as f:
            self.parser.set_json(f.read())

        with self.assertRaises(ValueError) as ctx:
            self.parser.parse()

        self.assertEqual(
            str(ctx.exception),
            "Too deep self calls! The maximum allowed "
            f"is {ParseJsonToObjectSeq.ALLOWED_SELF_CALL_DEPTH}",
        )

    def test_parse_self_call_too_deep_edge(self):
        # Edge case when the self call is in between some other non
        # self calls
        with open(os.path.join(TEST_DIR, "self_call_too_many_calls_edge.json")) as f:
            self.parser.set_json(f.read())

        with self.assertRaises(ValueError) as ctx:
            self.parser.parse()

        self.assertEqual(
            str(ctx.exception),
            "Too deep self calls! The maximum allowed "
            f"is {ParseJsonToObjectSeq.ALLOWED_SELF_CALL_DEPTH}",
        )

    def test_parse_self_call_multiple_valid_recursion(self):
        # If on one method there is multiple recursion happening (ignoring arguments
        # for now), it should still be valid
        # class ABC:
        #     def doA(self):
        #         self.doB()
        #         self.doC()
        #
        #     def doB(self):
        #         self.doB()
        #
        #     def doC(self):
        #         self.doC()
        with open(os.path.join(TEST_DIR, "self_call_recursion_multiple.json")) as f:
            self.parser.set_json(f.read())

        self.doC_call.set_caller(self.doA)
        doB_call2 = ClassMethodCallObject()
        doB_call2.set_method(self.doB)
        doB_call2.set_caller(self.doB)
        doC_call2 = ClassMethodCallObject()
        doC_call2.set_method(self.doC)
        doC_call2.set_caller(self.doC)

        add_cls_method_call_cmobj = self.add_cls_method_call_cmobj.start()
        set_caller_cmcobj = self.set_caller_cmcobj.start()
        set_method_cmcobj = self.set_method_cmcobj.start()

        self.parser.parse()

        self.assertEqual(
            add_cls_method_call_cmobj.call_args_list,
            [
                call(self.doB_call),
                call(doB_call2),
                call(self.doC_call),
                call(doC_call2),
            ],
        )
        self.assertEqual(
            [call_args.args[1] for call_args in set_caller_cmcobj.call_args_list],
            [self.doA, self.doB, self.doA, self.doC],
        )
        self.assertEqual(
            [call_args.args[1] for call_args in set_method_cmcobj.call_args_list],
            [self.doB, self.doB, self.doC, self.doC],
        )

    def test_parse_self_call_valid_ret_syntax(self):
        # Case when the return syntax is correct on self calls
        with open(os.path.join(TEST_DIR, "self_call_valid_ret_syntax.json")) as f:
            self.parser.set_json(f.read())

        set_return_var_name = patch.object(
            AbstractMethodCallObject, "set_return_var_name"
        ).start()

        self.parser.parse()

        set_return_var_name.assert_called_once_with("bval")

    def test_parse_self_call_invalid_ret_syntax(self):
        # Case when the return syntax is incorrect
        with open(os.path.join(TEST_DIR, "self_call_invalid_ret_syntax.json")) as f:
            self.parser.set_json(f.read())

        with self.assertRaises(ValueError) as ctx:
            self.parser.parse()

        self.assertEqual(
            str(ctx.exception), "Invalid return variable name: bval -> cval"
        )

    def test_parse_self_call_invalid_ret_val(self):
        # Case when the return value is not a Python identifier
        with open(os.path.join(TEST_DIR, "self_call_invalid_ret_value.json")) as f:
            self.parser.set_json(f.read())

        with self.assertRaises(ValueError) as ctx:
            self.parser.parse()

        self.assertEqual(str(ctx.exception), "Invalid return variable name: $bval")

    def test_parse_self_call_infinite_loop(self):
        # Edge case when a threat actor intentionally modified
        # the JetUML JSON such that it creates an infinite self call
        # loop. Caught thanks to Gemini Reviewer Bot
        with open(os.path.join(TEST_DIR, "self_call_infinite_loop.json")) as f:
            self.parser.set_json(f.read())

        with self.assertRaises(ValueError) as ctx:
            self.parser.parse()

        self.assertEqual(
            str(ctx.exception),
            "Too deep self calls! The maximum allowed "
            f"is {ParseJsonToObjectSeq.ALLOWED_SELF_CALL_DEPTH}",
        )


if __name__ == "__main__":
    unittest.main()
