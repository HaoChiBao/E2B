from e2b_desktop import Sandbox


class _FakeCommands:
    def __init__(self):
        self.ran = []

    def run(self, command, **kwargs):
        self.ran.append(command)

        class _Result:
            stdout = ""
            exit_code = 0

            def disconnect(self):
                pass

        return _Result()


def _sandbox_with_fake_commands():
    class _FakeSandbox(Sandbox):
        @property
        def commands(self):
            return self._fake_commands

    sandbox = _FakeSandbox.__new__(_FakeSandbox)
    commands = _FakeCommands()
    sandbox._fake_commands = commands
    return sandbox, commands.ran


def test_open_quotes_a_url_so_ampersand_is_not_a_shell_metacharacter():
    sandbox, ran = _sandbox_with_fake_commands()
    sandbox.open("https://example.com/search?q=a&lang=en")
    assert ran == ["xdg-open 'https://example.com/search?q=a&lang=en'"]


def test_open_quotes_a_path_that_contains_spaces():
    sandbox, ran = _sandbox_with_fake_commands()
    sandbox.open("/home/user/My Report.pdf")
    assert ran == ["xdg-open '/home/user/My Report.pdf'"]


def test_open_quotes_an_argument_that_contains_a_single_quote():
    sandbox, ran = _sandbox_with_fake_commands()
    sandbox.open("O'Brien Report.pdf")
    assert ran == ["xdg-open 'O'\"'\"'Brien Report.pdf'"]


def test_get_window_title_quotes_a_window_id_that_contains_a_single_quote():
    sandbox, ran = _sandbox_with_fake_commands()
    sandbox.get_window_title("win'id")
    assert ran == ["xdotool getwindowname 'win'\"'\"'id'"]


def test_launch_with_no_uri_does_not_append_an_empty_argument():
    sandbox, ran = _sandbox_with_fake_commands()
    sandbox.launch("firefox")
    assert ran == ["gtk-launch firefox"]
