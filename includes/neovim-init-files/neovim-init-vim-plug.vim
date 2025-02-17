""""[ vim-plug Configurations ]"""""""""""""""""""""""""""""""""""""""""""""""""""""""""


call plug#begin(stdpath('data') . '/plugged')
" Make sure you use single quotes

" Vim help for vim-plug itself
Plug 'junegunn/vim-plug'

" Rainbow delimiters for Neovim with Tree-sitter.
Plug 'HiPhish/rainbow-delimiters.nvim'
" Lean & mean status/tabline for vim that's light as air.
Plug 'vim-airline/vim-airline'
" A collection of themes for vim-airline.
Plug 'vim-airline/vim-airline-themes'
" Retro groove color scheme for Vim.
Plug 'sainnhe/gruvbox-material'
" Check syntax in Vim asynchronously and fix files, with Language Server Protocol (LSP)
" support.
Plug 'dense-analysis/ale'
" Better whitespace highlighting for Vim.
Plug 'ntpeters/vim-better-whitespace'
" An incremental parsing system for programming tools.
Plug 'nvim-treesitter/nvim-treesitter', {'do': ':TSUpdate'}
" Highlight columns in CSV and TSV files and run queries in SQL-like language.
Plug 'mechatroner/rainbow_csv'
" A simple and lightweight Neovim plugin that brings syntax highlighting to generic log
" patterns and provides straight-forward configuration to manage the filetype detection
" rules over your preferred log files.
Plug 'fei6409/log-highlight.nvim'
" Library of 40+ independent Lua modules improving overall Neovim (version 0.8 and
" higher) experience with minimal effort.
Plug 'echasnovski/mini.nvim'

" Initialize plugin system
call plug#end()
"
" Brief help:
"   PlugInstall  - Install plugins
"   PlugUpdate   - Install or update plugins
"   PlugClean    - Remove unlisted plugins (bang version will clean without prompt)
"   PlugUpgrade  - Upgrade vim-plug itself
"   PlugStatus   - Check the status of plugins
"   PlugDiff     - Examine changes from the previous update and the pending changes
"   PlugSnapshot - Generate script for restoring the current snapshot of the plugins


""""[ General Configurations ]"""""""""""""""""""""""""""""""""""""""""""""


"""
""" Overwrites specified default setting.
"""

"" Overwrite for all file types.
set expandtab       " Use spaces instead of tabs.
set tabstop=4       " Number of spaces that a <Tab> in the file counts for.
set shiftwidth=4    " Number of spaces to use for each step of (auto)indent.
set softtabstop=4   " Number of spaces that a <Tab> in the file counts for.
set endofline       " Keep the last line of a file if it has no newline.
set fixendofline    " Ensures a newline at the end of the file, if endofline is enabled.
set colorcolumn=88  " Set a colored line at column 88 in every row.

"" Filetype-specific configurations.
autocmd Filetype markdown,text,csv setlocal colorcolumn=0
autocmd Filetype java setlocal colorcolumn=100
autocmd Filetype cs setlocal colorcolumn=120
" As recommended by the luarocks Style Guide:
" https://github.com/luarocks/lua-style-guide/blob/master/README.md
autocmd Filetype lua setlocal tabstop=3 shiftwidth=3 softtabstop=3
autocmd Filetype html,css,vue,javascript,typescript setlocal colorcolumn=100 tabstop=2 shiftwidth=2 softtabstop=2


""""[ vim-plug Plugin Configurations ]""""""""""""""""""""""""""""""""""""""""""""""""""


" Font: Power Line Font
set guifont=MesloLGS_NF:h12

"" Plugin: gruvbox-material
colorscheme gruvbox-material
set background=dark
let g:gruvbox_material_foreground = 'original'
let g:gruvbox_material_enable_bold = 1
let g:gruvbox_material_enable_italic = 1

"" Plugin: vim-airline
let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#tabline#left_sep = ' '
let g:airline#extensions#tabline#left_alt_sep = '|'
let g:airline#extensions#tabline#formatter = 'default'
let g:airline#extensions#ale#enabled = 1
let g:airline_powerline_fonts = 1

"" Plugin: better-whitespace
let g:better_whitespace_enabled = 1
let g:strip_whitespace_on_save = 1

"" Plugin: ale
"let g:ale_use_neovim_diagnostics_api = 0


""""[ Lua Configurations ]""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


" Load 'nvim-treesitter' configurations.
lua dofile(vim.fn.stdpath('config') .. '/second_init.lua')


""""[ Useful Commands ]"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


" :NERDTree        - Opens NERDTree file system explorer.
" :StripWhitespace - Clean extra whitespace.
" :ALEInfo         - Show ALE information.
" :ALEToggle       - Toggle ALE on/off.
" :TSInstall       - Install treesitter parsers.
" :TSUpdate        - Update treesitter parsers.
" :TSInstallInfo   - Show treesitter information.

