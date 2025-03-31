""""[ General Configurations ]""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


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
set colorcolumn=92  " Set a colored line at column 88 in every row.

"" Filetype-specific configurations.
augroup FiletypeConfigs
  autocmd!
  autocmd Filetype markdown,text,csv setlocal colorcolumn=0
  autocmd Filetype java setlocal colorcolumn=100
  autocmd Filetype cs setlocal colorcolumn=120
  " As recommended by the luarocks Style Guide:
  " https://github.com/luarocks/lua-style-guide/blob/master/README.md
  autocmd Filetype lua setlocal tabstop=3 shiftwidth=3 softtabstop=3
  autocmd Filetype html,css,vue,javascript,typescript setlocal colorcolumn=100 tabstop=2 shiftwidth=2 softtabstop=2
  autocmd Filetype vim setlocal tabstop=2 shiftwidth=2 softtabstop=2
augroup END
augroup CsprojSettings
  autocmd!
  autocmd BufRead,BufNewFile *.csproj setlocal tabstop=2 shiftwidth=2 softtabstop=2
augroup END
augroup SlnSettings
  autocmd!
  autocmd BufRead,BufNewFile *.sln setlocal tabstop=4 shiftwidth=4
augroup END



