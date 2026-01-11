-- This file is loaded after and by 'init.vim', and contains additional configurations
-- that require the use of lua.
----[ nvim-treesitter Configurations ]--------------------------------------------------


require('nvim-treesitter').setup {
  -- Directory to install parsers and queries to (prepended to `runtimepath` to have
  -- priority)
  install_dir = vim.fn.stdpath('data') .. '/site'
}

require('nvim-treesitter').install {
  'awk',
  'bash',
  'comment',
  'diff',
  'lua',
  'regex',
  'python',
  'vim',
  'vimdoc',
  'yaml',
}

vim.api.nvim_create_autocmd('FileType', {
  callback = function(args)
    -- Enable highlighting (Neovim core).
    -- NOTE: pcall will prevent the absence of a parser from throwing an error.
    pcall(vim.treesitter.start, args.buf)
  end,
})


----[ mini.nvim Configurations ]--------------------------------------------------------


-- TODO: Consider adding additional modules.
require('mini.comment').setup()
require('mini.move').setup()
require('mini.pairs').setup()

