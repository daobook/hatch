# 构建配置

-----

所有构建配置都在 `tool.hatch.build` 表中定义。

[Build targets](#build-targets) 被定义为 `tool.hatch.build.targets` 内的部分：

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build.targets.<TARGET_NAME>]
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build.targets.<TARGET_NAME>]
    ```

对于每个构建目标，您可以覆盖顶层 `tool.hatch.build` 表中设置的任何默认值。

## 构建系统

要与更广泛的 [Python 打包生态系统](../build.md#packaging-ecosystem) 兼容，必须如下定义[构建系统](https://peps.python.org/pep-0517/#source-trees)：

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [build-system]
    requires = ["hatchling"]
    build-backend = "hatchling.build"
    ```

这里定义的 `hatchling` 版本将用于构建所有目标。

Hatchling 是  [PEP 517][]/[PEP 660][] 兼容的构建后端，是 Hatch 本身的一个依赖项。

## 文件选择

### VCS

默认情况下，Hatch 会尊重项目根目录或父目录中的第一个 `.gitignore` 或 `.hgignore` 文件。设置 `ignore-vcs` 为 `true` 来禁用此行为：

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build]
    ignore-vcs = true
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build]
    ignore-vcs = true
    ```

!!! note
    `.hgignore` 文件只支持 glob 语法。

### 模式

您可以设置 `include` 和 `exclude` 选项，以准确地选择在每次构建中使用哪些文件，其中 `exclude` 优先。每个条目都代表 [git 风格的 glob 模式](https://git-scm.com/docs/gitignore#_pattern_format)。

例如，配置如下：

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build]
    include = [
      "pkg/*.py",
      "/tests",
    ]
    exclude = [
      "*.json",
      "pkg/_compat.py",
    ]
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build]
    include = [
      "pkg/*.py",
      "/tests",
    ]
    exclude = [
      "*.json",
      "pkg/_compat.py",
    ]
    ```

将排除所有扩展名为 `.json` 的文件，并包括位于根目录下的 `tests/` 目录下的所有文件，以及位于根目录下的 `pkg` 目录下的所有扩展名为 `.py` 的文件(`_compat.py` 除外)。

### Artifacts

如果你想包含 [被VCS忽略](#vcs) 的文件，比如那些可能由 [build hooks](#build-hooks) 创建的文件，你可以使用 `artifacts` 选项。该选项在语义上等价于 `include`。

注意，`artifacts` 不受 `exclude` 选项的影响。可以使用更显式的路径或使用 `!` 否定算子。当使用 `!` 算子，否定模式必须在更通用的模式之后。

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build]
    artifacts = [
      "*.so",
      "*.dll",
      "!/foo/*.so",
    ]
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build]
    artifacts = [
      "*.so",
      "*.dll",
      "!/foo/*.so",
    ]
    ```

### 显式选择

#### 通用

您可以使用 `only-include` 选项来防止从项目根开始的目录遍历，并且只选择目录或文件的特定相对路径。使用此选项会忽略任何已定义的 [`include` 模式](#patterns)。

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build.targets.wheel]
    only-include = ["pkg", "tests/unit"]
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build.targets.wheel]
    only-include = ["pkg", "tests/unit"]
    ```

#### Packages

`packages` 选项在语义上等价于 `only-include` (优先级)，只是附带的路径将被折叠为只包含最终组件。

例如，如果你想要发送存储在 `src` 目录下的包 `foo`，你可以这样做：

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build.targets.wheel]
    packages = ["src/foo"]
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build.targets.wheel]
    packages = ["src/foo"]
    ```

### Forced inclusion

`force-include` 选项允许您从文件系统上任何位置选择应该包含的特定文件或目录，并将它们映射到所需的相对发布路径。

例如，如果在项目根目录中有名为 `artifacts` 的目录，其中包含名为 `lib.so` 的文件。并且，在你的主目录下有名为 `lib.h` 的文件，你可以使用以下配置将这两个文件放在 `pkg` 目录中：

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build.force-include]
    "../artifacts" = "pkg"
    "~/lib.h" = "pkg/lib.h"
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build.force-include]
    "../artifacts" = "pkg"
    "~/lib.h" = "pkg/lib.h"
    ```

!!! note
    - 文件必须精确地映射到它们所需的路径，而不是目录。
    - 递归地包含目录源的内容。
    - 要将目录内容直接映射到根目录，请使用 `/` (一个正斜杠)。
    - 不存在的源将被静默地忽略。

!!! warning
    使用此选项包含的文件将覆盖其他文件选择选项已经包含的任何文件路径。

### 默认文件选择

如果没有提供文件选择选项，则包含的内容由每个 [build target](#build-targets) 决定。

### 排除包之外的文件

如果你想排除不存在于 Python 包中的非 [artifact](#artifacts) 文件，将 `only-packages` 设置为 `true`：

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build]
    only-packages = true
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build]
    only-packages = true
    ```

### 重写路径

你可以用 `sources` 选项重写目录的相对路径。例如，配置如下：

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build.sources]
    "src/foo" = "bar"
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build.sources]
    "src/foo" = "bar"
    ```

将分发文件 `src/foo/file.ext` 作为 `bar/file.ext`。

如果你想完全删除路径前缀，而不是将每个前缀都设置为空字符串，你可以将 `sources` 定义为数组：

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build]
    sources = ["src"]
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build]
    sources = ["src"]
    ```

[packages](#packages) 选项本身依赖于 sources。为 `wheel` 目标定义 `#!toml packages = ["src/foo"]` 等价如下：

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build.targets.wheel]
    only-include = ["src/foo"]
    sources = ["src"]
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build.targets.wheel]
    only-include = ["src/foo"]
    sources = ["src"]
    ```

### Performance

All encountered directories are traversed by default. To skip non-[artifact](#artifacts) directories that are excluded, set `skip-excluded-dirs` to `true`:

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build]
    skip-excluded-dirs = true
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build]
    skip-excluded-dirs = true
    ```

!!! warning
    This may result in not shipping desired files. For example, if you want to include the file `a/b/c.txt` but your [VCS ignores](#vcs) `a/b`, the file `c.txt` will not be seen because its parent directory will not be entered. In such cases you can use the [`force-include`](#forced-inclusion) option.

## Reproducible builds

By default, [build targets](#build-targets) will build in a reproducible manner provided that they support that behavior. To disable this, set `reproducible` to `false`:

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build]
    reproducible = false
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build]
    reproducible = false
    ```

When enabled, the [SOURCE_DATE_EPOCH](https://reproducible-builds.org/specs/source-date-epoch/) environment variable will be used for all build timestamps. If not set, then Hatch will use an [unchanging default value](../plugins/utilities.md#hatchling.builders.utils.get_reproducible_timestamp).

## Output directory

When the output directory is not provided to the [`build`](../cli/reference.md#hatch-build) command, the `dist` directory will be used by default. You can change the default to a different directory using a relative or absolute path like so:

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build]
    directory = "<PATH>"
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build]
    directory = "<PATH>"
    ```

## Dev mode

By default for [dev mode](environment/overview.md#dev-mode) environment installations or [editable installs](https://pip.pypa.io/en/stable/cli/pip_install/#editable-installs), the `wheel` target will determine which directories should be added to Python's search path based on the [selected files](#file-selection).

If you want to override this detection or perhaps instruct other build targets as well, you can use the `dev-mode-dirs` option:

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build]
    dev-mode-dirs = ["."]
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build]
    dev-mode-dirs = ["."]
    ```

If you don't want to add entire directories to Python's search path, you can enable a more targeted mechanism with the mutually exclusive `dev-mode-exact` option:

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build]
    dev-mode-exact = true
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build]
    dev-mode-exact = true
    ```

!!! warning
    The `dev-mode-exact` mechanism is [not supported](https://github.com/microsoft/pylance-release/issues/2114) by static analysis tools & IDEs, therefore functionality such as autocompletion is unlikely to work.

## Build targets

A build target can be provided by any [builder plugin](../plugins/builder/reference.md). There are three built-in build targets: [wheel](../plugins/builder/wheel.md), [sdist](../plugins/builder/sdist.md), and [custom](../plugins/builder/custom.md).

### Dependencies

You can specify additional dependencies that will be installed in each build environment, such as for third party builders:

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build.targets.your-target-name]
    dependencies = [
      "your-builder-plugin"
    ]
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build.targets.your-target-name]
    dependencies = [
      "your-builder-plugin"
    ]
    ```

You can also declare dependence on the project's [runtime dependencies](metadata.md#required) with the `require-runtime-dependencies` option:

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build.targets.your-target-name]
    require-runtime-dependencies = true
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build.targets.your-target-name]
    require-runtime-dependencies = true
    ```

Additionally, you may declare dependence on specific [runtime features](metadata.md#optional) of the project with the `require-runtime-features` option:

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build.targets.your-target-name]
    require-runtime-features = [
      "feature1",
      "feature2",
    ]
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build.targets.your-target-name]
    require-runtime-features = [
      "feature1",
      "feature2",
    ]
    ```

### Versions

If a build target supports multiple build strategies or if there are major changes over time, you can specify exactly which versions you want to build using the `versions` option, which may be defined as either an array of strings or a comma-separated string:

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build.targets.<TARGET_NAME>]
    versions = [
      "v1",
      "beta-feature",
    ]
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build.targets.<TARGET_NAME>]
    versions = [
      "v1",
      "beta-feature",
    ]
    ```

See the [wheel](../plugins/builder/wheel.md#versions) target for a real world example.

## Build hooks

A build hook defines code that will be executed at various stages of the build process and can be provided by any [build hook plugin](../plugins/build-hook/reference.md). There is one built-in build hook: [custom](../plugins/build-hook/custom.md).

Build hooks can be applied either globally:

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build.hooks.<HOOK_NAME>]
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build.hooks.<HOOK_NAME>]
    ```

or to specific build targets:

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build.targets.<TARGET_NAME>.hooks.<HOOK_NAME>]
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build.targets.<TARGET_NAME>.hooks.<HOOK_NAME>]
    ```

### Dependencies

You can specify additional dependencies that will be installed in each build environment, such as for third party build hooks:

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build.hooks.your-hook-name]
    dependencies = [
      "your-build-hook-plugin"
    ]
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build.hooks.your-hook-name]
    dependencies = [
      "your-build-hook-plugin"
    ]
    ```

You can also declare dependence on the project's [runtime dependencies](metadata.md#required) with the `require-runtime-dependencies` option:

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build.hooks.your-hook-name]
    require-runtime-dependencies = true
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build.hooks.your-hook-name]
    require-runtime-dependencies = true
    ```

Additionally, you may declare dependence on specific [runtime features](metadata.md#optional) of the project with the `require-runtime-features` option:

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build.hooks.your-hook-name]
    require-runtime-features = [
      "feature1",
      "feature2",
    ]
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build.hooks.your-hook-name]
    require-runtime-features = [
      "feature1",
      "feature2",
    ]
    ```

### Order of execution

For each build target, build hooks execute in the order in which they are defined, starting with global hooks.

As an example, for the following configuration:

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build.targets.foo.hooks.hook2]

    [tool.hatch.build.hooks.hook3]
    [tool.hatch.build.hooks.hook1]
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build.targets.foo.hooks.hook2]

    [build.hooks.hook3]
    [build.hooks.hook1]
    ```

When target `foo` is built, build hook `hook3` will be executed first, followed by `hook1`, and then finally `hook2`.

### Conditional execution

If you want to disable a build hook by default and control its use by [environment variables](#environment-variables), you can do so by setting the `enable-by-default` option to `false`:

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build.hooks.<HOOK_NAME>]
    enable-by-default = false
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build.hooks.<HOOK_NAME>]
    enable-by-default = false
    ```

## Environment variables

| Variable | Default | Description |
| --- | --- | --- |
| `HATCH_BUILD_CLEAN` | `false` | Whether or not existing artifacts should first be removed |
| `HATCH_BUILD_CLEAN_HOOKS_AFTER` | `false` | Whether or not build hook artifacts should be removed after each build |
| `HATCH_BUILD_HOOKS_ONLY` | `false` | Whether or not to only execute build hooks |
| `HATCH_BUILD_NO_HOOKS` | `false` | Whether or not to disable all build hooks; this takes precedence over other options |
| `HATCH_BUILD_HOOKS_ENABLE` | `false` | Whether or not to enable all build hooks |
| `HATCH_BUILD_HOOK_ENABLE_<HOOK_NAME>` | `false` |  |
| `HATCH_BUILD_LOCATION` | `dist` | The location with which to build the targets; only used by the [`build`](../cli/reference.md#hatch-build) command |
