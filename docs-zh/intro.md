# 简介

-----

## 配置

使用 Hatch  [`new`](cli/reference.md#hatch-new) 命令配置项目。

### 新项目

假设你想创建名为 `Hatch Demo` 的项目。可以：

```
hatch new "Hatch Demo"
```

这将在你的当前工作目录中创建以下结构：

```
hatch-demo
├── hatch_demo
│   ├── __about__.py
│   └── __init__.py
├── tests
│   └── __init__.py
├── LICENSE.txt
├── README.md
└── pyproject.toml
```

!!! tip
    有许多方法可以 [自定义](config/project-templates.md) 生成项目。

### 现有的项目

要初始化已存在的项目，进入包含该项目的目录，运行如下命令：

```
hatch new --init
```

如果项目有 `setup.py` 文件，该命令会自动为你迁移 `setuptools` 配置。否则，这将交互式地指导您完成配置过程。

## 项目元数据

接下来，您将希望定义更多位于 `pyproject.toml` 文件中的项目[元数据](config/metadata.md) 。t您可以指定它的[许可](config/metadata.md#license)、[支持的 Python 版本](config/metadata.md#python-support) 以及引用项目各个部分的 [URL](config/metadata.md#urls)，比如文档。

## 依赖关系

配置过程的最后一步是定义 [依赖关系](config/dependency.md)，您希望在项目开始时使用它。

## 配置

所有由 Hatch 识别的特定于项目的配置都在 `pyproject.toml` 文件，或选项不包含在 `tool.hatch` 表的名为 `hatch.toml` 的文件中：

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch]
    option = "..."

    [tool.hatch.table1]
    option = "..."

    [tool.hatch.table2]
    option = "..."
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    option = "..."

    [table1]
    option = "..."

    [table2]
    option = "..."
    ```

在两个文件中定义时，后一个文件中的顶级键优先。

!!! tip
    如果你想让你的文件更紧凑，你可以使用 [dotted keys](https://toml.io/en/v1.0.0#table)，把上面的例子变成：

    === ":octicons-file-code-16: pyproject.toml"

        ```toml
        [tool.hatch]
        option = "..."
        table1.option = "..."
        table2.option = "..."
        ```

    === ":octicons-file-code-16: hatch.toml"

        ```toml
        option = "..."
        table1.option = "..."
        table2.option = "..."
        ```
