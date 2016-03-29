import os

import mock

from test_utils import CharmTestCase

os.environ['JUJU_UNIT_NAME'] = 'glance'
with mock.patch('actions.hooks.glance_utils.register_configs') as configs:
    configs.return_value = 'test-config'
    import actions.actions


class PauseTestCase(CharmTestCase):

    def setUp(self):
        super(PauseTestCase, self).setUp(
            actions.actions, ["pause_unit_helper"])

    def test_pauses_services(self):
        actions.actions.pause([])
        self.pause_unit_helper.assert_called_once_with('test-config')


class ResumeTestCase(CharmTestCase):

    def setUp(self):
        super(ResumeTestCase, self).setUp(
            actions.actions, ["resume_unit_helper"])

    def test_pauses_services(self):
        actions.actions.resume([])
        self.resume_unit_helper.assert_called_once_with('test-config')


class MainTestCase(CharmTestCase):

    def setUp(self):
        super(MainTestCase, self).setUp(actions.actions, ["action_fail"])

    def test_invokes_action(self):
        dummy_calls = []

        def dummy_action(args):
            dummy_calls.append(True)

        with mock.patch.dict(actions.actions.ACTIONS, {"foo": dummy_action}):
            actions.actions.main(["foo"])
        self.assertEqual(dummy_calls, [True])

    def test_unknown_action(self):
        """Unknown actions aren't a traceback."""
        exit_string = actions.actions.main(["foo"])
        self.assertEqual("Action foo undefined", exit_string)

    def test_failing_action(self):
        """Actions which traceback trigger action_fail() calls."""
        dummy_calls = []

        self.action_fail.side_effect = dummy_calls.append

        def dummy_action(args):
            raise ValueError("uh oh")

        with mock.patch.dict(actions.actions.ACTIONS, {"foo": dummy_action}):
            actions.actions.main(["foo"])
        self.assertEqual(dummy_calls, ["uh oh"])
