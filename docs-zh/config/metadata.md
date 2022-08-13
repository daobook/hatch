# 项目元数据

-----

项目元数据存储在位于项目根目录的 `pyproject.toml` 文件中，完全基于 [PEP 621][]。

## Name (*required*) ## {: #name }

项目的名称。

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [project]
    name = "your-app"
    ```

## Version (*required*) ## {: #version }

=== ":octicons-file-code-16: pyproject.toml"

    === "Dynamic"
        请参阅 [versioning](../version.md) 部分。

        ```toml
        [project]
        ...
        dynamic = ["version"]

        [tool.hatch.version]
        path = "..."
        ```

    === "Static"
        ```toml
        [project]
        ...
        version = "0.0.1"
        ```

## Description

项目概要。

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [project]
    ...
    description = '...'
    ```

## Readme

项目的完整描述。

=== ":octicons-file-code-16: pyproject.toml"

    === "Simple"
        文件扩展名必须为 `.md`、`.rst` 或 `.txt`。

        ```toml
        [project]
        ...
        readme = "README.md"
        ```

    === "Complex"
        `content-type` 字段必须设置为 `text/markdown`， `text/x-rst`，或 `text/plain`。

        === "File"
            还可以设置 `charset` 字段来指示使用哪种编码来读取文件，默认为 `utf-8`。

            ```toml
            [project]
            ...
            readme = {"file" = "README.md", "content-type" = "text/markdown"}
            ```

        === "Text"
            `content-type` 字段必须设置为 `text/markdown` 或 `text/x-rst`。

            ```toml
            [project]
            ...
            readme = {"text" = "...", "content-type" = "text/markdown"}
            ```

!!! note
    如果它被定义为文件，那么它将总是包含在 [source distributions](../plugins/builder/sdist.md) 中以实现一致的构建。

## Python 支持

项目的 Python 版本要求。

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [project]
    ...
    requires-python = ">=3.8"
    ```

## 许可证

更多信息参阅 [PEP 639][]。

=== ":octicons-file-code-16: pyproject.toml"

    === "SPDX expression"

        ```toml
        [project]
        ...
        license = "Apache-2.0 OR MIT"
        ```

    === "Files"

        === "Paths"

            ```toml
            [project]
            ...
            license-files = { paths = ["LICENSE.txt"] }
            ```

        === "Globs"

            ```toml
            [project]
            ...
            license-files = { globs = ["LICENSES/*"] }
            ```

## 所有权

被认为是项目的 `authors` 或 `maintainers` 的人或组织。确切的意思是可以解释的；它可以列出原作者或主要作者，当前的维护人员，或包的所有者。如果两个值相同，则选择使用 `authors` 字段。

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [project]
    ...
    authors = [
      { name = "...", email = "..." },
    ]
    maintainers = [
      { name = "...", email = "..." },
    ]
    ```

## Keywords

用于协助发现项目的关键字。

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [project]
    ...
    keywords = [
      "...",
    ]
    ```

## Classifiers

应用于项目的 [trove 分类器](https://pypi.org/classifiers/)。

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [project]
    ...
    classifiers = [
      "...",
    ]
    ```

## URLs

URL 表，其中键是 URL 标签，值是 URL 本身。

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [project.urls]
    Documentation = "..."
    "Source code" = "..."
    ```

## 依赖关系

格式基于 [PEP 631][]。更多信息请参见 [dependency specification](dependency.md) 部分。

条目支持 [context formatting](context.md)，默认情况下不允许[直接引用](#allowing-direct-references)。

### Required

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [project]
    ...
    dependencies = [
      "...",
    ]
    ```

### Optional

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [project.optional-dependencies]
    option1 = [
      "...",
    ]
    option2 = [
      "...",
    ]
    ```

## Entry points

[入口点](https://packaging.python.org/specifications/entry-points/) 是项目发布组件的一种机制，它提供组件供其他代码发现和使用。

### CLI

在安装了定义 CLI 脚本的项目后，每个键都可以通过调用其关联对象的命令沿着 `PATH` 使用。

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [project.scripts]
    cli-name = "pkg.subpkg:func"
    ```

使用上面的例子，运行 `cli-name` 实际上会执行以下 Python 脚本：

```python
import sys

from pkg.subpkg import func

sys.exit(func())
```

### GUI

GUI 脚本与 CLI 脚本完全相同，除了在 Windows 上，它们被专门处理，以便它们可以在没有控制台的情况下启动。

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [project.gui-scripts]
    gui-name = "pkg.subpkg:func"
    ```

### 插件

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [project.entry-points.plugin-namespace]
    plugin-name1 = "pkg.subpkg1"
    plugin-name2 = "pkg.subpkg2:func"
    ```

## 可选元数据

### 允许直接引用

默认情况下，[dependencies](#dependencies) 不允许定义 [direct references](https://peps.python.org/pep-0440/#direct-references)。要禁用这个检查，设置 `allow-direct-references`  为 `true`：

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.metadata]
    allow-direct-references = true
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [metadata]
    allow-direct-references = true
    ```
