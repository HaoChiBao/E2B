import { expect, test } from 'vitest'

import { Sandbox } from '../src'

class FakeCommands {
  ran: string[] = []
  async run(command: string) {
    this.ran.push(command)
    return {
      stdout: '',
      exitCode: 0,
      disconnect: async () => {},
    }
  }
}

function sandboxWithFakeCommands(): { sandbox: any; ran: string[] } {
  const sandbox = Object.create(Sandbox.prototype) as any
  const commands = new FakeCommands()
  sandbox.commands = commands
  return { sandbox, ran: commands.ran }
}

test('open quotes a URL so & is not treated as a shell metacharacter', async () => {
  const { sandbox, ran } = sandboxWithFakeCommands()
  await sandbox.open('https://example.com/search?q=a&lang=en')
  expect(ran).toEqual(["xdg-open 'https://example.com/search?q=a&lang=en'"])
})

test('open quotes a path that contains spaces', async () => {
  const { sandbox, ran } = sandboxWithFakeCommands()
  await sandbox.open('/home/user/My Report.pdf')
  expect(ran).toEqual(["xdg-open '/home/user/My Report.pdf'"])
})

test('open quotes an argument that contains a single quote', async () => {
  const { sandbox, ran } = sandboxWithFakeCommands()
  await sandbox.open("O'Brien Report.pdf")
  expect(ran).toEqual([`xdg-open 'O'"'"'Brien Report.pdf'`])
})

test('getWindowTitle quotes a window id that contains a single quote', async () => {
  const { sandbox, ran } = sandboxWithFakeCommands()
  await sandbox.getWindowTitle("win'id")
  expect(ran).toEqual([`xdotool getwindowname 'win'"'"'id'`])
})

test('launch with no uri does not append an empty argument', async () => {
  const { sandbox, ran } = sandboxWithFakeCommands()
  await sandbox.launch('firefox')
  expect(ran).toEqual(['gtk-launch firefox'])
})
