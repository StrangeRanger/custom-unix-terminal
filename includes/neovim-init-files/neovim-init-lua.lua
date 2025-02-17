-- This file is loaded after and by 'init.vim', and contains additional configurations
-- that require the use of lua.
----[ nvim-treesitter Configurations ]--------------------------------------------------


-- TODO: Determine if I should add more parsers or other configurations.
require('nvim-treesitter.configs').setup {
   -- A list of parser names, or "all" (the listed parsers MUST always be installed).
   ensure_installed = {
      "bash",
      "c",
      "comment",
      "diff",
      -- "disassembly",  -- Good to have on standbye.
      "dockerfile",
      "editorconfig",
      "git_config",
      "git_rebase",
      "gitattributes",
      "gitcommit",
      "gitignore",
      "html",
      "javascript",
      "json",
      -- "kconfig",  -- Good to have on standbye.
      "lua",
      "markdown",
      "markdown_inline",
      "php",
      --"printf",  -- Unsure how it will interact with the C and Bash parsers.
      "python",
      "query",
      "regex",
      "requirements",
      "rust",
      "sql",
      -- "strace",  -- Good to have on standbye.
      -- "tmux",  -- Maybe...
      "typescript",
      "vim",
      "vimdoc",
      "vue",
      "xml",
      "yaml",
   },
   highlight = {
      enable = true,
      -- Setting this to true will run `:h syntax` and tree-sitter at the same time.
      -- Set this to `true` if you depend on 'syntax' being enabled (like for
      -- indentation). Using this option may slow down your editor, and you may see some
      -- duplicate highlights. Instead of true it can also be a list of languages.
      additional_vim_regex_highlighting = false,
   },
}


----[ mini.nvim Configurations ]--------------------------------------------------------


-- TODO: Check other modules to enable.
-- Module: mini.comment
require('mini.comment').setup()
-- Module: mini.move
require('mini.move').setup()
-- Module: mini.pairs
require('mini.pairs').setup()

