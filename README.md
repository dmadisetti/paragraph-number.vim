paragraph-number.vim
=============

Paragraph centered line numbering for efficient writing.

![](https://raw.github.com/dmadisetti/paragraph-number.vim/main/doc/money-shot.png)

Best served with [Goyo.vim](https://github.com/junegunn/goyo.vim) and [limelight.vim](https://github.com/junegunn/limelight.vim).
Works on 256-color terminal or on GVim.

Usage
-----

- `:ToggleParagraphNumber`

### Styling

You'll probably want something like:

```vim
    :highlight CursorLineNR ctermbg=236 ctermfg=240
    :highlight Hidden ctermbg=234 ctermfg=234
    :highlight LineNum ctermbg=234 ctermfg=238
    :set signcolumn=yes:5
    :set cursorline
    :set number
```


License
-------

MIT
