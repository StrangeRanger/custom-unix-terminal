# Custom Unix Terminal

This document serves as an informational guide on how I've customized my terminal in macOS and Linux. It includes a variety of configurations, settings, and programs that enhance my productivity and improve my overall experience within the terminal environment. The document is divided into several sections, each focusing on a different aspect of terminal customization, such as shell frameworks, themes, resource files, plugins, and more.

/// admonition | Disclaimer
    type: warning

This guide assumes you have a basic understanding of the Unix terminal and are comfortable working with configuration files. If you're new to the terminal or need clarification on any of the instructions provided, I recommend proceeding with caution and seeking additional resources or assistance.

///

## Useful Programs

The following table consists of CLI programs that have been useful to me in my day-to-day work. These programs are divided into two categories: Third Party Package Managers (TPPM) and Native Package Managers (NPM).

The TPPM section features programs that can be installed via package managers like Homebrew, Pip, Cargo, Npm, Gem, or Git(1). For each program, I've included a brief description, the operating systems it supports, and the package managers available for installation.
{ .annotate }

1. While all of these programs can be installed manually with `git`, they will only be marked as such if it is recommended by the program's documentation, myself, or it's the only available method.

The NPM section lists programs that can be installed using the system's default package manager. Since I primarily use Debian and Arch-based Linux distributions, all the programs in this section are confirmed to be installable via `apt` or `pacman`. For other Linux distributions, refer to [Repology](https://repology.org/) to see if the program is available via your distribution's package manager. Like the TPPM section, I've included additional information such as a brief description of each program and a link to its Repology page.

/// tab | Third Party Package Manager

--8<-- "includes/tables/useful-packages-tppm.md"

///

/// tab | Native Package Manager

Applicable Operating Systems: Linux

--8<-- "includes/tables/useful-packages-npm.md"

///

## Z Shell (Zsh)

The Z shell, or `zsh`, is a powerful and feature-rich shell that offers many improvements over the default shells provided by most Unix-based operating systems. It includes advanced features such as improved tab completion, spelling correction, and shared command history, making it a popular choice among developers and power users. This section covers the shell framework, theme, resource file, plugins, and aliases that I use to customize my `zsh` environment.

### Shell Framework

A framework makes customizing the shell much more manageable, whether it be through plugins or themes. I often prefer complete control over my configurations, but the convenience provided by a framework has dramatically improved my workflow and ease of management.

Due to its popularity, reliability, and consistent updates, my framework of choice has become [oh-my-zsh](https://github.com/ohmyzsh/ohmyzsh). As one of the leading `zsh` frameworks, it made its initial commit on August 23, 2009, allowing it enough time to improve and refine its features.

<!-- In a [later section](#oh-my-zsh-plugins), I've included a list of built-in plugins that I use. -->

### Shell Theme

Similar to how a shell framework enhances the shell's functionality, a shell theme improves its appearance and user experience. A well-designed theme can provide valuable information at a glance, such as the current directory, git branch, and other relevant details.

My preferred shell theme is [Starship](https://github.com/starship/starship), which draws inspiration from several well-known and popular [shell themes](https://github.com/starship/starship#-inspired-by). It is written in Rust, making it fast, lightweight, and highly customizable. Starship is designed to support a wide range of shells and external tools, making it a versatile choice for users across different platforms.

Before Starship, I used [Powerlevel10k](https://github.com/romkatv/powerlevel10k), which is another **excellent** shell theme. However, as of May 21, 2024, Powerlevel10k has entered a ["life support" mode](https://github.com/romkatv/powerlevel10k/issues/2690). In the [maintainer's words](https://github.com/romkatv/powerlevel10k#powerlevel10k), "The project has very limited support", with "no new features [in the works]", "most bugs will go unfixed", and "help requests will be ignored". As a result, I searched for an alternative and found Starship to be a suitable replacement.

### Zsh Resource File

The `.zshrc` file is where all the configurations for `zsh` are stored. It's the primary resource file for customizing the shell, containing settings, aliases, and other configurations that define its behavior and appearance.

Below is the content of my `.zshrc` file, divided into two sections: one for macOS and one for Linux. Each section is tailored to its respective operating system. You're welcome to use this resource however you like. I offer it as a guide for structuring your own `.zshrc` file and to present additional configurations not detailed elsewhere in this document.

/// details | My Zsh Resource File
//// tab | macOS

```bash title=".zshrc"
--8<-- "includes/zshrc-files/zshrc-macos.zsh"
```

////

//// tab | Linux

```bash title=".zshrc"
--8<-- "includes/zshrc-files/zshrc-linux.zsh"
```

////
///

#### Oh-my-zsh Plugins

`oh-my-zsh` provides more than 325 [built-in plugins](https://github.com/ohmyzsh/ohmyzsh#plugins) that are regularly updated and maintained by the community. These plugins offer a wide range of features, from syntax highlighting and auto-completion to git integration and directory navigation.

Below are all the plugins that I use, along with a brief description of their functionality:

--8<-- "includes/tables/oh-my-zsh-plugins.md"

#### Aliases

Many frameworks, such as `oh-my-zsh`, provide their own set of aliases to simplify and improve common commands. Any CLI user will tell you that aliases are a powerful tool for increasing productivity and efficiency. They allow you to create shortcuts for frequently used commands, reducing the time and effort required to type them out.

Below are aliases I've create, organized into two groups: Group 1 and Group 2. Group 1 contains general aliases, while Group 2 includes aliases for displaying useful programs I don't frequently use and often forget about.

/// tab | macOS

```zsh title=".zshrc"
--8<-- "includes/zshrc-files/zshrc-macos-snippet.zsh:user_config"
```

///

/// tab | Linux

```zsh title=".zshrc"
--8<-- "includes/zshrc-files/zshrc-linux-snippet.zsh:user_config"
```

///

### Modifying CLI Colors

You can customize the colors of folders, files, and other items in the terminal by setting the `LS_COLORS` or `LSCOLORS` environment variables.(1) Each variable uses a unique format to specify the colors and styles of different file types and directories. For more information regarding these variables, refer to the "CLI Colors Explained" drop-down.
{ .annotate }

1. Linux only requires `LS_COLORS`, while macOS needs both `LS_COLORS` and `LSCOLORS` to be set.

/// details | CLI Colors Explained

Between macOS and Linux, there is a slight difference in how CLI colors are configured. macOS requires both `LSCOLORS` and `LS_COLORS` to fully enable and set CLI colors within the terminal. Conversely, Linux only needs `LS_COLORS` to achieve the same.

This difference arises from the distinct version of the `ls` command on macOS and Linux. macOS employs the FreeBSD version of `ls`, which relies on `LSCOLORS` to define the color scheme for file and directory listings. In contrast, Linux uses the GNU version, which depends on `LS_COLORS` for the same purpose. On both systems, `LS_COLORS` is also used by shells like `zsh` to colorize other tools and utilities.

Included below is a key that explains the values of `LSCOLORS` and `LS_COLORS` in my configurations:

--8<-- "includes/tables/cli-colors-explained.md"

I recommend visiting this [gist](https://gist.github.com/thomd/7667642) for an in-depth understanding of the `LS_COLORS` and `LSCOLORS` values.

///

The below configurations are my `LS_COLORS` and `LSCOLORS` settings for macOS and Linux. To use them, add the code to your `.zshrc` file:

/// tab | macOS

```bash title="CLI Color Configuration"
--8<-- "includes/zshrc-files/zshrc-macos-snippet.zsh:ls_colors"
```

///

/// tab | Linux

```bash title="CLI Color Configuration"
--8<-- "includes/zshrc-files/zshrc-linux-snippet.zsh:ls_colors"
```

///

You can further modify the shading and appearance of CLI colors by adjusting the ANSI color scheme in your terminal profile. This can be done manually, with guides available for [macOS](https://support.apple.com/guide/terminal/change-profiles-text-preferences-trmltxt/mac) and [Linux](https://help.gnome.org/users/gnome-terminal/stable/app-colors.html.en) (specific to GNOME). Alternatively, you can use my custom profile schemes, with instructions detailed in the [Terminal Profile](#terminal-profile) section.

## Text Editor

There are many terminal-based text editors to choose from, each with unique features and capabilities. I've found that [Neovim](https://github.com/neovim/neovim) is the most powerful and versatile option for my needs.

<!-- Neovim a fork of [Vim](https://github.com/vim/vim) that aims to improve upon Vim's features and performance, with a focus on extensibility and usability. It is designed to be more user-friendly and accessible to new users while still providing the power and flexibility that experienced users expect. -->

### Neovim Resource File

Like the `.zshrc` file for `zsh`, Neovim has its own resource file, located at `~/.config/nvim/init.vim`, where all the configurations for the editor are stored. This file contains settings, key mappings, syntax highlighting, and other configurations that define Neovim's behavior and appearance.

Below is the content of my `init.vim` file, divided into two sections: with plugins and without plugins. The former includes configurations for various plugins I use, while the latter is a more streamlined setup without any plugins. You can choose the configuration that best suits your needs and add it to your `~/.config/nvim/init.vim` file.

/// tab | With Plugins

I manage all of my Neovim plugins using [vim-plug](https://github.com/junegunn/vim-plug#installation), a self-described minimalist Vim plugin manager. It simplifies the process of installing, updating, and removing plugins, making it easier to manage and maintain a large number of plugins. While other Vim package managers are available, my configurations are specifically tailored to `vim-plug`.

To use these configurations, you'll first need to [install vim-plug](https://github.com/junegunn/vim-plug?tab=readme-ov-file#installation). Once installed, you can add the following code to your `init.vim` file. With `init.vim` open in Neovim, initiate the plugin installation by entering `:source %` (1) followed by `:PlugInstall`.
{ .annotate }

1. When using `:source %`, you can safely ignore any errors that may appear, as they are most likely caused by Neovim searching for plugins that have yet to be installed.

```vim title="init.vim"
--8<-- "includes/neovim-init-files/neovim-init-vim-plug.vim"
```

///

/// tab | Without Plugins

These configurations are designed for users who prefer a more straightforward setup without the features provided by plugins. They tweak Neovim's default settings without changing its core functionality, offering a more streamlined experience while preserving Vim's essential behavior.

```vim title="init.vim"
--8<-- "includes/neovim-init-files/neovim-init-non-vim-plug.vim"
```

///

## Terminal Profile

A terminal profile is a set of configurations that define the visual appearance and behavior of the terminal window, including the color scheme, font style, and other visual elements. Customizing the terminal profile can improve the user experience, making the terminal more visually appealing and easier to work with.

/// tab | macOS

My custom profile is a modified version of the "Basic" profile that comes pre-installed on macOS. To add it to your list of profiles, follow the instructions below:

1. Download the terminal profile: [Basic (Modified).terminal](terminal-profiles/Basic%20(Modified).terminal)
2. Open a new terminal window.
3. Import the profile:
      1. Go to **Preferences**.
      2. Navigate to the **Profiles** tab.
      3. Click on the gear icon at the bottom left of the window.
      4. Select **Import...**.
      5. Locate and select the downloaded **Basic (Modified).terminal** file.
4. Set as default profile:
      1. Select the newly imported profile from the list.
      2. Click the **Default** button at the bottom of the window.

///

/// tab | Linux

My custom profile is based on the one I use for macOS. To add it to your list of profiles, follow the instructions below:

1. Download the terminal profile: [Gnome Basic (Modified).dconf](terminal-profiles/gnome-terminal-profile.dconf)
2. Download the profile setup script: [terminal-profile-setup.bash](terminal-profiles/terminal-profile-setup.bash)
3. Open a new terminal window.
4. Navigate to the directory where both files were downloaded to (e.g., `~/Downloads`).
5. Execute the setup script:
```bash
chmod +x terminal-profile-setup.bash
./terminal-profile-setup.bash
```

///
