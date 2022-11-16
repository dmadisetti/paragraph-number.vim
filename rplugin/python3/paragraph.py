import pynvim

def s(i):
  if i < 100:
    return [min(-1, i), i]
  return [i // 10, i % 10]

def invalid_start(line):
  line = line.strip()
  return not line or line.startswith("#") or line.startswith("-")

@pynvim.plugin
class ParagraphNumbering(object):
    """ Use vim gutter signs to place paragraph and relative paragraph
    linenumbers. Maybe useful for writing?"""

    def update_signs(self):
      for s in range(100):
        self.vim.command(f"sign define l{s} text={s} texthl=LineNum")
        self.vim.command(f"sign define p{s} text={s} texthl=LineNum")
        self.vim.command(f"sign define s{s} text={s} texthl=LineNum")
      self.vim.command(r"sign define empty text=. texthl=Hidden")

    def __init__(self, vim):
        self.previous = []
        self.vim = vim
        self.update_signs()
        self.on = False

    @pynvim.command('ParagraphNumberToggle', range='', nargs='*', sync=True)
    def command_handler(self, args, _range):
        self.on = not self.on
        if self.on:
          self.process()
        else:
          self.vim.command("sign unplace * group=p")
          self.vim.command("sign unplace * group=s")
          self.vim.command("sign unplace * group=l")
          self.vim.command("sign unplace * group=e")

    def process(self):
        empty = True
        current = []
        good = True

        ps = 0
        l = 0
        local = 0

        net = 1
        buffer = self.vim.current.buffer[:]
        for i, line in enumerate(buffer):
          next_is_empty = invalid_start(line)
          p = l = -2
          if empty and not next_is_empty:
            p = ps
            ps += 1
            l = 0
            local = 1
          elif not empty and not next_is_empty:
            l = local
            local += 1
          empty = next_is_empty
          prev = [-10, -10]
          if len(self.previous) > i:
            prev = self.previous[i]
          current.append([p, l])
          for pr, t in zip(prev, [p, l]):
            for n, m in zip(s(t + 1), s(pr + 1)):
              good = good and n == m
          if good or (p == l and p == -2):
              net += 5
              continue

          for t, k in zip([p, l], "ps"):
            for n in s(t + 1):
              self.vim.command(f"sign unplace {net}")
              if n < 0:
                self.vim.command(f"sign place {net} line={i+1} group=e name=empty")
              else:
                self.vim.command(f"sign place {net} line={i+1} group={k} name={k}{n}")
              net += 1
          self.vim.command(f"sign unplace {net}")
          self.vim.command(f"sign place {net} line={i+1} group=e name=empty")
          net += 1
        self.previous = current


    @pynvim.autocmd('CursorMovedI', sync=False)
    def autocmd_handler(self):
      if self.on:
        self.process()
