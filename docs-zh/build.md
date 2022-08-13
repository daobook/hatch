# 构建

-----

## 配置

构建使用 `tool.hatch.build` 表进行[配置](config/build.md)。每个 [target](config/build.md#build-targets) 都是由 `tool.hatch.build.targets` 部分定义的，例如：

=== ":octicons-file-code-16: pyproject.toml"

    ```toml
    [tool.hatch.build.targets.sdist]
    exclude = [
      "/.github",
      "/docs",
    ]

    [tool.hatch.build.targets.wheel]
    packages = ["src/foo"]
    ```

=== ":octicons-file-code-16: hatch.toml"

    ```toml
    [build.targets.sdist]
    exclude = [
      "/.github",
      "/docs",
    ]

    [build.targets.wheel]
    packages = ["src/foo"]
    ```

## 构建过程

调用不带任何参数的 [`build`](cli/reference.md#hatch-build) 命令将在隔离的环境中构建所有已定义的目标：

```console
$ hatch build
Setting up build environment
[sdist]
dist/hatch_demo-1rc0.tar.gz

Setting up build environment
[wheel]
dist/hatch_demo-1rc0-py3-none-any.whl
```

要只构建特定的目标，使用 `-t`/`--target` 选项：

```console
$ hatch build -t wheel
Setting up build environment
[wheel]
dist/hatch_demo-1rc0-py3-none-any.whl
```

如果目标支持多个[版本](config/build.md#versions)，您可以通过添加冒号和以逗号分隔的所需版本来指定要构建的确切版本：

```console
$ hatch -v build -t wheel:standard
Setting up build environment
...
[wheel]
Building `wheel` version `standard`
dist/hatch_demo-1rc0-py3-none-any.whl
```

## 打包生态

Hatch [遵循](config/build.md#build-system) 现代 Python 打包规范，因此你的项目可以被其他工具使用，而 Hatch 只是作为构建后端。

因此，您可以使用 [tox](https://github.com/tox-dev/tox) 作为 Hatch [环境管理](environment.md) 的替代方案，或者使用 [cibuildwheel](https://github.com/pypa/cibuildwheel) 为每个平台分发包，它们都将透明地使用 Hatch，而无需任何额外的修改。

